from functools import reduce
import pandas as pd
import pydeck
import re
import streamlit as st
import time
from src.area_loader import AllAreasData, load_area_data, load_region_data
from src.enums import MapType, ColorCoding
from src.town_loader import load_town_data_from_gml_zip, mod_data
from src.municipality_loader import load_municipality_borders_from_json, load_municipality_borders_from_json_multi
from src.city_list import ORG_CITY_NAMES, CITY_NAMES, SUBPREFECTURES


st.set_page_config(
    page_title="「信長の野望 出陣」エリア別石高の可視化",
    page_icon="🗾",
    layout="wide")
st.header("「信長の野望 出陣」エリア別石高の可視化")

col_left, col_right = st.columns(2)

prefecture_name: str = col_left.selectbox(
    label="都道府県",
    options=CITY_NAMES.keys(),
) or ""
if not prefecture_name:
    st.warning("都道府県を選択してください")
    st.stop()
city_name: str = col_right.selectbox(
    label="市区町村",
    options=CITY_NAMES[prefecture_name],
    index=None,
    disabled=prefecture_name.startswith("（")
) or ""
if prefecture_name.startswith("（"):
    city_name = "（全体）"
else:
    city_name = re.sub(r"^\d+: ", "", city_name)


with st.expander("オプション"):
    col1, col2 = st.columns(2)
    with col1:
        map_type = st.radio(
            label="マップ種別",
            options=[t.value for t in MapType],
            horizontal=True,)
        color_coding_options = [t.value for t in ColorCoding]
        if map_type == MapType.ALL_TOWNS:
            color_coding_options.remove(ColorCoding.OWNERSHIP)
        color_coding = st.radio(
            label="色分け",
            options=color_coding_options,
            horizontal=True,)
        show_municipality_borders = st.checkbox(
            label="市区町村境界を表示",
            value=True,
            disabled=(not city_name.startswith("（")))
    with col2:
        bastion_coordinates: str | None = st.text_input(
            "拠点の緯度・経度 (入力した場合に半径50kmの円を表示)", value=None, placeholder="例: 43.0687, 141.3507")
        bastion_latitude, bastion_longitude = None, None
        if bastion_coordinates:
            try:
                bastion_latitude, bastion_longitude = map(float, bastion_coordinates.split(","))
            except:
                pass

        map_height: float = st.number_input("Map高さ(px)", value=600, max_value=6000, min_value=100, step=10)

