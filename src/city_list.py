ORG_REGIONS: dict[str, tuple[str, ...]] = {
    "北海道": ("北海道",),
    # "東北": ("青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"),
    "東北": ("青森県",),
    "関東": ("東京都", "神奈川県", "千葉県", "埼玉県", "茨城県", "栃木県", "群馬県"),
    "!一都三県": ("東京都", "神奈川県", "千葉県", "埼玉県"),
}

REGIONS_TO_SELECT = list(ORG_REGIONS.keys())
REGIONS_TO_SELECT.remove("!一都三県")

ORG_CITY_NAMES: dict[str, tuple[str, ...]] = {
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
        "室蘭市",
        "釧路市",
        "帯広市",
        "北見市",
        "夕張市",
        "岩見沢市",
        "網走市",
        "留萌市",
        "苫小牧市",
        "稚内市",
        "美唄市",
        "芦別市",
        "江別市",
        "赤平市",
        "紋別市",
        "士別市",
        "名寄市",
        "三笠市",
        "根室市",
        "千歳市",
        "滝川市",
        "砂川市",
        "歌志内市",
        "深川市",
        "富良野市",
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
        "瀬棚郡今金町",
        "久遠郡せたな町",
        "奥尻郡奥尻町",
        "島牧郡島牧村",
        "虻田郡倶知安町",
        "虻田郡京極町",
        "虻田郡喜茂別町",
        "虻田郡留寿都村",
        "虻田郡真狩村",
        "虻田郡ニセコ町",
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
        "勇払郡むかわ町",
        "沙流郡平取町",
        "沙流郡日高町",
        "新冠郡新冠町",
        "日高郡新ひだか町",
        "浦河郡浦河町",
        "様似郡様似町",
        "幌泉郡えりも町",
        "石狩郡当別町",
        "石狩郡新篠津村",
        "樺戸郡月形町",
        "樺戸郡浦臼町",
        "樺戸郡新十津川町",
        "空知郡南幌町",
        "空知郡奈井江町",
        "空知郡上砂川町",
        "夕張郡長沼町",
        "夕張郡栗山町",
        "夕張郡由仁町",
        "雨竜郡雨竜町",
        "雨竜郡北竜町",
        "雨竜郡妹背牛町",
        "雨竜郡秩父別町",
        "雨竜郡沼田町",
        "雨竜郡幌加内町",
        "勇払郡占冠村",
        "空知郡南富良野町",
        "空知郡中富良野町",
        "空知郡上富良野町",
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
        "上川郡下川町",
        "中川郡美深町",
        "中川郡音威子府村",
        "中川郡中川町",
        "増毛郡増毛町",
        "留萌郡小平町",
        "苫前郡苫前町",
        "苫前郡羽幌町",
        "苫前郡初山別村",
        "天塩郡遠別町",
        "天塩郡天塩町",
        "天塩郡幌延町",
        "天塩郡豊富町",
        "利尻郡利尻町",
        "利尻郡利尻富士町",
        "礼文郡礼文町",
        "宗谷郡猿払村",
        "枝幸郡浜頓別町",
        "枝幸郡中頓別町",
        "枝幸郡枝幸町",
        "紋別郡雄武町",
        "紋別郡興部町",
        "紋別郡西興部村",
        "紋別郡滝上町",
        "紋別郡湧別町",
        "紋別郡遠軽町",
        "常呂郡佐呂間町",
        "常呂郡置戸町",
        "常呂郡訓子府町",
        "網走郡津別町",
        "網走郡美幌町",
        "網走郡大空町",
        "斜里郡小清水町",
        "斜里郡清里町",
        "斜里郡斜里町",
        "上川郡新得町",
        "上川郡清水町",
        "中川郡幕別町",
        "中川郡池田町",
        "中川郡本別町",
        "中川郡豊頃町",
        "十勝郡浦幌町",
        "河西郡芽室町",
        "河西郡中札内村",
        "河西郡更別村",
        "広尾郡広尾町",
        "広尾郡大樹町",
        "河東郡音更町",
        "河東郡鹿追町",
        "河東郡士幌町",
        "河東郡上士幌町",
        "足寄郡足寄町",
        "足寄郡陸別町",
        "白糠郡白糠町",
        "阿寒郡鶴居村",
        "川上郡標茶町",
        "川上郡弟子屈町",
        "釧路郡釧路町",
        "厚岸郡厚岸町",
        "厚岸郡浜中町",
        "野付郡別海町",
        "標津郡中標津町",
        "標津郡標津町",
        "目梨郡羅臼町",
    ),
    "青森県": (
        "青森市",
        "弘前市",
        "八戸市",
        "黒石市",
        "五所川原市",
        "十和田市",
        "三沢市",
        "むつ市",
        "つがる市",
        "平川市",
        "下北郡大間町",
        "下北郡風間浦村",
        "下北郡佐井村",
        "下北郡東通村",
        "上北郡横浜町",
        "上北郡六ヶ所村",
        "上北郡野辺地町",
        "上北郡東北町",
        "上北郡七戸町",
        "上北郡六戸町",
        "上北郡おいらせ町",
        "三戸郡五戸町",
        "三戸郡新郷村",
        "三戸郡三戸町",
        "三戸郡田子町",
        "三戸郡南部町",
        "三戸郡階上町",
        "東津軽郡平内町",
        "東津軽郡蓬田村",
        "東津軽郡外ヶ浜町",
        "東津軽郡今別町",
        "北津軽郡中泊町",
        "北津軽郡鶴田町",
        "北津軽郡板柳町",
        "西津軽郡鰺ヶ沢町",
        "西津軽郡深浦町",
        "中津軽郡西目屋村",
        "南津軽郡藤崎町",
        "南津軽郡田舎館村",
        "南津軽郡大鰐町",
    ),
    "福島県": (
        "須賀川市",
        "田村市",
    ),
    "茨城県": (
        "水戸市",
        "日立市",
        "土浦市",
        "古河市",
        "石岡市",
        "結城市",
        "龍ケ崎市",
        "下妻市",
        "常総市",
        "常陸太田市",
        "高萩市",
        "北茨城市",
        "笠間市",
        "取手市",
        "牛久市",
        "つくば市",
        "ひたちなか市",
        "鹿嶋市",
        "潮来市",
        "守谷市",
        "常陸大宮市",
        "那珂市",
        "筑西市",
        "坂東市",
        "稲敷市",
        "かすみがうら市",
        "桜川市",
        "神栖市",
        "行方市",
        "鉾田市",
        "つくばみらい市",
        "小美玉市",
        "東茨城郡茨城町",
        "東茨城郡大洗町",
        "東茨城郡城里町",
        "那珂郡東海村",
        "久慈郡大子町",
        "稲敷郡美浦村",
        "稲敷郡阿見町",
        "稲敷郡河内町",
        "結城郡八千代町",
        "猿島郡五霞町",
        "猿島郡境町",
        "北相馬郡利根町",
    ),
    "栃木県": (
        "宇都宮市",
        "足利市",
        "栃木市",
        "佐野市",
        "鹿沼市",
        "日光市",
        "小山市",
        "真岡市",
        "大田原市",
        "矢板市",
        "那須塩原市",
        "さくら市",
        "那須烏山市",
        "下野市",
        "河内郡上三川町",
        "芳賀郡益子町",
        "芳賀郡茂木町",
        "芳賀郡市貝町",
        "芳賀郡芳賀町",
        "下都賀郡壬生町",
        "下都賀郡野木町",
        "塩谷郡塩谷町",
        "塩谷郡高根沢町",
        "那須郡那須町",
        "那須郡那珂川町",
    ),
    "群馬県": (
        "前橋市",
        "高崎市",
        "桐生市",
        "伊勢崎市",
        "太田市",
        "沼田市",
        "館林市",
        "渋川市",
        "藤岡市",
        "富岡市",
        "安中市",
        "みどり市",
        "北群馬郡榛東村",
        "北群馬郡吉岡町",
        "多野郡上野村",
        "多野郡神流町",
        "甘楽郡下仁田町",
        "甘楽郡南牧村",
        "甘楽郡甘楽町",
        "吾妻郡中之条町",
        "吾妻郡長野原町",
        "吾妻郡嬬恋村",
        "吾妻郡草津町",
        "吾妻郡高山村",
        "吾妻郡東吾妻町",
        "利根郡片品村",
        "利根郡川場村",
        "利根郡昭和村",
        "利根郡みなかみ町",
        "佐波郡玉村町",
        "邑楽郡板倉町",
        "邑楽郡明和町",
        "邑楽郡千代田町",
        "邑楽郡大泉町",
        "邑楽郡邑楽町",
    ),
    "埼玉県": (
        "さいたま市西区",
        "さいたま市北区",
        "さいたま市大宮区",
        "さいたま市見沼区",
        "さいたま市中央区",
        "さいたま市桜区",
        "さいたま市浦和区",
        "さいたま市南区",
        "さいたま市緑区",
        "さいたま市岩槻区",
        "川越市",
        "熊谷市",
        "川口市",
        "行田市",
        "秩父市",
        "所沢市",
        "飯能市",
        "加須市",
        "本庄市",
        "東松山市",
        "春日部市",
        "狭山市",
        "羽生市",
        "鴻巣市",
        "深谷市",
        "上尾市",
        "草加市",
        "越谷市",
        "蕨市",
        "戸田市",
        "入間市",
        "朝霞市",
        "志木市",
        "和光市",
        "新座市",
        "桶川市",
        "久喜市",
        "北本市",
        "八潮市",
        "富士見市",
        "三郷市",
        "蓮田市",
        "坂戸市",
        "幸手市",
        "鶴ヶ島市",
        "日高市",
        "吉川市",
        "ふじみ野市",
        "白岡市",
        "北足立郡伊奈町",
        "入間郡三芳町",
        "入間郡毛呂山町",
        "入間郡越生町",
        "比企郡滑川町",
        "比企郡嵐山町",
        "比企郡小川町",
        "比企郡川島町",
        "比企郡吉見町",
        "比企郡鳩山町",
        "比企郡ときがわ町",
        "秩父郡横瀬町",
        "秩父郡皆野町",
        "秩父郡長瀞町",
        "秩父郡小鹿野町",
        "秩父郡東秩父村",
        "児玉郡美里町",
        "児玉郡神川町",
        "児玉郡上里町",
        "大里郡寄居町",
        "南埼玉郡宮代町",
        "北葛飾郡杉戸町",
        "北葛飾郡松伏町",
    ),
    "千葉県": (
        "千葉市中央区",
        "千葉市花見川区",
        "千葉市稲毛区",
        "千葉市若葉区",
        "千葉市緑区",
        "千葉市美浜区",
        "銚子市",
        "市川市",
        "船橋市",
        "館山市",
        "木更津市",
        "松戸市",
        "野田市",
        "茂原市",
        "成田市",
        "佐倉市",
        "東金市",
        "旭市",
        "習志野市",
        "柏市",
        "勝浦市",
        "市原市",
        "流山市",
        "八千代市",
        "我孫子市",
        "鴨川市",
        "鎌ケ谷市",
        "君津市",
        "富津市",
        "浦安市",
        "四街道市",
        "袖ケ浦市",
        "八街市",
        "印西市",
        "白井市",
        "富里市",
        "南房総市",
        "匝瑳市",
        "香取市",
        "山武市",
        "いすみ市",
        "大網白里市",
        "印旛郡酒々井町",
        "印旛郡栄町",
        "香取郡神崎町",
        "香取郡多古町",
        "香取郡東庄町",
        "山武郡九十九里町",
        "山武郡芝山町",
        "山武郡横芝光町",
        "長生郡一宮町",
        "長生郡睦沢町",
        "長生郡長生村",
        "長生郡白子町",
        "長生郡長柄町",
        "長生郡長南町",
        "夷隅郡大多喜町",
        "夷隅郡御宿町",
        "安房郡鋸南町",
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
        "八王子市",
        "立川市",
        "武蔵野市",
        "三鷹市",
        "青梅市",
        "府中市",
        "昭島市",
        "調布市",
        "町田市",
        "小金井市",
        "小平市",
        "日野市",
        "東村山市",
        "国分寺市",
        "国立市",
        "福生市",
        "狛江市",
        "東大和市",
        "清瀬市",
        "東久留米市",
        "武蔵村山市",
        "多摩市",
        "稲城市",
        "羽村市",
        "あきる野市",
        "西東京市",
        "西多摩郡瑞穂町",
        "西多摩郡日の出町",
        "西多摩郡檜原村",
        "西多摩郡奥多摩町",
    ),
    "神奈川県": (
        "横浜市鶴見区",
        "横浜市神奈川区",
        "横浜市西区",
        "横浜市中区",
        "横浜市南区",
        "横浜市保土ケ谷区",
        "横浜市磯子区",
        "横浜市金沢区",
        "横浜市港北区",
        "横浜市戸塚区",
        "横浜市港南区",
        "横浜市旭区",
        "横浜市緑区",
        "横浜市瀬谷区",
        "横浜市栄区",
        "横浜市泉区",
        "横浜市青葉区",
        "横浜市都筑区",
        "川崎市川崎区",
        "川崎市幸区",
        "川崎市中原区",
        "川崎市高津区",
        "川崎市多摩区",
        "川崎市宮前区",
        "川崎市麻生区",
        "相模原市緑区",
        "相模原市中央区",
        "相模原市南区",
        "横須賀市",
        "平塚市",
        "鎌倉市",
        "藤沢市",
        "小田原市",
        "茅ヶ崎市",
        "逗子市",
        "三浦市",
        "秦野市",
        "厚木市",
        "大和市",
        "伊勢原市",
        "海老名市",
        "座間市",
        "南足柄市",
        "綾瀬市",
        "三浦郡葉山町",
        "高座郡寒川町",
        "中郡大磯町",
        "中郡二宮町",
        "足柄上郡中井町",
        "足柄上郡大井町",
        "足柄上郡松田町",
        "足柄上郡山北町",
        "足柄上郡開成町",
        "足柄下郡箱根町",
        "足柄下郡真鶴町",
        "足柄下郡湯河原町",
        "愛甲郡愛川町",
        "愛甲郡清川村",
    ),
    "石川県": ("珠洲市",),
    "京都府": (
        "京都市北区",
        "京都市上京区",
        "京都市左京区",
        "京都市中京区",
        "京都市東山区",
        "京都市下京区",
        "京都市南区",
        "京都市右京区",
        "京都市伏見区",
        "京都市山科区",
        "京都市西京区",
        "福知山市",
        "舞鶴市",
        "綾部市",
        "宇治市",
        "宮津市",
        "亀岡市",
        "城陽市",
        "向日市",
        "長岡京市",
        "八幡市",
        "京田辺市",
        "京丹後市",
        "南丹市",
        "木津川市",
        "乙訓郡大山崎町",
        "久世郡久御山町",
        "綴喜郡井手町",
        "綴喜郡宇治田原町",
        "相楽郡笠置町",
        "相楽郡和束町",
        "相楽郡精華町",
        "相楽郡南山城村",
        "船井郡京丹波町",
        "与謝郡伊根町",
        "与謝郡与謝野町",
    ),
}


