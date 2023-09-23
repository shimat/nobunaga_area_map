import pydeck
import streamlit as st
from data_loader import load_data_from_gml_zip, load_area_data, mod_data
import time


st.set_page_config(page_title="「信長の野望 出陣」エリア別石高の可視化")

t = time.perf_counter()
df_org = load_data_from_gml_zip("gml/経済センサス_活動調査_北海道.zip")
print(f"DataFrame Load Time = {time.perf_counter() - t}s")

city_name = st.selectbox(
    label="市区町村",
    options=(
        "北海道",
        "札幌市南区",
        "札幌市手稲区",
        "札幌市豊平区",
        "札幌市清田区",
        "虻田郡京極町",
    ),
)

t = time.perf_counter()
area_data = load_area_data()
print(f"AreaData Load Time = {time.perf_counter() - t}s")

t = time.perf_counter()
if city_name == "北海道":
    df_target = df_org[df_org["city_name"].isin(area_data.areas.keys())].copy()
    df_mod = mod_data(df_target, area_data.get_all_correspondences())
    view_state = area_data.view_state
else:
    df_target = df_org[df_org["city_name"] == city_name].copy()
    df_mod = mod_data(df_target, area_data.areas[city_name].correspondences)
    view_state = area_data.areas[city_name].view_state
print(f"DataFrame Mod Time = {time.perf_counter() - t}s")
# df_org.to_csv("hokkaido.csv", columns=["prefecture_name", "address", "area",], index=False, encoding="utf-8-sig")
# st.write(df_org.memory_usage(deep=True))

df_target["area_str"] = df_org["area"].apply(lambda x: "{:,.0f}".format(x))
df_mod["area_str"] = df_mod["area"].apply(lambda x: "{:,.0f}".format(x))


df_map = {"「信長の野望 出陣」の各エリア": df_mod, "全町名": df_target}
tabs = dict(zip(df_map.keys(), st.tabs(df_map.keys())))

for name, df in df_map.items():
    with tabs[name]:
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
            highlight_color=[0, 0, 255, 128],
            auto_highlight=True,
            pickable=True,
        )
        tooltip = "{address}\n面積: {area_str}㎡"
        if name != "全町名":
            tooltip += "\n推定石高:{kokudaka}"
        deck = pydeck.Deck(
            layers=(polygon_layer,),
            initial_view_state=pydeck.ViewState(
                latitude=view_state.latitude,
                longitude=view_state.longitude,
                zoom=view_state.zoom,
                max_zoom=16,
                pitch=0,
                bearing=0,
            ),
            tooltip={"text": tooltip},
        )
        st.pydeck_chart(deck)

        address_label = "住所" if (name == "全町名") else "エリア名"
        st.dataframe(
            df,
            hide_index=True,
            column_config={
                "prefecture_name": st.column_config.TextColumn("都道府県", width="small"),
                "address": address_label,
                "area": st.column_config.NumberColumn("面積[㎡]", step="0"),
                "kokudaka": st.column_config.NumberColumn("推定石高", format="%.2f"),
                "sub_addresses": st.column_config.ListColumn("含む町名"),
                "lonlat_coordinates": st.column_config.ListColumn("輪郭座標"),
                "city_name": None,
                "area_str": None,
            },
        )


st.markdown(
    """
-----

利用データ:
+ [e-Stat 統計で見る日本](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200553&toukeiYear=2016&serveyId=A002005532016&coordsys=1&format=gml&datum=2011): 経済センサス－活動調査（総務省・経済産業省）/ 2016年 / 小地域（町丁・大字）（JGD2011）
""",  # noqa: E501
    unsafe_allow_html=True,
)
