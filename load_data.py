from xml.etree import ElementTree
import pandas as pd
import streamlit as st

# https://tm23forest.com/contents/python-jpgis-gml-dem-geotiff
NAMESPACES = {
    "gml": "http://www.opengis.net/gml",
    "fme": "http://www.safe.com/gml/fme",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xlink": "http://www.w3.org/1999/xlink"
}


@st.cache_data
def load_data(file_name: str) -> pd.DataFrame:
    tree = ElementTree.parse(file_name)
    # root = tree.getroot()

    # bounded_by = tree.find("gml:boundedBy", NAMESPACES)
    # st.write(bounded_by)

    prefecture_names: list[str] = []
    city_names: list[str] = []
    town_names: list[str] = []
    areas: list[float] = []
    perimeters: list[float] = []
    populations: list[int] = []
    household_counts: list[isinstance] = []
    lonlat_lists: list[list[list[list[float]]]] = []

    for index, feature_member in enumerate(tree.findall("gml:featureMember", NAMESPACES)):
        elem = feature_member[0]
        prefecture_names.append(elem.find("fme:PREF_NAME", NAMESPACES).text)
        city_names.append(elem.find("fme:CITY_NAME", NAMESPACES).text)
        town_names.append(elem.find("fme:S_NAME", NAMESPACES).text)
        areas.append(float(elem.find("fme:AREA", NAMESPACES).text))
        perimeters.append(float(elem.find("fme:PERIMETER", NAMESPACES).text))
        populations.append(int(elem.find("fme:JINKO", NAMESPACES).text))
        household_counts.append(int(elem.find("fme:SETAI", NAMESPACES).text))

        pos_list_elem = elem.find("gml:surfaceProperty//gml:Surface//gml:PolygonPatch//gml:exterior//gml:LinearRing//gml:posList", NAMESPACES)
        pos_list = [float(v) for v in pos_list_elem.text.split(" ")]
        lonlat_list = [[[pos_list[i*2+1], pos_list[i*2]] for i in range(len(pos_list) // 2)]]
        lonlat_lists.append(lonlat_list)

        #if index > 10:
        #    break

    data = {
        "prefecture_name": prefecture_names,
        "city_name": city_names,
        "town_name": town_names,
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