if city_name:
    t = time.perf_counter()
    # 地方全体モード
    if prefecture_name.startswith("（"):
        df_org = pd.concat([
            load_town_data_from_gml_zip(f"gml/経済センサス_活動調査_{pn}.zip")
            for pn in ORG_CITY_NAMES[prefecture_name]])
    # 1つの都道府県モード
    else:
        df_org = load_town_data_from_gml_zip(f"gml/経済センサス_活動調査_{prefecture_name}.zip")
    print(f"DataFrame Load Time = {time.perf_counter() - t:.3f}s")

    t = time.perf_counter()
    if prefecture_name.startswith("（"):
        area_data: AllAreasData = load_region_data(prefecture_name, ORG_CITY_NAMES[prefecture_name])
    else:
        area_data: AllAreasData = load_area_data(prefecture_name)
    print(f"AreaData Load Time = {time.perf_counter() - t:.3f}s")

    t = time.perf_counter()
    if city_name == "（全体）" or prefecture_name.startswith("（"):
        df_target = df_org[df_org["pref_city"].isin(area_data.areas.keys())].copy()
        correspondences = area_data.get_all_correspondences()
        df_mod = mod_data(df_target, correspondences, color_coding, prefecture_name)
        view_state = area_data.view_state
        st.dataframe(df_target)
        st.write(view_state)
    elif city_name.startswith("（"):  # 北海道等の各ブロック
        target_pref_cities = {f"{prefecture_name} {city_name}" for city_name in SUBPREFECTURES[prefecture_name][city_name]}
        df_target = df_org[df_org["pref_city"].isin(target_pref_cities)].copy()
        correspondences = area_data.get_multiple_areas_correspondences(target_pref_cities)
        subpref_identifier = f"{prefecture_name} {city_name}"
        df_mod = mod_data(df_target, correspondences, color_coding, subpref_identifier)
        view_state = area_data.areas[subpref_identifier].view_state
    else:
        df_target = df_org[df_org["city_name"] == city_name].copy()
        pref_city = f"{prefecture_name} {city_name}"
        correspondences = area_data.get_one_area_correspondences(pref_city)
        df_mod = mod_data(df_target, correspondences, color_coding, pref_city)
        view_state = area_data.areas[pref_city].view_state
    print(f"DataFrame Mod Time = {time.perf_counter() - t:.3f}s")
    # df_org.to_csv("hokkaido.csv", columns=["prefecture_name", "address", "area",], index=False, encoding="utf-8-sig")
    # st.write(df_org.memory_usage(deep=True))

    df_target["area_str"] = df_target["area"].apply(lambda x: "{:,.0f}".format(x))
    df_mod["area_str"] = df_mod["area"].apply(lambda x: "{:,.0f}".format(x))

    fill_color: str | list[int]
    df_show: pd.DataFrame
    match map_type:
        case MapType.NOBUNAGA_AREAS:
            df_show = df_mod
            line_width_scale = 15
            fill_color = "fill_color"
            tooltip = "{city_name} {area_name}{sub_towns_suffix}\n面積: {area_str}㎡\n石高:{kokudaka_str}"
        case MapType.ALL_TOWNS:
            df_show = df_target
            line_width_scale = 10
            if color_coding == ColorCoding.RANDOM:
                fill_color = "fill_color"
            else:
                fill_color = [64, 64, 256, 64]
            tooltip = "{city_name} {town_name}\n面積: {area_str}㎡"
        case _:
            raise Exception(f"Invalid map_type '{map_type}'")

    layers: list[pydeck.Layer] = []
    layers.append(pydeck.Layer(
        "PolygonLayer",
        df_show,
        stroked=True,
        filled=True,
        extruded=False,
        wireframe=False,
        line_width_scale=line_width_scale,
        # line_width_min_pixels=0.1,
        get_polygon="lonlat_coordinates",
        get_line_color=[255, 255, 255],
        get_fill_color=fill_color,
        highlight_color=[255, 200, 0, 128],
        auto_highlight=True,
        pickable=True,
    ))
    if show_municipality_borders and city_name.startswith("（"):
        t = time.perf_counter()
        if prefecture_name.startswith("（"):
            df_municipalities = load_municipality_borders_from_json_multi(
                {pn: set(ORG_CITY_NAMES[pn]) for pn in ORG_CITY_NAMES[prefecture_name]})
        else:
            if city_name == "（全体）":
                target_cities = ORG_CITY_NAMES[prefecture_name]
            else:
                target_cities = SUBPREFECTURES[prefecture_name][city_name]
            df_municipalities = load_municipality_borders_from_json(
                prefecture_name,
                set(target_cities))
        print(f"Municipality Load Time = {time.perf_counter() - t:.3f}s")
        layers.append(pydeck.Layer(
            "PolygonLayer",
            df_municipalities,
            stroked=True,
            filled=False,
            extruded=False,
            wireframe=False,
            line_width_scale=60,
            line_width_min_pixels=1,
            get_polygon="lonlat_coordinates",
            get_line_color=[255, 255, 255],
            auto_highlight=False,
            pickable=False,
        ))
    # 遠征可能範囲の表示
    if bastion_latitude and bastion_longitude:
        df_circle = pd.DataFrame({
            "coordinates": [[bastion_longitude, bastion_latitude]] * 2,
            "radius": [50000, 300],
            "fill_color": [
                [255, 140, 0, 32],
                [255, 0, 0, 255],
            ],
        })
        layers.append(pydeck.Layer(
            "ScatterplotLayer",
            df_circle,
            pickable=False,
            stroked=True,
            filled=True,
            #radius_units="meters",
            line_width_min_pixels=1,
            get_position="coordinates",
            get_radius="radius",
            get_fill_color="fill_color",
            get_line_color=[255, 255, 255],
        ))
    deck = pydeck.Deck(
        layers=layers,
        initial_view_state=pydeck.ViewState(
            latitude=view_state.latitude,
            longitude=view_state.longitude,
            zoom=view_state.zoom,
            max_zoom=17,
            min_zoom=4,
            pitch=0,
            bearing=0,
        ),
        tooltip={"text": tooltip},
        height=map_height,
        map_provider="carto",
        map_style="dark",
    )

    # st.pydeck_chart(deck)
    st.components.v1.html(deck.to_html(as_string=True), height=map_height)

    address_label = "住所" if (map_type == MapType.ALL_TOWNS) else "エリア名"
    st.dataframe(
        df_show,
        hide_index=True,
        use_container_width=True,
        column_config={
            "prefecture_name": st.column_config.TextColumn("都道府県", width="small"),
            "city_name": st.column_config.TextColumn("市区町村"),
            "area_name": st.column_config.TextColumn("エリア名"),
            "town_name": st.column_config.TextColumn("町丁"),
            "address": address_label,
            "area": st.column_config.NumberColumn("面積[㎡]", step="0", width="small"),
            "kokudaka": st.column_config.NumberColumn("石高", format="%.2f", width="small"),
            "kokudaka_str": None,
            "is_observed_kokudaka": st.column_config.CheckboxColumn("実測石高か", width="small", help="石高が実測値か、回帰分析による推定値かのフラグ"),
            # "sub_towns": st.column_config.ListColumn("含む町名"),
            "sub_towns_suffix": None,
            "lonlat_coordinates": None,
            "pref_city": None,
            "area_str": None,
            "own": st.column_config.TextColumn("領有", width="small", help="0:未踏, 1:直接来訪, 2:遠征で獲得"),
            "fill_color": None,
        },
    )

    if map_type != MapType.ALL_TOWNS.value:
        df_uniq = df_show.drop_duplicates(subset=("city_name", "area_name"))
        df_own = df_uniq[df_uniq["own"] != 0]
        kokudaka_all_sum = df_uniq["kokudaka"].sum()
        kokudaka_own_sum = df_own["kokudaka"].sum()
        st.write(f"推定石高合計: {kokudaka_own_sum:.2f}石 / {kokudaka_all_sum:.2f}石 ({kokudaka_own_sum/kokudaka_all_sum:.1%})")


st.markdown(
    """
-----

利用データ:
+ [e-Stat 統計で見る日本](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200553&toukeiYear=2016&serveyId=A002005532016&coordsys=1&format=gml&datum=2011): 経済センサス－活動調査（総務省・経済産業省）/ 2016年 / 小地域（町丁・大字）（JGD2011）
+ [『国土数値情報「⾏政区域データ」 (N03)』（国土交通省）](https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v3_1.html)
""",  # noqa: E501
    unsafe_allow_html=True,
)