SUBPREFECTURES: dict[str, dict[str, tuple[str, ...]]] = {
    "北海道": {
        "（札幌市）": (
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
        ),
        "（渡島・檜山）": (
            "函館市",
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
            "瀬棚郡今金町",
            "久遠郡せたな町",
            "奥尻郡奥尻町",
        ),
        "（石狩・空知・後志）": (
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
            "小樽市",
            "夕張市",
            "岩見沢市",
            "美唄市",
            "芦別市",
            "江別市",
            "赤平市",
            "三笠市",
            "千歳市",
            "滝川市",
            "砂川市",
            "歌志内市",
            "深川市",
            "恵庭市",
            "北広島市",
            "石狩市",
            "島牧郡島牧村",
            "虻田郡倶知安町",
            "虻田郡京極町",
            "虻田郡喜茂別町",
            "虻田郡留寿都村",
            "虻田郡真狩村",
            "虻田郡ニセコ町",
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
            "石狩郡当別町",
            "石狩郡新篠津村",
            "樺戸郡月形町",
            "樺戸郡浦臼町",
            "樺戸郡新十津川町",
            "空知郡南幌町",
            "空知郡奈井江町",
            "空知郡上砂川町",
            "夕張郡長沼町",
            "夕張郡栗山町",
            "夕張郡由仁町",
            "雨竜郡雨竜町",
            "雨竜郡北竜町",
            "雨竜郡妹背牛町",
            "雨竜郡秩父別町",
            "雨竜郡沼田町",
        ),
        "（胆振・日高）": (
            "室蘭市",
            "苫小牧市",
            "登別市",
            "伊達市",
            "白老郡白老町",
            "有珠郡壮瞥町",
            "虻田郡洞爺湖町",
            "虻田郡豊浦町",
            "勇払郡安平町",
            "勇払郡厚真町",
            "勇払郡むかわ町",
            "沙流郡平取町",
            "沙流郡日高町",
            "新冠郡新冠町",
            "日高郡新ひだか町",
            "浦河郡浦河町",
            "様似郡様似町",
            "幌泉郡えりも町",
        ),
        "（上川・留萌）": (
            "旭川市",
            "留萌市",
            "士別市",
            "名寄市",
            "富良野市",
            "雨竜郡幌加内町",
            "勇払郡占冠村",
            "空知郡南富良野町",
            "空知郡中富良野町",
            "空知郡上富良野町",
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
            "上川郡下川町",
            "中川郡美深町",
            "中川郡音威子府村",
            "中川郡中川町",
            "増毛郡増毛町",
            "留萌郡小平町",
            "苫前郡苫前町",
            "苫前郡羽幌町",
            "苫前郡初山別村",
            "天塩郡遠別町",
            "天塩郡天塩町",
        ),
        "（宗谷）": (
            "稚内市",
            "天塩郡幌延町",
            "天塩郡豊富町",
            "利尻郡利尻町",
            "利尻郡利尻富士町",
            "礼文郡礼文町",
            "宗谷郡猿払村",
            "枝幸郡浜頓別町",
            "枝幸郡中頓別町",
            "枝幸郡枝幸町",
        ),
        "（オホーツク）": (
            "北見市",
            "網走市",
            "紋別市",
            "紋別郡雄武町",
            "紋別郡興部町",
            "紋別郡西興部村",
            "紋別郡滝上町",
            "紋別郡湧別町",
            "紋別郡遠軽町",
            "常呂郡佐呂間町",
            "常呂郡置戸町",
            "常呂郡訓子府町",
            "網走郡津別町",
            "網走郡美幌町",
            "網走郡大空町",
            "斜里郡小清水町",
            "斜里郡清里町",
            "斜里郡斜里町",
        ),
        "（十勝・釧路・根室）": (
            "釧路市",
            "帯広市",
            "根室市",
            "上川郡新得町",
            "上川郡清水町",
            "中川郡幕別町",
            "中川郡池田町",
            "中川郡本別町",
            "中川郡豊頃町",
            "十勝郡浦幌町",
            "河西郡芽室町",
            "河西郡中札内村",
            "河西郡更別村",
            "広尾郡広尾町",
            "広尾郡大樹町",
            "河東郡音更町",
            "河東郡鹿追町",
            "河東郡士幌町",
            "河東郡上士幌町",
            "足寄郡足寄町",
            "足寄郡陸別町",
            "白糠郡白糠町",
            "阿寒郡鶴居村",
            "川上郡標茶町",
            "川上郡弟子屈町",
            "釧路郡釧路町",
            "厚岸郡厚岸町",
            "厚岸郡浜中町",
            "野付郡別海町",
            "標津郡中標津町",
            "標津郡標津町",
            "目梨郡羅臼町",
        ),
    },
    "埼玉県": {
        "（さいたま市）": (
            "さいたま市西区",
            "さいたま市北区",
            "さいたま市大宮区",
            "さいたま市見沼区",
            "さいたま市中央区",
            "さいたま市桜区",
            "さいたま市浦和区",
            "さいたま市南区",
            "さいたま市緑区",
            "さいたま市岩槻区",
        ),
    },
    "千葉県": {
        "（千葉市）": (
            "千葉市中央区",
            "千葉市花見川区",
            "千葉市稲毛区",
            "千葉市若葉区",
            "千葉市緑区",
            "千葉市美浜区",
        ),
    },
    "東京都": {
        "（２３区）": (
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
    },
    "神奈川県": {
        "（横浜市）": (
            "横浜市鶴見区",
            "横浜市神奈川区",
            "横浜市西区",
            "横浜市中区",
            "横浜市南区",
            "横浜市保土ケ谷区",
            "横浜市磯子区",
            "横浜市金沢区",
            "横浜市港北区",
            "横浜市戸塚区",
            "横浜市港南区",
            "横浜市旭区",
            "横浜市緑区",
            "横浜市瀬谷区",
            "横浜市栄区",
            "横浜市泉区",
            "横浜市青葉区",
            "横浜市都筑区",
        ),
        "（川崎市）": (
            "川崎市川崎区",
            "川崎市幸区",
            "川崎市中原区",
            "川崎市高津区",
            "川崎市宮前区",
            "川崎市多摩区",
            "川崎市麻生区",
        ),
        "（相模原市）": (
            "相模原市緑区",
            "相模原市中央区",
            "相模原市南区",
        ),
    },
    "京都府": {
        "（京都市）": (
            "京都市北区",
            "京都市上京区",
            "京都市左京区",
            "京都市中京区",
            "京都市東山区",
            "京都市下京区",
            "京都市南区",
            "京都市右京区",
            "京都市伏見区",
            "京都市山科区",
            "京都市西京区",
        ),
    },
}

CITY_NAMES = ORG_CITY_NAMES.copy()
REGIONS = ORG_REGIONS.copy()

for pref_name, v in SUBPREFECTURES.items():
    CITY_NAMES[pref_name] = tuple(v.keys()) + CITY_NAMES[pref_name]

for key, value in CITY_NAMES.items():
    value_with_index = tuple(f"{i}: {v}" for i, v in enumerate(value, start=1))
    CITY_NAMES[key] = ("0: （全体）",) + value_with_index

for key, value in REGIONS.items():
    new_value = value
    if key == "関東":
        new_value = ("（一都三県）",) + new_value
    if key != "北海道":
        new_value = ("（全体）",) + new_value
    REGIONS[key] = new_value
