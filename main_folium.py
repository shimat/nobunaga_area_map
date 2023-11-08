import folium
import streamlit as st
from streamlit_folium import st_folium
from area_loader import load_area_data
from town_loader import load_town_data_from_gml_zip, mod_data
from municipality_loader import load_municipality_geojson_simplified
import time


st.set_page_config(
    page_title="「信長の野望 出陣」エリア別石高の可視化", 
    page_icon="🗾",
    layout="wide")
st.header("「信長の野望 出陣」エリア別石高の可視化")

t = time.perf_counter()
df_org = load_town_data_from_gml_zip("gml/経済センサス_活動調査_北海道.zip")
print(f"DataFrame Load Time = {time.perf_counter() - t}s")

t = time.perf_counter()
area_data = load_area_data()
print(f"AreaData Load Time = {time.perf_counter() - t}s")

# t = time.perf_counter()
# df_municipalities = load_municipality_data_zip("北海道")
# print(f"Municipality Load Time = {time.perf_counter() - t}s")

city_name = st.selectbox(
    label="市区町村",
    options=(
        "北海道",
        "札幌市中央区",
        "札幌市北区",
        "札幌市東区",
        "札幌市南区",
        "札幌市白石区",
        "札幌市厚別区",
        "札幌市西区",
        "札幌市手稲区",
        "札幌市豊平区",
        "札幌市清田区",
        "函館市",
        "小樽市",
        "石狩市",
        "亀田郡七飯町",
        "樺戸郡月形町",
        "虻田郡京極町",
    ),
)


map = folium.Map(
    location=(43.062, 141.354),
    tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png",
    attr="Stadia.AlidadeSmoothDark",
    zoom_start=7,
    prefer_canvas=True,)

t = time.perf_counter()
geojson = load_municipality_geojson_simplified("北海道")
folium.GeoJson(
    geojson,
    # smooth_factor=2,
    style_function=lambda feature: {
        "color": "white",
        "weight": 1,
        "fillOpacity": 0.0,
    }).add_to(map)
print(f"Municipality Load Time = {time.perf_counter() - t}s")

event: dict = st_folium(
    map,
    use_container_width=True,
    returned_objects=(
        "last_clicked",
        "last_object_clicked",
        "last_object_clicked_tooltip",
        "last_object_clicked_popup"))
print(event)


t = time.perf_counter()
if city_name == "北海道":
    df_target = df_org[df_org["pref_city"].isin(area_data.areas.keys())].copy()
    correspondences = area_data.get_all_correspondences()
    df_mod = mod_data(df_target, correspondences)
    view_state = area_data.view_state
else:
    df_target = df_org[df_org["city_name"] == city_name].copy()
    pref_city = f"北海道 {city_name}"
    correspondences = area_data.get_one_area_correspondences(pref_city)
    df_mod = mod_data(df_target, correspondences)
    view_state = area_data.areas[pref_city].view_state
print(f"DataFrame Mod Time = {time.perf_counter() - t}s")
# df_org.to_csv("hokkaido.csv", columns=["prefecture_name", "address", "area",], index=False, encoding="utf-8-sig")
# st.write(df_org.memory_usage(deep=True))

df_target["area_str"] = df_org["area"].apply(lambda x: "{:,.0f}".format(x))
df_mod["area_str"] = df_mod["area"].apply(lambda x: "{:,.0f}".format(x))


df_map = {"「信長の野望 出陣」の各エリア": df_mod, "全町名": df_target}
tabs = dict(zip(df_map.keys(), st.tabs(df_map.keys())))

for name, df in df_map.items():
    with tabs[name]:

        if name == "全町名":
            fill_color = [0, 0, 0, 64]
            tooltip = "{city_name} {town_name}\n面積: {area_str}㎡"
        else:
            fill_color = "fill_color"
            tooltip = "{city_name} {area_name}\n面積: {area_str}㎡\n推定石高:{kokudaka}"

        # st.pydeck_chart(deck)
        # st.components.v1.html(deck.to_html(as_string=True), height=600)
        # from streamlit_deckgl import st_deckgl
        # value = st_deckgl(deck, key=name, events=[])
        # print(f"{value=}")

        address_label = "住所" if (name == "全町名") else "エリア名"
        st.dataframe(
            df,
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
""",  # noqa: E501
    unsafe_allow_html=True,
)
