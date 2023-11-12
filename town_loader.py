import functools
import itertools
import more_itertools
import pandas as pd
import streamlit as st
import shapely
import zipfile
from os.path import splitext
from xml.etree import ElementTree
from area_loader import Correspondences

# https://tm23forest.com/contents/python-jpgis-gml-dem-geotiff
NAMESPACES = {
    "gml": "http://www.opengis.net/gml",
    "fme": "http://www.safe.com/gml/fme",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink"
}


@st.cache_resource
def load_town_data_from_gml_zip(file_name: str) -> pd.DataFrame:
    with zipfile.ZipFile(file_name, 'r') as zf:
        gml_file_name = more_itertools.first_true(zf.namelist(), pred=lambda f: splitext(f)[1] == ".gml")
        with zf.open(gml_file_name, 'r') as file:
            tree = ElementTree.parse(file)
            return load_town_data(tree)


@st.cache_data
def load_town_data_from_gml(file_name: str) -> pd.DataFrame:
    tree = ElementTree.parse(file_name)
    return load_town_data(tree)


def load_town_data(tree: ElementTree) -> pd.DataFrame:
    prefecture_names: list[str] = []
    city_names: list[str] = []
    pref_cities: list[str] = []
    town_names: list[str] = []
    areas: list[float] = []
    all_towns_polygons: list[list[list[list[float]]]] = []

    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]
        prefecture_names.append(elem.find("fme:PREF_NAME", NAMESPACES).text)
        city_name = elem.find("fme:CITY_NAME", NAMESPACES).text
        town_name = elem.find("fme:S_NAME", NAMESPACES).text or "(町名無し)"
        city_names.append(city_name)
        pref_cities.append(f"{prefecture_names[-1]} {city_name}")
        town_names.append(town_name)
        areas.append(float(elem.find("fme:AREA", NAMESPACES).text))

        polygons = []
        contour_elements = itertools.chain(
              elem.findall("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior", NAMESPACES),
              elem.findall("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:interior", NAMESPACES))
        for contour_elem in contour_elements:
            pos_list_elem = contour_elem.find("gml:LinearRing//gml:posList", NAMESPACES)
            pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
            lonlat_list = [[pos_list[i*2+1], pos_list[i*2]] for i in range(len(pos_list) // 2)]
            polygons.append(lonlat_list)
        all_towns_polygons.append(polygons)

    data = {
        "prefecture_name": prefecture_names,
        "city_name": city_names,
        "pref_city": pref_cities,
        "town_name": town_names,
        "area": areas,
        "lonlat_coordinates": all_towns_polygons,
    }
    return pd.DataFrame(
        data=data,
        columns=data.keys()
    )


def load_town_data_(tree: ElementTree) -> pd.DataFrame:
    prefecture_names: list[str] = []
    city_names: list[str] = []
    pref_cities: list[str] = []
    town_names: list[str] = []
    areas: list[float] = []
    lonlat_lists: list[list[list[list[float]]]] = []

    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]
        prefecture_names.append(elem.find("fme:PREF_NAME", NAMESPACES).text)
        city_name = elem.find("fme:CITY_NAME", NAMESPACES).text
        town_name = elem.find("fme:S_NAME", NAMESPACES).text
        city_names.append(city_name)
        pref_cities.append(f"{prefecture_names[-1]} {city_name}")
        town_names.append(town_name)
        areas.append(float(elem.find("fme:AREA", NAMESPACES).text))

        pos_list_elem = elem.find("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior//gml:LinearRing//gml:posList", NAMESPACES)
        pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
        lonlat_list = [[[pos_list[i*2+1], pos_list[i*2]] for i in range(len(pos_list) // 2)]]
        lonlat_lists.append(lonlat_list)

    data = {
        "prefecture_name": prefecture_names,
        "city_name": city_names,
        "pref_city": pref_cities,
        "town_name": town_names,
        "area": areas,
        "lonlat_coordinates": lonlat_lists,
    }
    return pd.DataFrame(
        data=data,
        columns=data.keys()
    )


#@st.cache_data
def mod_data(df: pd.DataFrame, _area_data_list: list[Correspondences], cache_key: str) -> pd.DataFrame:
    new_data = {
        "prefecture_name": [],
        "city_name": [],
        "area_name": [],
        "area": [],
        "kokudaka": [],
        "sub_towns": [],
        "sub_towns_suffix": [],
        "own": [],
        "fill_color": [],
        "lonlat_coordinates": [],
    }
    for area_data in _area_data_list:
        pref_city = area_data.pref_city
        for area_name, correespondence in area_data.values.items():
            if correespondence is None or correespondence.towns is None:
                sub_towns = []
                own = 0
            else:
                sub_towns = correespondence.towns
                own = correespondence.own
            sub_towns.append(area_name)

            sub_rows = df[(df["pref_city"] == pref_city) & df["town_name"].isin(sub_towns)]
            if sub_rows.empty:
                raise Exception(f"Town not found ({pref_city=}, {sub_towns=})")
            prefecture_name = sub_rows.iloc[0]["prefecture_name"]
            city_name = sub_rows.iloc[0]["city_name"]
            area: float = sub_rows["area"].sum()
            kokudaka = estimate_kokudaka(area)

            # st.write(new_data["address"][-1], sub_rows)
            polygons = [shapely.geometry.Polygon(c[0])
                        for c in sub_rows["lonlat_coordinates"].values]
            if not polygons:
                continue
            merged_polygon = functools.reduce(lambda r, s: r.union(s), polygons[1:], polygons[0])
            simple_polygon = merged_polygon.simplify(0.0002, preserve_topology=True)

            if simple_polygon.geom_type == "Polygon":
                coords = [list(simple_polygon.exterior.coords)]
            elif simple_polygon.geom_type == "MultiPolygon":
                coords = [list(p.exterior.coords) for p in simple_polygon.geoms]
                # st.write(new_data["address"][-1], coords)
            else:
                raise

            simplified_sub_towns = [s.split(" ")[1:] for s in sub_towns]

            fill_color = arrival_color(own)

            if len(coords) > 1:
                area_name += " [飛び地あり]"
            sub_towns_suffix = ""
            if len(simplified_sub_towns) > 1:
                sub_towns_suffix = f" (+{len(simplified_sub_towns)-1}町)"

            for c in coords:
                new_data["prefecture_name"].append(prefecture_name)
                new_data["city_name"].append(city_name)
                new_data["area_name"].append(area_name)
                new_data["area"].append(round(area))
                new_data["kokudaka"].append(round(kokudaka, 2))
                new_data["sub_towns"].append(simplified_sub_towns)
                new_data["sub_towns_suffix"].append(sub_towns_suffix)
                new_data["lonlat_coordinates"].append([c])
                new_data["own"].append(own)
                new_data["fill_color"].append(fill_color)

    return pd.DataFrame(
        data=new_data,
        columns=new_data.keys()
    )


def estimate_kokudaka(area: float) -> float:
    return (area ** 0.497) / 30


def arrival_color(own: int) -> list[int]:
    match own:
        case 0:  # 未踏
            return [192, 192, 192, 64]
        case 1:  # 直接来訪
            return [0, 192, 255, 128]
        case 2:  # 遠征
            return [0, 255, 102, 128]
        case _:
            raise
