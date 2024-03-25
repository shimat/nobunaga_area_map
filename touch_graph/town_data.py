import itertools
import more_itertools
import os
import shapely  # type: ignore
import streamlit as st
import zipfile
from models import TownPolygon
from xml.etree import ElementTree as ET


NAMESPACES = {
    "gml": "http://www.opengis.net/gml",
    "fme": "http://www.safe.com/gml/fme",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink"
}


@st.cache_data
def load_town_data_from_gml_zip(file_name: str) -> list[TownPolygon]:
    with zipfile.ZipFile(file_name, 'r') as zf:
        gml_file_name = more_itertools.first_true(zf.namelist(), pred=lambda f: os.path.splitext(f)[1] == ".gml")
        if not gml_file_name:
            raise Exception(f"GML file not found in ZipFile '{file_name}'")
        with zf.open(gml_file_name, 'r') as file:
            tree = ET.parse(file)
            return load_town_data(tree)


def load_town_data(tree: ET.ElementTree) -> list[TownPolygon]:
    def get_elem_text(elem: ET.Element, path: str) -> str | None:
        child = elem.find(path, NAMESPACES)
        if child is None:
            return None
        return child.text

    result: list[TownPolygon] = []
    for feature_member in tree.findall("gml:featureMember", NAMESPACES):
        elem = feature_member[0]

        prefecture_name = get_elem_text(elem, "fme:PREF_NAME")
        city_name = get_elem_text(elem, "fme:CITY_NAME")
        if not prefecture_name or not city_name:
            continue
        if city_name == "境界未定地域":
            continue
        town_name = get_elem_text(elem, "fme:S_NAME")  # or "(町名無し)"
        if not town_name:
            continue

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
        polygon = shapely.Polygon(shell=polygons[0], holes=polygons[1:])
        result.append(TownPolygon(prefecture_name, city_name, town_name, polygon))

    return result
