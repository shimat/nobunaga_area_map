
import orjson
import zipfile
import shapely
import pandas as pd
import streamlit as st
from typing import Iterable
from collections.abc import Container


@st.cache_resource
def load_municipality_data_zip(
    prefecture: str,
    target_city_names: Container[str] | Iterable[str]
) -> pd.DataFrame:
    with zipfile.ZipFile(f"municipality/{prefecture}.zip", 'r') as zf:
        geojson_file_name = zf.namelist()[0]
        with zf.open(geojson_file_name, 'r') as file:
            geojson_str = file.read()
            geojson = orjson.loads(geojson_str)
            return _parse_municipality_json(geojson, target_city_names)


@st.cache_resource
def load_municipality_geojson_simplified(prefecture: str) -> pd.DataFrame:
    with zipfile.ZipFile(f"municipality/{prefecture}.zip", 'r') as zf:
        geojson_file_name = zf.namelist()[0]
        with zf.open(geojson_file_name, 'r') as file:
            geojson_str = file.read()
            geojson = orjson.loads(geojson_str)
            _simplify_geojson_coordinates(geojson)
            return geojson


# @st.cache_resource
# def load_municipality_data(prefecture: str) -> pd.DataFrame:
#     with open(f"municipality/{prefecture}.geojson", "r", encoding="utf-8") as f:
#         geojson_str = f.read()
#         geojson = orjson.load(geojson_str)
#         return _parse_municipality_json(geojson)


def _simplify_geojson_coordinates(geojson: dict) -> None:
    remove_indices = []
    exclude_guns = {"択捉郡", "蘂取郡", "紗那郡", "国後郡", "色丹郡"}

    for i, f in enumerate(geojson["features"]):

        prop = f["properties"]
        if prop["N03_003"] in exclude_guns:
            remove_indices.append(i)
            continue

        shape = shapely.geometry.shape(f["geometry"])
        if shape.geom_type != "Polygon":
            remove_indices.append(i)
            continue

        simple_shape = shape.simplify(0.001, preserve_topology=False)
        if simple_shape.is_empty:
            remove_indices.append(i)
            continue
    
        if simple_shape.geom_type == "Polygon":
            # print(f["geometry"]["coordinates"])
            f["geometry"]["coordinates"].clear()
            f["geometry"]["coordinates"].append(list(simple_shape.exterior.coords))
            # print(f["geometry"]["coordinates"])
        elif simple_shape.geom_type == "MultiPolygon":
            pass

    for i in reversed(remove_indices):
        geojson["features"].pop(i)


def _parse_municipality_json(
    geojson: dict,
    target_city_names: Container[str] | Iterable[str]
) -> pd.DataFrame:
    prefecture_names: list[str] = []
    city_names: list[str] = []
    polygons: list[list[list[list[float]]]] = []

    for f in geojson["features"]:
        prop = f["properties"]

        if prop["N03_003"]:
            if (prop["N03_003"]+prop["N03_004"]) not in target_city_names:
                continue
        elif prop["N03_004"] not in target_city_names:
            continue

        # simplify municipality contours
        shape = shapely.geometry.shape(f["geometry"])
        if shape.geom_type != "Polygon":
            continue
        simple_shape = shape.simplify(0.0005, preserve_topology=True)
        if simple_shape.is_empty:
            continue

        if simple_shape.geom_type == "Polygon":
            polygons.append(list(simple_shape.exterior.coords))
            prefecture_names.append(prop["N03_001"])
            city_names.append(prop["N03_004"])
        elif simple_shape.geom_type == "MultiPolygon":
            for p in simple_shape.geoms:
                prefecture_names.append(prop["N03_001"])
                city_names.append(prop["N03_004"])
                polygons.append(list(p.exterior.coords))

    data = {
        "prefecture_name": prefecture_names,
        "city_name": city_names,
        "lonlat_coordinates": polygons,
    }
    return pd.DataFrame(
        data=data,
        columns=data.keys()
    )
