import os
import zipfile
from xml.etree import ElementTree as ET

import more_itertools
import pandas as pd
import pydeck
import shapely
import streamlit as st

NAMESPACES = {
    "gml": "http://www.opengis.net/gml",
    "fme": "http://www.safe.com/gml/fme",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink",
}


def load_town_data_from_gml_zip(file_name: str) -> pd.DataFrame:
    with zipfile.ZipFile(file_name, "r") as zf:
        gml_file_name = more_itertools.first_true(zf.namelist(), pred=lambda f: os.path.splitext(f)[1] == ".gml")
        if not gml_file_name:
            raise Exception(f"GML file not found in ZipFile '{file_name}'")
        with zf.open(gml_file_name, "r") as file:
            tree = ET.parse(file)
            return load_town_data(tree)


def load_town_data(tree: ET.ElementTree) -> pd.DataFrame:
    all_towns_polygons: dict[str, list[list[list[float]]]] = {}

    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]
        prefecture_name = elem.find("fme:PREF_NAME", NAMESPACES).text
        city_name = elem.find("fme:CITY_NAME", NAMESPACES).text
        if not prefecture_name or not city_name:
            continue
        pref_city = f"{prefecture_name} {city_name}"

        polygons: list[list[list[float]]] = []
        contour_elements = elem.findall(
            "gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior",
            NAMESPACES,
        )
        for contour_elem in contour_elements:
            pos_list_elem = contour_elem.find("gml:LinearRing//gml:posList", NAMESPACES)
            pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
            lonlat_list = [[pos_list[i * 2 + 1], pos_list[i * 2]] for i in range(len(pos_list) // 2)]
            polygons.append(lonlat_list)

        if pref_city not in all_towns_polygons:
            all_towns_polygons[pref_city] = []
        all_towns_polygons[pref_city].extend(polygons)

    merged_polygons = merge_contours_by_municipality(all_towns_polygons)

    data = {
        "pref_city": list(merged_polygons.keys()),
        "lonlat_coordinates": list(merged_polygons.values()),
    }
    return pd.DataFrame(data=data, columns=list(data.keys()))


def merge_contours_by_municipality(
    all_coordinates: dict[str, list[list[list[float]]]],
) -> dict[str, list[list[list[float]]]]:
    result = {}
    for pref_city, coordinates in all_coordinates.items():
        print(pref_city)
        polygons = [shapely.Polygon(c) for c in coordinates]
        # st.write(pref_city, coordinates)
        merged_polygon = shapely.unary_union(polygons)
        simple_polygon = merged_polygon.simplify(0.0002, preserve_topology=True)
        match simple_polygon.geom_type:
            case "Polygon":
                coords = [list(simple_polygon.exterior.coords)]
            case "MultiPolygon":
                coords = [list(p.exterior.coords) for p in simple_polygon.geoms]
            case _:
                raise Exception(f"Unexpected geom_type '{simple_polygon.geom_type}'")
        result[pref_city] = coords
    return result


prefecture = st.selectbox(
    label="都道府県",
    options=(
        "北海道",
        "青森県",
        "岩手県",
        "宮城県",
        "秋田県",
        "山形県",
        "福島県",
        "茨城県",
        "栃木県",
        "群馬県",
        "埼玉県",
        "東京都",
        "神奈川県",
        "千葉県",
        "富山県",
        "石川県",
        "福井県",
        "山梨県",
        "長野県",
        "岐阜県",
        "静岡県",
        "愛知県",
        "三重県",
        "滋賀県",
        "京都府",
        "広島県",
        "徳島県",
        "大分県",
    ),
    index=None,
)
if prefecture:
    df = load_town_data_from_gml_zip(f"./gml/経済センサス_活動調査_{prefecture}.zip")
    st.dataframe(df)

    os.makedirs("out", exist_ok=True)
    df.to_json(f"out/{prefecture}.json", index=False, force_ascii=False, indent=None)
    # df.to_json(f"out/{prefecture}.zip", index=False, force_ascii=False, indent=2, compression="zip")

    deck = pydeck.Deck(
        layers=[
            pydeck.Layer(
                "PolygonLayer",
                df,
                stroked=True,
                filled=False,
                extruded=False,
                wireframe=True,
                line_width_scale=60,
                line_width_min_pixels=1,
                get_polygon="lonlat_coordinates",
                get_line_color=[255, 255, 255],
                auto_highlight=False,
                pickable=False,
            )
        ],
        initial_view_state=pydeck.ViewState(
            latitude=36.26,
            longitude=138.15,
            zoom=4.0,
            maxzoom=16,
            pitch=0,
            bearing=0,
        ),
        tooltip={"text": ""},  # type: ignore
        height=600,
        map_provider="carto",
        map_style="dark",
    )
    st.components.v1.html(deck.to_html(as_string=True), height=600)
