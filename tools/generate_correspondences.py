# data/correspondences/*.yaml の基本形を簡単に生成する。
# 経済センサスデータにおける100,000m^2越えの町丁が単独で1エリアになると仮定して出力。
# それ以下の町丁は末尾に余りとして付加。

import argparse
import os
import os.path
import zipfile
import itertools
import more_itertools
from pathlib import Path
from typing import NamedTuple
from xml.etree import ElementTree
from pydantic import BaseModel, Field
import pydantic_yaml




class OneCorrespondence(BaseModel):
    towns: tuple[str, ...] = Field(min_length=1)


class OneAreaData(BaseModel):
    correspondences: tuple[OneCorrespondence, ...]


class AllAreasData(BaseModel):
    areas: dict[str, OneAreaData]


class GmlArea(NamedTuple):
    city_name: str
    town_name: str
    area: float


def load_town_data_from_gml_zip(file_name: str) -> list[GmlArea]:
    with zipfile.ZipFile(file_name, 'r') as zf:
        gml_file_name = more_itertools.first_true(zf.namelist(), pred=lambda f: os.path.splitext(f)[1] == ".gml")
        if not gml_file_name:
            raise Exception(f"GML file not found in ZipFile '{file_name}'")
        with zf.open(gml_file_name, 'r') as file:
            tree = ElementTree.parse(file)
            return load_town_data(tree)


def load_town_data(tree: ElementTree) -> list[GmlArea]:
    # https://tm23forest.com/contents/python-jpgis-gml-dem-geotiff
    NAMESPACES = {
        "gml": "http://www.opengis.net/gml",
        "fme": "http://www.safe.com/gml/fme",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xlink": "http://www.w3.org/1999/xlink"
    }

    areas: list[GmlArea] = []
    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]
        city_name = elem.find("fme:CITY_NAME", NAMESPACES).text
        town_name = elem.find("fme:S_NAME", NAMESPACES).text or "(町名無し)"
        area = float(elem.find("fme:AREA", NAMESPACES).text)
        areas.append(GmlArea(city_name, town_name, area))
    return areas


ap = argparse.ArgumentParser()
ap.add_argument("prefecture_name", type=str)
ap.add_argument("city_name", type=str)
args = ap.parse_args()

print(args)

gml_path = Path(f"../gml/経済センサス_活動調査_{args.prefecture_name}.zip")
areas = [
    a for a in load_town_data_from_gml_zip(gml_path)
    if a.city_name == args.city_name]
areas = sorted(areas, key=lambda a: a.town_name)

towns: list[list[str]] = []
small_towns: list[str] = []
groups = itertools.groupby(areas, key=lambda a: a.town_name)
for town_name, elems in groups:
    area_total = sum(a.area for a in elems)
    if area_total>= 100000:
        towns.append([town_name])
    else:
        small_towns.append(town_name)
if small_towns:
    towns.append(small_towns)
print(towns)



write_data = AllAreasData(areas={
    f"{args.prefecture_name} {args.city_name}":
        OneAreaData(correspondences=tuple(OneCorrespondence(towns=tuple(t)) for t in towns))
})

os.makedirs("out", exist_ok=True)
yaml_str = pydantic_yaml.to_yaml_str(write_data)
Path(f"out/{args.prefecture_name}_{args.city_name}.yaml").write_text(yaml_str, encoding="utf-8")
