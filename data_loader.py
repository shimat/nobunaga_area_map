import functools
import json
import more_itertools
import pandas as pd
import streamlit as st
import shapely
import zipfile
from os.path import splitext
from xml.etree import ElementTree

# https://tm23forest.com/contents/python-jpgis-gml-dem-geotiff
NAMESPACES = {
    "gml": "http://www.opengis.net/gml",
    "fme": "http://www.safe.com/gml/fme",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink"
}


def load_data_from_gml_zip(file_name: str) -> pd.DataFrame:
    with zipfile.ZipFile(file_name, 'r') as zf:
        gml_file_name = more_itertools.first_true(zf.namelist(), pred=lambda f: splitext(f)[1] == ".gml")
        with zf.open(gml_file_name, 'r') as file:
            tree = ElementTree.parse(file)
            return load_data(tree)


@st.cache_data
def load_data_from_gml(file_name: str) -> pd.DataFrame:
    tree = ElementTree.parse(file_name)
    return load_data(tree)


def load_data(tree: ElementTree) -> pd.DataFrame:
    # root = tree.getroot()

    # bounded_by = tree.find("gml:boundedBy", NAMESPACES)
    # st.write(bounded_by)

    prefecture_names: list[str] = []
    city_names: list[str] = []
    town_names: list[str] = []
    addresses: list[str] = []
    areas: list[float] = []
    perimeters: list[float] = []
    populations: list[int] = []
    household_counts: list[int] = []
    lonlat_lists: list[list[list[list[float]]]] = []

    for index, feature_member in enumerate(tree.findall("gml:featureMember", NAMESPACES)):
        elem = feature_member[0]
        prefecture_names.append(elem.find("fme:PREF_NAME", NAMESPACES).text)
        city_names.append(elem.find("fme:CITY_NAME", NAMESPACES).text)
        town_names.append(elem.find("fme:S_NAME", NAMESPACES).text)
        addresses.append(f"{city_names[-1]} {town_names[-1]}")
        areas.append(float(elem.find("fme:AREA", NAMESPACES).text))
        perimeters.append(float(elem.find("fme:PERIMETER", NAMESPACES).text))
        #populations.append(int(elem.find("fme:JINKO", NAMESPACES).text))
        #household_counts.append(int(elem.find("fme:SETAI", NAMESPACES).text))
        populations.append(0)
        household_counts.append(0)

        pos_list_elem = elem.find("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior//gml:LinearRing//gml:posList", NAMESPACES)
        pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
        lonlat_list = [[[pos_list[i*2+1], pos_list[i*2]] for i in range(len(pos_list) // 2)]]
        lonlat_lists.append(lonlat_list)

    data = {
        "prefecture_name": prefecture_names,
        "city_name": city_names,
        "town_name": town_names,
        "address": addresses,
        "area": areas,
        "perimeter": perimeters,
        "population": populations,
        "household_count": household_counts,
        "lonlat_coordinates": lonlat_lists,
    }
    return pd.DataFrame(
        data=data,
        columns=data.keys()
    )


def mod_data(df: pd.DataFrame) -> pd.DataFrame:
    with open("nobunaga_areas_correspondences.json", "r", encoding="utf-8-sig") as f:
        PAIRS = json.load(f)

    new_data = {
        "prefecture_name": [],
        "address": [],
        "area": [],
        "perimeter": [],
        "population": [],
        "household_count": [],
        "estimated_kokudaka": [],
        "lonlat_coordinates": [],
    }
    for address, sub_addresses in PAIRS.items():
        sub_rows = df.query("address in @sub_addresses")
        # st.dataframe(sub_rows)
        #new_data["prefecture_name"].append(sub_rows.iloc[0]["prefecture_name"])
        new_data["prefecture_name"].append("")
        new_data["address"].append(address)
        new_data["area"].append(sub_rows["area"].sum())
        new_data["perimeter"].append(sub_rows["perimeter"].sum())
        new_data["population"].append(sub_rows["population"].sum())
        new_data["household_count"].append(sub_rows["household_count"].sum())

        kokudaka = estimate_kokudaka(new_data["area"][-1])
        new_data["estimated_kokudaka"].append(f"{kokudaka:.1f}")

        polygons = [shapely.geometry.Polygon(c[0])
                    for c in sub_rows["lonlat_coordinates"].values]
        if not polygons:
            new_data["lonlat_coordinates"].append([])
            continue
        merged_polygon = functools.reduce(lambda r, s: r.union(s), polygons[1:], polygons[0])
        if merged_polygon.geom_type == "Polygon":
            coords = [list(merged_polygon.exterior.coords)]
        elif merged_polygon.geom_type == "MultiPolygon":
            coords = [list(p.exterior.coords) for p in merged_polygon.geoms]
        else:
            raise
        new_data["lonlat_coordinates"].append(coords)

    x = pd.DataFrame(
        data=new_data,
        columns=new_data.keys()
    )
    # st.dataframe(x)
    return x

    # df = df[:5800]
    # return df


def estimate_kokudaka(area: float):
    return 0.035 * (area ** 0.494)
