import itertools
import more_itertools
import orjson
import pickle
import shapely  # type: ignore
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import pydeck
from typing import Sequence, NamedTuple, TypeAlias
from town_data import load_town_data_from_gml_zip
from models import TownPolygon


Contours: TypeAlias = list[list[list[float]]]

EXCLUDED_TOWNS = {
    "東京都_千代田区_皇居外苑",
    "東京都_千代田区_千代田",
    "東京都_港区_元赤坂２丁目",
}
TARGET_PREFECTURES = ("北海道", "青森県", "東京都", "埼玉県", "神奈川県", "千葉県", "茨城県", )
DEFAULT_TARGET_PREFECTURES = ("東京都", "埼玉県", "神奈川県", "千葉県", )
MAP_HEIGHT = 1000


class MunicipalityBorder(NamedTuple):
    pref_city: str
    coordinates: Contours


#@st.cache_resource
def load_municipality_borders_from_json(prefecture: str) -> dict[str, shapely.Polygon]:
    with open(f"../municipality/json/{prefecture}.json", "r", encoding="utf-8") as f:
        json_str = f.read()
        data = orjson.loads(json_str)

    # pref_city_indices = {v: k for k, v in data["pref_city"].items()}
    # lonlat_coordinates = data["lonlat_coordinates"]

    #target_pref_cities = [f"{prefecture} {c}" for c in target_city_names]
    #target_indices = [pref_city_indices[c] for c in target_pref_cities]
    #target_coordinates = [lonlat_coordinates[i] for i in target_indices]

    indices = list(data["pref_city"].keys())
    result: dict[str, shapely.Polygon] = {}
    for i in indices:
        coordinates = data["lonlat_coordinates"][i]
        if len(coordinates) == 1:
            result[data["pref_city"][i]] = shapely.Polygon(shell=coordinates[0])
        else:
            result[data["pref_city"][i]] = shapely.Polygon(shell=coordinates[0], holes=coordinates[1:])
    return result


# @st.cache_data
def build_city_graph(prefectures: Sequence[str]) -> nx.Graph:
    border_data: dict[str, shapely.Polygon] = {}
    for prefecture in prefectures:
        border_data.update(load_municipality_borders_from_json(prefecture))

    graph = nx.Graph()
    for city1, city2 in itertools.combinations(border_data.keys(), 2):
        poly1 = border_data[city1]
        poly2 = border_data[city2]
        if poly1.intersects(poly2):
            # print(f"{city1} touches {city2}")
            graph.add_edge(city1, city2)
        else:
            graph.add_node(city1)
            graph.add_node(city2)

    #fig = plt.figure(1, figsize=(25.0, 15.0))
    #nx.draw(graph, with_labels=True, font_family="Meiryo")
    #st.pyplot(fig)

    return graph


@st.cache_data
def build_town_graph(
    _town_polygons_dict: dict[str, TownPolygon],
    _town_graph: nx.Graph,
    prefectures_to_hash: Sequence[str]) -> nx.Graph:

    graph = nx.Graph()
    for town in _town_polygons_dict.values():
        if town.name in EXCLUDED_TOWNS:
            continue
        neighbor_cities = set(
            itertools.chain([f"{town.prefecture} {town.city}"], _town_graph.neighbors(f"{town.prefecture} {town.city}")))
        candidate_towns = [t for t in town_polygons_dict.values() if f"{t.prefecture} {t.city}" in neighbor_cities]
        for town2 in candidate_towns:
            if town.polygon.intersects(town2.polygon):
                # print(f"{town.name} touches {town2.name}")
                graph.add_edge(town.name, town2.name)

    return graph


