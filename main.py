import streamlit as st
import pandas as pd
import numpy as np
import pydeck

# https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200521&toukeiYear=2020&serveyId=A002005212020&datum=2011
RAW_POS = [
        43.0664068559,
        141.3031330179,
        43.0664134668,
        141.3031414525,
        43.0665145283,
        141.3032688165,
        43.0666760300,
        141.3034675765,
        43.0671080134,
        141.3027055331,
        43.0672086586,
        141.3025277709,
        43.0673160826,
        141.3023362839,
        43.0675358492,
        141.3019444058,
        43.0677092268,
        141.3015984197,
        43.0678239368,
        141.3013697905,
        43.0681751152,
        141.3006692061,
        43.0679493516,
        141.3003970024,
        43.0677837595,
        141.3001974462,
        43.0675522410,
        141.2999184297,
        43.0673082003,
        141.3003759172,
        43.0671890878,
        141.3005992441,
        43.0670683128,
        141.3008087813,
        43.0668805738,
        141.3011526854,
        43.0666780937,
        141.3015170528,
        43.0666561808,
        141.3015545135,
        43.0664769906,
        141.3018864821,
        43.0660470295,
        141.3026797627,
        43.0664068559,
        141.3031330179]

POS = [[[RAW_POS[i*2+1], RAW_POS[i*2]] for i in range(len(RAW_POS) // 2)]]
df = pd.DataFrame()
df["coordinates"] = POS
st.write(POS)

polygon_layer = pydeck.Layer(
    "PolygonLayer",
    df,
    stroked=True,
    filled=True,
    extruded=False,
    wireframe=True,
    line_width_scale=10,
    line_width_min_pixels=1,
    get_polygon="coordinates",
    get_line_color=[255, 255, 255],
    get_fill_color=[0, 0, 0, 128],
    pickable=True,
)
deck = pydeck.Deck(
        layers=(polygon_layer, ),
        initial_view_state=pydeck.ViewState(
            latitude=43.08,
            longitude=141.35,
            zoom=10.0,
            max_zoom=16,
            pitch=0,
            bearing=0),
        tooltip={"html": "Hello"})
st.pydeck_chart(deck)
