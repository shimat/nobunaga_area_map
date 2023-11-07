import json
import pandas as pd
import streamlit as st


def load_municipality_data(prefecture: str) -> pd.DataFrame:
    with open(f"municipality/{prefecture}.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)
    #st.write(geojson)
    
    prefecture_names: list[str] = []
    city_names: list[str] = []
    polygons: list[list[list[list[float]]]] = []

    for f in geojson["features"]:
        prop = f["properties"]
        prefecture_names.append(prop["N03_001"])
        city_names.append(prop["N03_004"])
        # TODO: simplify https://shapely.readthedocs.io/en/stable/manual.html#object.simplify
        polygons.append(f["geometry"]["coordinates"])
    
    data = {
        "prefecture_name": prefecture_names,
        "city_name": city_names,
        "lonlat_coordinates": polygons,
    }
    return pd.DataFrame(
        data=data,
        columns=data.keys()
    )
