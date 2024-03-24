import itertools
from pathlib import Path
import more_itertools
import os
import pickle
import shapely # type: ignore
import zipfile
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import pydeck
from typing import Iterable, NamedTuple
from xml.etree import ElementTree as ET
import streamlit as st


NAMESPACES = {
    "gml": "http://www.opengis.net/gml",
    "fme": "http://www.safe.com/gml/fme",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink"
}


class TownPolygon(NamedTuple):
    city: str
    town: str
    polygon: shapely.Polygon

    @property
    def name(self) -> str:
        return f"{self.city}_{self.town}"

    def __str__(self) -> str:
        return self.name


def load_town_data_from_gml_zip(file_name: str) -> Iterable[TownPolygon]:
    with zipfile.ZipFile(file_name, 'r') as zf:
        gml_file_name = more_itertools.first_true(zf.namelist(), pred=lambda f: os.path.splitext(f)[1] == ".gml")
        if not gml_file_name:
            raise Exception(f"GML file not found in ZipFile '{file_name}'")
        with zf.open(gml_file_name, 'r') as file:
            tree = ET.parse(file)
            return load_town_data(tree)


def load_town_data(tree: ET.ElementTree) -> Iterable[TownPolygon]:
    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]

        prefecture_name = get_elem_text(elem, "fme:PREF_NAME")
        city_name = get_elem_text(elem, "fme:CITY_NAME")
        if not prefecture_name or not city_name:
            continue
        town_name = get_elem_text(elem, "fme:S_NAME") or "(町名無し)"

        contour_elements = itertools.chain(
              elem.findall("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior", NAMESPACES),
              elem.findall("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:interior", NAMESPACES))
        polygons: list[list[list[float]]] = []
        for contour_elem in contour_elements:
            pos_list_elem = contour_elem.find("gml:LinearRing//gml:posList", NAMESPACES)
            if pos_list_elem is None or pos_list_elem.text is None:
                continue
            pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
            lonlat_list = [[pos_list[i*2+1], pos_list[i*2]] for i in range(len(pos_list) // 2)]
            polygons.append(lonlat_list)
        polygon = shapely.geometry.Polygon(shell=polygons[0], holes=polygons[1:])

        yield TownPolygon(city_name, town_name, polygon)


def get_elem_text(elem: ET.Element, path: str) -> str | None:
    child = elem.find(path, NAMESPACES)
    if child is None:
        return None
    return child.text


if __name__== "__main__":
    st.set_page_config(layout="wide")

    town_polygons = load_town_data_from_gml_zip("../gml/経済センサス_活動調査_東京都.zip")
    # town_polygons = list(itertools.islice(town_polygons, 10))
    town_polygons = [p for p in town_polygons if p.city.endswith("区")]
    town_polygons_dict = {p.name: p for p in town_polygons}
    print(town_polygons)


    graph_path = Path("graph.pkl")
    if graph_path.exists():
        print("Loading graph from cache...")
        graph: nx.Graph = pickle.load(graph_path.open('rb'))
    else:
        graph = nx.Graph()
        EXCLUDED_TOWNS = {"千代田区_皇居外苑", "千代田区_千代田", "港区_元赤坂２丁目",}
        for a, b in itertools.combinations(town_polygons_dict.values(), 2):
            if a.name in EXCLUDED_TOWNS or b.name in EXCLUDED_TOWNS:
                continue
            if a.polygon.touches(b.polygon):
                print(f"{a.name} touches {b.name}")
                graph.add_edge(a, b)
            else:
                graph.add_node(a)
                graph.add_node(b)
        pickle.dump(graph, open('graph.pkl', 'wb'))

    print("Finding shortest path...")
    node_from = town_polygons_dict["千代田区_丸の内１丁目"]
    node_to = town_polygons_dict["大田区_田園調布本町"]
    shortest_path: list[TownPolygon] = nx.shortest_path(
        graph,
        source=node_from,
        target=node_to)
    print([p.name for p in shortest_path])

    if False:
        print("Drawing graph...")
        fig = plt.figure(1, figsize=(50.0, 40.0))
        nx.draw(graph, with_labels=True, font_family="Meiryo")
        plt.savefig("graph.png")

    print("Drawing map...")
    df_path_towns = pd.DataFrame({
        "town": [p.name for p in shortest_path],
        "coordinates": [list(p.polygon.exterior.coords) for p in shortest_path],
    })
    # st.dataframe(df_path_towns)

    MAP_HEIGHT = 1000
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
            latitude=35.681,
            longitude=139.765,
            zoom=11.0,
            max_zoom=17,
            min_zoom=4,
            pitch=0,
            bearing=0,
        ),
        tooltip={"text": "{town}"}, # type: ignore
        height=MAP_HEIGHT,
        map_provider="carto",
        map_style="dark",
    )

    deck.to_html("pydeck.html")
    st.components.v1.html(deck.to_html(as_string=True), height=MAP_HEIGHT)

    st.write(f"最短経路: \n{'\n'.join(f'1. {p.name}' for p in shortest_path)}")
