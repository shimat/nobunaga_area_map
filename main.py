import pydeck
# import numpy as np
# import pandas as pd
import streamlit as st
from data_loader import load_data_from_gml, load_data_from_gml_zip, mod_data


df_org = load_data_from_gml_zip("gml/経済センサス_活動調査_北海道.zip")
#df_org.to_csv("hokkaido.csv")

#df_org = load_data_from_gml("gml/北海道.gml")
df_mod = mod_data(df_org)
df_org = df_org[:6000]

df_map = {"「信長の野望 出陣」のエリア": df_mod, "全町名": df_org}
#df_map = {"全町名": df_org}
for name, df in df_map.items():
    st.header(name)
    polygon_layer = pydeck.Layer(
        "PolygonLayer",
        df,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        line_width_scale=10,
        line_width_min_pixels=1,
        get_polygon="lonlat_coordinates",
        get_line_color=[255, 255, 255],
        get_fill_color=[0, 0, 0, 64],
        auto_highlight=True,
        pickable=True,
    )
    tooltip = "{address}\n面積: {area}㎡\n人口: {population}人, 世帯数: {household_count}"
    if name != "全町名":
        tooltip += "\n推定石高:{estimated_kokudaka}"
    deck = pydeck.Deck(
            layers=(polygon_layer, ),
            initial_view_state=pydeck.ViewState(
                # latitude=43.08,
                # longitude=141.35,
                # zoom=10.0,
                # latitude=43.08,
                # longitude=141.30,
                # zoom=12.0,
                latitude=42.99,
                longitude=141.46,
                zoom=12.0,
                max_zoom=16,
                pitch=0,
                bearing=0),
            tooltip={"text": tooltip})
    st.pydeck_chart(deck)
    st.dataframe(df)


st.markdown(
    """
-----

利用データ:
+ [地図で見る統計(統計GIS)](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200521&toukeiYear=2020&serveyId=A002005212020&datum=2011): 令和2年国勢調査町丁・字等別境界データ
""",  # noqa: E501
    unsafe_allow_html=True,
)
