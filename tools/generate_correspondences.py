# data/correspondences/*.yaml の基本形を簡単に生成する。
# 経済センサスデータにおける100,000m^2越えの町丁が単独で1エリアになると仮定して出力。
# それ以下の町丁は末尾に余りとして付加。

import argparse
import functools
import json
import os
import os.path
import zipfile
import itertools
import more_itertools
import shapely
from io import StringIO
from pathlib import Path
from typing import NamedTuple
from xml.etree import ElementTree
from pydantic import BaseModel, Field
from ruamel.yaml import YAML


class ViewState(BaseModel):
    latitude: float
    longitude: float
    zoom: float


class OneCorrespondence(BaseModel):
    towns: tuple[str, ...] = Field(min_length=1)


class OneAreaData(BaseModel):
    view_state: ViewState
    correspondences: tuple[OneCorrespondence, ...]


class AllAreasData(BaseModel):
    areas: dict[str, OneAreaData]


class Town(NamedTuple):
    city_name: str
    town_name: str
    area: float
    exterior_coordinates: list[list[list[float]]]


def load_town_data_from_gml_zip(file_name: str) -> list[Town]:
    with zipfile.ZipFile(file_name, 'r') as zf:
        gml_file_name = more_itertools.first_true(zf.namelist(), pred=lambda f: os.path.splitext(f)[1] == ".gml")
        if not gml_file_name:
            raise Exception(f"GML file not found in ZipFile '{file_name}'")
        with zf.open(gml_file_name, 'r') as file:
            tree = ElementTree.parse(file)
            return load_town_data(tree)


def load_town_data(tree: ElementTree) -> list[Town]:
    # https://tm23forest.com/contents/python-jpgis-gml-dem-geotiff
    NAMESPACES = {
        "gml": "http://www.opengis.net/gml",
        "fme": "http://www.safe.com/gml/fme",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xlink": "http://www.w3.org/1999/xlink"
    }

    areas: list[Town] = []
    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]
        city_name = elem.find("fme:CITY_NAME", NAMESPACES).text
        town_name = elem.find("fme:S_NAME", NAMESPACES).text or "(町名無し)"
        area = float(elem.find("fme:AREA", NAMESPACES).text)

        exterior_coordinates: list[list[list[float]]] = []
        contour_elements = elem.findall("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior", NAMESPACES)
        for contour_elem in contour_elements:
            pos_list_elem = contour_elem.find("gml:LinearRing//gml:posList", NAMESPACES)
            pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
            lonlat_list = [[pos_list[i*2+1], pos_list[i*2]] for i in range(len(pos_list) // 2)]
            exterior_coordinates.append(lonlat_list)

        areas.append(Town(city_name, town_name, area, exterior_coordinates))
    return areas


ap = argparse.ArgumentParser()
ap.add_argument("prefecture_name", type=str)
ap.add_argument("city_name", type=str)
args = ap.parse_args()


# GMLから読み込み、対象市区町村内の町丁に絞る
gml_path = Path(f"../gml/経済センサス_活動調査_{args.prefecture_name}.zip")
areas = [
    a for a in load_town_data_from_gml_zip(gml_path)
    if a.city_name == args.city_name]
if not areas:
    print("No data found")
    exit(-1)
areas = sorted(areas, key=lambda a: a.town_name)

# 飛び地を考慮してgroupbyしたのち、各町丁ごとに面積が10石(10万平米)を超えるものをピックアップ
towns: list[list[str]] = []
small_towns: list[str] = []
polygons: list[shapely.geometry.Polygon] = []
groups = itertools.groupby(areas, key=lambda a: a.town_name)
for town_name, elems in groups:
    elems = list(elems)
    area_total = sum(a.area for a in elems)
    if area_total >= 100000:
        towns.append([town_name])
    else:
        small_towns.append(town_name)
    polygons.extend(
        shapely.geometry.Polygon(c) for e in elems for c in e.exterior_coordinates)
if small_towns:
    towns.append(small_towns)
print(towns)

# 輪郭から重心を求める
# print(polygons)
merged_polygon = functools.reduce(lambda r, s: r.union(s), polygons[1:], polygons[0])
centroid: shapely.Point = merged_polygon.centroid
print(f"centroid = {centroid}")

write_data = AllAreasData(
    areas={
        f"{args.prefecture_name} {args.city_name}":
            OneAreaData(
                view_state=ViewState(latitude=centroid.y, longitude=centroid.x, zoom=10.0),
                correspondences=tuple(OneCorrespondence(towns=tuple(t)) for t in towns))
    },
)


json_val = write_data.model_dump_json()
json_dict = json.loads(json_val)
yaml_writer = YAML()
s = StringIO()
yaml_writer.dump(json_dict, s)
s.seek(0)
yaml_str = s.read()
# yaml_str = pydantic_yaml.to_yaml_str(write_data)

os.makedirs("out", exist_ok=True)
Path(f"out/{args.prefecture_name}_{args.city_name}.yaml").write_text(yaml_str, encoding="utf-8")
