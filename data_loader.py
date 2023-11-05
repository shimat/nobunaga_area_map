import functools
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
    addresses: list[str] = []
    areas: list[float] = []
    lonlat_lists: list[list[list[list[float]]]] = []

    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]
        prefecture_names.append(elem.find("fme:PREF_NAME", NAMESPACES).text)
        city_name = elem.find("fme:CITY_NAME", NAMESPACES).text
        town_name = elem.find("fme:S_NAME", NAMESPACES).text
        city_names.append(city_name)
        addresses.append(f"{city_name} {town_name}")
        areas.append(float(elem.find("fme:AREA", NAMESPACES).text))

        pos_list_elem = elem.find("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior//gml:LinearRing//gml:posList", NAMESPACES)
        pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
        lonlat_list = [[[pos_list[i*2+1], pos_list[i*2]] for i in range(len(pos_list) // 2)]]
        lonlat_lists.append(lonlat_list)

    data = {
        "prefecture_name": prefecture_names,
        "city_name": city_names,
        "address": addresses,
        "area": areas,
        "lonlat_coordinates": lonlat_lists,
    }
    return pd.DataFrame(
        data=data,
        columns=data.keys()
    )


def mod_data(df: pd.DataFrame, area_data: Correspondences) -> pd.DataFrame:
    new_data = {
        "prefecture_name": [],
        "address": [],
        "area": [],
        "kokudaka": [],
        "sub_addresses": [],
        "own": [],
        "fill_color": [],
        "lonlat_coordinates": [],
    }
    for address, correespondence in area_data.items():
        if correespondence is None or correespondence.towns is None:
            sub_addresses = []
            own = False
        else:
            sub_addresses = correespondence.towns
            own = correespondence.own
        sub_addresses.append(address)
        sub_rows = df[df["address"].isin(sub_addresses)]
        prefecture_name = sub_rows.iloc[0]["prefecture_name"]
        area: float = sub_rows["area"].sum()
        kokudaka = estimate_kokudaka(area)

        # st.write(new_data["address"][-1], sub_rows)
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
            # st.write(new_data["address"][-1], coords)
        else:
            raise
        
        simplified_sub_addresses = [s.split(" ")[1:] for s in sub_addresses]
        
        fill_color = [0, 192, 255, 128] if own else [0, 0, 0, 0]

        if len(coords) > 1:
            address += " (飛び地あり)"
        for c in coords:
            new_data["prefecture_name"].append(prefecture_name)
            new_data["address"].append(address)
            new_data["area"].append(round(area))
            new_data["kokudaka"].append(round(kokudaka, 2))
            new_data["sub_addresses"].append(simplified_sub_addresses)
            new_data["lonlat_coordinates"].append([c])
            new_data["own"].append(own)
            new_data["fill_color"].append(fill_color)

    return pd.DataFrame(
        data=new_data,
        columns=new_data.keys()
    )


def estimate_kokudaka(area: float) -> float:
    return (area ** 0.497) / 30
