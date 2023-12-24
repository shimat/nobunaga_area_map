CITY_NAMES = {
    "北海道": (
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
        "旭川市",
        "夕張市",
        "岩見沢市",
        "苫小牧市",
        "美唄市",
        "芦別市",
        "江別市",
        "赤平市",
        "士別市",
        "三笠市",
        "千歳市",
        "滝川市",
        "砂川市",
        "歌志内市",
        "深川市",
        "登別市",
        "恵庭市",
        "伊達市",
        "北広島市",
        "石狩市",
        "北斗市",
        "松前郡松前町",
        "松前郡福島町",
        "上磯郡知内町",
        "上磯郡木古内町",
        "亀田郡七飯町",
        "茅部郡鹿部町",
        "茅部郡森町",
        "二海郡八雲町",
        "山越郡長万部町",
        "檜山郡上ノ国町",
        "檜山郡江差町",
        "檜山郡厚沢部町",
        "爾志郡乙部町",
        "島牧郡島牧村",
        "虻田郡倶知安町",
        "虻田郡京極町",
        "虻田郡喜茂別町",
        "虻田郡留寿都村",
        "余市郡余市町",
        "余市郡仁木町",
        "余市郡赤井川村",
        "岩内郡共和町",
        "岩内郡岩内町",
        "古宇郡泊村",
        "古宇郡神恵内村",
        "積丹郡積丹町",
        "古平郡古平町",
        "磯谷郡蘭越町",
        "寿都郡寿都町",
        "寿都郡黒松内町",
        "白老郡白老町",
        "有珠郡壮瞥町",
        "虻田郡洞爺湖町",
        "虻田郡豊浦町",
        "勇払郡安平町",
        "勇払郡厚真町",
        "石狩郡当別町",
        "石狩郡新篠津村",
        "樺戸郡月形町",
        "樺戸郡浦臼町",
        "樺戸郡新十津川町",
        "空知郡南幌町",
        "空知郡奈井江町",
        "空知郡上砂川町",
        "空知郡中富良野町",
        "空知郡上富良野町",
        "夕張郡長沼町",
        "夕張郡栗山町",
        "夕張郡由仁町",
        "雨竜郡雨竜町",
        "雨竜郡北竜町",
        "雨竜郡妹背牛町",
        "雨竜郡秩父別町",
        "雨竜郡沼田町",
        "雨竜郡幌加内町",
        "上川郡美瑛町",
        "上川郡東神楽町",
        "上川郡東川町",
        "上川郡鷹栖町",
        "上川郡比布町",
        "上川郡当麻町",
        "上川郡愛別町",
        "上川郡上川町",
        "上川郡和寒町",
        "上川郡剣淵町",
    ),
    "青森県": (
        "むつ市",
        "下北郡大間町",
        "下北郡風間浦村",
        "下北郡佐井村",
        "下北郡東通村",
    ),
    "福島県": (
        "須賀川市",
        "田村市",
    ),
    "東京都": (
        "千代田区",
        "中央区",
        "港区",
        "新宿区",
        "文京区",
        "台東区",
        "墨田区",
        "江東区",
        "品川区",
        "目黒区",
        "大田区",
        "世田谷区",
        "渋谷区",
        "中野区",
        "杉並区",
        "豊島区",
        "北区",
        "荒川区",
        "板橋区",
        "練馬区",
        "足立区",
        "葛飾区",
        "江戸川区",
    ),
    "神奈川県": (
        "川崎市川崎区",
        "川崎市幸区",
        "川崎市中原区",
        "川崎市高津区",
        "川崎市宮前区",
        "川崎市多摩区",
        "川崎市麻生区",
    ),
}


for key, value in CITY_NAMES.items():
    CITY_NAMES[key] = ("(全体)",) + value