if __name__ == "__main__":
    st.set_page_config(layout="wide")

    prefectures = st.multiselect(
        label="検索対象の都道府県",
        options=TARGET_PREFECTURES,
        default=DEFAULT_TARGET_PREFECTURES,)
    if not prefectures:
        st.stop()

    # 各区画の輪郭を取得
    town_polygons = itertools.chain.from_iterable(
        load_town_data_from_gml_zip(f"../gml/経済センサス_活動調査_{pn}.zip") for pn in prefectures)
    # town_polygons = list(itertools.islice(town_polygons, 10))
    town_polygons = [p for p in town_polygons if p.town != "(町名無し)"]
    town_polygons_dict = {p.name: p for p in town_polygons}

    col_left, col_right = st.columns(2)
    with col_left:
        st.text("始点")
        pref_from = st.selectbox("都道府県", prefectures, key="pref_from")
        _cities_from_objs = [p for p in town_polygons if p.prefecture == pref_from]
        _cities_from = list(dict.fromkeys(p.city for p in _cities_from_objs))
        city_from = st.selectbox("市区町村", _cities_from, key="city_from")
        towns_from = list(dict.fromkeys(p.town for p in _cities_from_objs if p.city == city_from))
        town_from = st.selectbox("町名", towns_from, key="town_from", index=None)
    with col_right:
        st.text("終点")
        pref_to = st.selectbox("都道府県", prefectures, key="pref_to")
        _cities_to_objs = [p for p in town_polygons if p.prefecture == pref_to]
        _cities_to = list(dict.fromkeys(p.city for p in _cities_to_objs))
        city_to = st.selectbox("市区町村", _cities_to, key="city_to")
        towns_to = list(dict.fromkeys(p.town for p in _cities_to_objs if p.city == city_to))
        town_to = st.selectbox("町名", towns_to, key="town_to", index=None)
    if not town_from or not town_to:
        st.stop()

    # 市区町村単位の隣接グラフを構築
    city_graph = build_city_graph(prefectures)

    # 区画の隣接グラフを構築
    town_graph = build_town_graph(town_polygons_dict, city_graph, prefectures)
    with open("town_graph.pkl", "wb") as f:
        pickle.dump(town_graph, f)

    print("Finding shortest path...")
    node_from = f"{pref_from}_{city_from}_{town_from}"
    node_to = f"{pref_to}_{city_to}_{town_to}"
    # print(list(town_graph.neighbors(node_to)))
    shortest_path: list[str] = nx.shortest_path(
        town_graph,
        source=node_from,
        target=node_to)
    print(shortest_path)

    if False:
        print("Drawing graph...")
        fig = plt.figure(1, figsize=(50.0, 40.0))
        nx.draw(graph, with_labels=True, font_family="Meiryo")
        plt.savefig("graph.png")

    print("Drawing map...")

    shortest_path_polygons = [town_polygons_dict[p] for p in shortest_path]
    df_path_towns = pd.DataFrame({
        "town": shortest_path,
        "coordinates": [list(p.polygon.exterior.coords) for p in shortest_path_polygons],
    })
    # st.dataframe(df_path_towns)

    merged_polygon = shapely.unary_union([p.polygon for p in shortest_path_polygons])
    centroid: shapely.Point = merged_polygon.centroid

    layer = pydeck.Layer(
        "PolygonLayer",
        df_path_towns,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_scale=10,
        # line_width_min_pixels=0.1,
        get_polygon="coordinates",
        get_line_color=[255, 255, 255],
        get_fill_color=[0, 192, 0, 128],
        highlight_color=[255, 200, 0, 128],
        auto_highlight=True,
        pickable=True,
    )
    deck = pydeck.Deck(
        layers=[layer],
        initial_view_state=pydeck.ViewState(
            latitude=centroid.y,
            longitude=centroid.x,
            zoom=10.0,
            max_zoom=17,
            min_zoom=4,
            pitch=0,
            bearing=0,
        ),
        tooltip={"text": "{town}"},  # type: ignore
        height=MAP_HEIGHT,
        map_provider="carto",
        map_style="dark",
    )

    deck.to_html("pydeck.html")
    st.components.v1.html(deck.to_html(as_string=True), height=MAP_HEIGHT)

    #st.write(f"最短経路: \n{'\n'.join(f'1. {p.name}' for p in shortest_path)}")
