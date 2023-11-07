
import json
import zipfile
import shapely
import pandas as pd
import streamlit as st


@st.cache_resource
def load_municipality_data_zip(prefecture: str) -> pd.DataFrame:
    with zipfile.ZipFile(f"municipality/{prefecture}.zip", 'r') as zf:
        geojson_file_name = zf.namelist()[0]
        with zf.open(geojson_file_name, 'r') as file:
            geojson = json.load(file)
            return _parse_municipality_json(geojson)


@st.cache_resource
def load_municipality_data(prefecture: str) -> pd.DataFrame:
    with open(f"municipality/{prefecture}.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
        return _parse_municipality_json(geojson)


def _parse_municipality_json(geojson: dict) -> pd.DataFrame:
    prefecture_names: list[str] = []
    city_names: list[str] = []
    polygons: list[list[list[list[float]]]] = []

    for f in geojson["features"]:
        prop = f["properties"]

        # simplify municipality contours
        shape = shapely.geometry.shape(f["geometry"])
        if shape.type != "Polygon":
            continue
        simple_shape = shape.simplify(0.0005, preserve_topology=False)
        if simple_shape.is_empty:
            continue

        if simple_shape.type == "Polygon":
            polygons.append(list(simple_shape.exterior.coords))
            prefecture_names.append(prop["N03_001"])
            city_names.append(prop["N03_004"])
        elif simple_shape.type == "MultiPolygon":
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
