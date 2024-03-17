import orjson
import zipfile
import shapely
import pandas as pd
import streamlit as st


@st.cache_resource
def load_municipality_borders_from_json(
    prefecture: str,
    target_city_names: set[str]
) -> pd.DataFrame:
    with open(f"municipality/json/{prefecture}.json", "r", encoding="utf-8") as f:
        json_str = f.read()
        data = orjson.loads(json_str)

    pref_city_indices = {v: k for k, v in data["pref_city"].items()}
    lonlat_coordinates = data["lonlat_coordinates"]

    target_pref_cities = [f"{prefecture} {c}" for c in target_city_names]
    target_indices = [pref_city_indices[c] for c in target_pref_cities]
    target_coordinates = [lonlat_coordinates[i] for i in target_indices]

    df_data = {
        "pref_city": target_pref_cities,
        "lonlat_coordinates": target_coordinates,
    }
    return pd.DataFrame(
        data=df_data,
        columns=df_data.keys()
    )


def load_municipality_borders_from_json_multi(
    prefecture_and_cities: dict[str, set[str]]) -> pd.DataFrame:
    return pd.concat([load_municipality_borders_from_json(prefecture, city_names)
                      for prefecture, city_names in prefecture_and_cities.items()])

# @st.cache_resource
# def load_municipality_data(prefecture: str) -> pd.DataFrame:
#     with open(f"municipality/{prefecture}.geojson", "r", encoding="utf-8") as f:
#         geojson_str = f.read()
#         geojson = orjson.load(geojson_str)
#         return _parse_municipality_json(geojson)
