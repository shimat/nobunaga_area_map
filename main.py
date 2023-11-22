import pydeck
import streamlit as st
from area_loader import load_area_data
from town_loader import load_town_data_from_gml_zip, mod_data
from municipality_loader import load_municipality_data_zip
from city_list import CITY_NAMES
import time


st.set_page_config(
    page_title="「信長の野望 出陣」エリア別石高の可視化",
    page_icon="🗾",
    layout="wide")
st.header("「信長の野望 出陣」エリア別石高の可視化")

col_left, col_right = st.columns(2)

prefecture_name = col_left.selectbox(
    label="都道府県",
    options=CITY_NAMES.keys(),
)
city_name: str | None = col_right.selectbox(
    label="市区町村",
    options=CITY_NAMES[prefecture_name],
    index=None
)

map_type = st.radio(
    label="マップ種別",
    options=("「信長の野望 出陣」の各エリア", "全町名"),
    horizontal=True,)

show_municipality_borders = st.checkbox(
    label="市区町村境界を表示",
    value=True,
    disabled=(city_name != "(全体)"))


if city_name:
    t = time.perf_counter()
    df_org = load_town_data_from_gml_zip(f"gml/経済センサス_活動調査_{prefecture_name}.zip")
    print(f"DataFrame Load Time = {time.perf_counter() - t}s")

    t = time.perf_counter()
    area_data = load_area_data(prefecture_name)
    print(f"AreaData Load Time = {time.perf_counter() - t}s")

    t = time.perf_counter()
    if city_name == "(全体)":
        df_target = df_org[df_org["pref_city"].isin(area_data.areas.keys())].copy()
        correspondences = area_data.get_all_correspondences()
        df_mod = mod_data(df_target, correspondences, prefecture_name)
        view_state = area_data.view_state
    else:
        df_target = df_org[df_org["city_name"] == city_name].copy()
        pref_city = f"{prefecture_name} {city_name}"
        correspondences = area_data.get_one_area_correspondences(pref_city)
        df_mod = mod_data(df_target, correspondences, pref_city)
        view_state = area_data.areas[pref_city].view_state
    print(f"DataFrame Mod Time = {time.perf_counter() - t}s")
    # df_org.to_csv("hokkaido.csv", columns=["prefecture_name", "address", "area",], index=False, encoding="utf-8-sig")
    # st.write(df_org.memory_usage(deep=True))

    df_target["area_str"] = df_org["area"].apply(lambda x: "{:,.0f}".format(x))
    df_mod["area_str"] = df_mod["area"].apply(lambda x: "{:,.0f}".format(x))


    match map_type:
        case "「信長の野望 出陣」の各エリア":
            df_show = df_mod
            fill_color = "fill_color"
            tooltip = "{city_name} {area_name}{sub_towns_suffix}\n面積: {area_str}㎡\n推定石高:{kokudaka}"
        case "全町名":
            df_show = df_target
            fill_color = [64, 64, 256, 64]
            tooltip = "{city_name} {town_name}\n面積: {area_str}㎡"

    layers: list[pydeck.Layer] = []
    layers.append(pydeck.Layer(
        "PolygonLayer",
        df_show,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=True,
        line_width_scale=20,
        # line_width_min_pixels=0.1,
        get_polygon="lonlat_coordinates",
        get_line_color=[255, 255, 255],
        get_fill_color=fill_color,
        highlight_color=[255, 200, 0, 128],
        auto_highlight=True,
        pickable=True,
    ))
    if show_municipality_borders and city_name == "(全体)":
        t = time.perf_counter()
        df_municipalities = load_municipality_data_zip(
            prefecture_name,
            set(CITY_NAMES[prefecture_name]))
        print(f"Municipality Load Time = {time.perf_counter() - t}s")
        layers.append(pydeck.Layer(
            "PolygonLayer",
            df_municipalities,
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
        ))
    deck = pydeck.Deck(
        layers=layers,
        initial_view_state=pydeck.ViewState(
            latitude=view_state.latitude,
            longitude=view_state.longitude,
            zoom=view_state.zoom,
            max_zoom=16,
            pitch=0,
            bearing=0,
        ),
        tooltip={"text": tooltip},
        height=600,
        map_provider="carto",
        map_style="dark",
    )

    # st.pydeck_chart(deck)
    st.components.v1.html(deck.to_html(as_string=True), height=600)

    address_label = "住所" if (map_type == "全町名") else "エリア名"
    st.dataframe(
        df_show,
        hide_index=True,
        use_container_width=True,
        column_config={
            "prefecture_name": st.column_config.TextColumn("都道府県", width="small"),
            "city_name": st.column_config.TextColumn("市区町村", width="small"),
            "area_name": st.column_config.TextColumn("エリア名", width="small"),
            "address": address_label,
            "area": st.column_config.NumberColumn("面積[㎡]", step="0"),
            "kokudaka": st.column_config.NumberColumn("推定石高", format="%.2f"),
            "sub_towns": st.column_config.ListColumn("含む町名"),
            "sub_towns_suffix": None,
            "lonlat_coordinates": st.column_config.ListColumn("輪郭座標"),
            "pref_city": None,
            "area_str": None,
            "own": st.column_config.TextColumn("領有", width="small", help="0:未踏, 1:直接来訪, 2:遠征で獲得"),
            "fill_color": None,
        },
    )

st.markdown(
    """
-----

利用データ:
+ [e-Stat 統計で見る日本](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200553&toukeiYear=2016&serveyId=A002005532016&coordsys=1&format=gml&datum=2011): 経済センサス－活動調査（総務省・経済産業省）/ 2016年 / 小地域（町丁・大字）（JGD2011）
+ [『国土数値情報「⾏政区域データ」 (N03)』（国土交通省）](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_1.html)
""",  # noqa: E501
    unsafe_allow_html=True,
)

