ORG_REGIONS: dict[str, tuple[str, ...]] = {
    "北海道": ("北海道",),
    "東北": ("青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"),
    "関東": ("東京都", "神奈川県", "千葉県", "埼玉県", "茨城県", "栃木県", "群馬県"),
    "甲信": ("山梨県", "長野県"),
    "北陸": ("富山県", "石川県", "福井県"),
    "東海": ("岐阜県", "静岡県", "愛知県", "三重県"),
    "近畿": ("滋賀県",),
    "中国": ("広島県",),
    "四国": ("徳島県", "香川県", "愛媛県", "高知県"),
    "九州・沖縄": ("大分県", "沖縄県"),
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
    "岩手県": (
        "盛岡市",
        "宮古市",
        "大船渡市",
        "花巻市",
        "北上市",
        "久慈市",
        "遠野市",
        "一関市",
        "陸前高田市",
        "釜石市",
        "二戸市",
        "八幡平市",
        "奥州市",
        "滝沢市",
        "岩手郡雫石町",
        "岩手郡葛巻町",
        "岩手郡岩手町",
        "紫波郡紫波町",
        "紫波郡矢巾町",
        "和賀郡西和賀町",
        "胆沢郡金ケ崎町",
        "西磐井郡平泉町",
        "気仙郡住田町",
        "上閉伊郡大槌町",
        "下閉伊郡山田町",
        "下閉伊郡岩泉町",
        "下閉伊郡田野畑村",
        "下閉伊郡普代村",
        "九戸郡軽米町",
        "九戸郡野田村",
        "九戸郡九戸村",
        "九戸郡洋野町",
        "二戸郡一戸町",
    ),
    "宮城県": (
        "仙台市青葉区",
        "仙台市宮城野区",
        "仙台市若林区",
        "仙台市太白区",
        "仙台市泉区",
        "石巻市",
        "塩竈市",
        "気仙沼市",
        "白石市",
        "名取市",
        "角田市",
        "多賀城市",
        "岩沼市",
        "登米市",
        "栗原市",
        "東松島市",
        "大崎市",
        "刈田郡蔵王町",
        "刈田郡七ヶ宿町",
        "柴田郡大河原町",
        "柴田郡村田町",
        "柴田郡柴田町",
        "柴田郡川崎町",
        "伊具郡丸森町",
        "亘理郡亘理町",
        "亘理郡山元町",
        "宮城郡松島町",
        "宮城郡七ヶ浜町",
        "宮城郡利府町",
        "黒川郡大和町",
        "黒川郡大郷町",
        "黒川郡富谷町",
        "黒川郡大衡村",
        "加美郡色麻町",
        "加美郡加美町",
        "遠田郡涌谷町",
        "遠田郡美里町",
        "牡鹿郡女川町",
        "本吉郡南三陸町",
    ),
    "秋田県": (
        "秋田市",
        "能代市",
        "横手市",
        "大館市",
        "男鹿市",
        "湯沢市",
        "鹿角市",
        "由利本荘市",
        "潟上市",
        "大仙市",
        "北秋田市",
        "にかほ市",
        "仙北市",
        "鹿角郡小坂町",
        "北秋田郡上小阿仁村",
        "山本郡藤里町",
        "山本郡三種町",
        "山本郡八峰町",
        "南秋田郡五城目町",
        "南秋田郡八郎潟町",
        "南秋田郡井川町",
        "南秋田郡大潟村",
        "仙北郡美郷町",
        "雄勝郡羽後町",
        "雄勝郡東成瀬村",
    ),
    "山形県": (
        "山形市",
        "米沢市",
        "鶴岡市",
        "酒田市",
        "新庄市",
        "寒河江市",
        "上山市",
        "村山市",
        "長井市",
        "天童市",
        "東根市",
        "尾花沢市",
        "南陽市",
        "東村山郡山辺町",
        "東村山郡中山町",
        "西村山郡河北町",
        "西村山郡西川町",
        "西村山郡朝日町",
        "西村山郡大江町",
        "北村山郡大石田町",
        "最上郡金山町",
        "最上郡最上町",
        "最上郡舟形町",
        "最上郡真室川町",
        "最上郡大蔵村",
        "最上郡鮭川村",
        "最上郡戸沢村",
        "東置賜郡高畠町",
        "東置賜郡川西町",
        "西置賜郡小国町",
        "西置賜郡白鷹町",
        "西置賜郡飯豊町",
        "東田川郡三川町",
        "東田川郡庄内町",
        "飽海郡遊佐町",
    ),
    "福島県": (
        "福島市",
        "会津若松市",
        "郡山市",
        "いわき市",
        "白河市",
        "須賀川市",
        "喜多方市",
        "相馬市",
        "二本松市",
        "田村市",
        "南相馬市",
        "伊達市",
        "本宮市",
        "伊達郡桑折町",
        "伊達郡国見町",
        "伊達郡川俣町",
        "安達郡大玉村",
        "岩瀬郡鏡石町",
        "岩瀬郡天栄村",
        "南会津郡下郷町",
        "南会津郡檜枝岐村",
        "南会津郡只見町",
        "南会津郡南会津町",
        "耶麻郡北塩原村",
        "耶麻郡西会津町",
        "耶麻郡磐梯町",
        "耶麻郡猪苗代町",
        "河沼郡会津坂下町",
        "河沼郡湯川村",
        "河沼郡柳津町",
        "大沼郡三島町",
        "大沼郡金山町",
        "大沼郡昭和村",
        "大沼郡会津美里町",
        "西白河郡西郷村",
        "西白河郡泉崎村",
        "西白河郡中島村",
        "西白河郡矢吹町",
        "東白川郡棚倉町",
        "東白川郡矢祭町",
        "東白川郡塙町",
        "東白川郡鮫川村",
        "石川郡石川町",
        "石川郡玉川村",
        "石川郡平田村",
        "石川郡浅川町",
        "石川郡古殿町",
        "田村郡三春町",
        "田村郡小野町",
        "双葉郡広野町",
        "双葉郡楢葉町",
        "双葉郡富岡町",
        "双葉郡川内村",
        "双葉郡大熊町",
        "双葉郡双葉町",
        "双葉郡浪江町",
        "双葉郡葛尾村",
        "相馬郡新地町",
        "相馬郡飯舘村",
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
        "大島支庁大島町",
        "大島支庁利島村",
        "大島支庁新島村",
        "大島支庁神津島村",
        "三宅支庁三宅村",
        "三宅支庁御蔵島村",
        "八丈支庁八丈町",
        "八丈支庁青ケ島村",
        "小笠原支庁小笠原村",
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
    "富山県": (
        "富山市",
        "高岡市",
        "魚津市",
        "氷見市",
        "滑川市",
        "黒部市",
        "砺波市",
        "小矢部市",
        "南砺市",
        "射水市",
        "中新川郡舟橋村",
        "中新川郡上市町",
        "中新川郡立山町",
        "下新川郡入善町",
        "下新川郡朝日町",
    ),
    "石川県": (
        "金沢市",
        "七尾市",
        "小松市",
        "輪島市",
        "珠洲市",
        "加賀市",
        "羽咋市",
        "かほく市",
        "白山市",
        "能美市",
        "野々市市",
        "能美郡川北町",
        "河北郡津幡町",
        "河北郡内灘町",
        "羽咋郡志賀町",
        "羽咋郡宝達志水町",
        "鹿島郡中能登町",
        "鳳珠郡穴水町",
        "鳳珠郡能登町",
    ),
    "福井県": (
        "福井市",
        "敦賀市",
        "小浜市",
        "大野市",
        "勝山市",
        "鯖江市",
        "あわら市",
        "越前市",
        "坂井市",
        "吉田郡永平寺町",
        "今立郡池田町",
        "南条郡南越前町",
        "丹生郡越前町",
        "三方郡美浜町",
        "大飯郡高浜町",
        "大飯郡おおい町",
        "三方上中郡若狭町",
    ),
    "山梨県": (
        "甲府市",
        "富士吉田市",
        "都留市",
        "山梨市",
        "大月市",
        "韮崎市",
        "南アルプス市",
        "北杜市",
        "甲斐市",
        "笛吹市",
        "上野原市",
        "甲州市",
        "中央市",
        "西八代郡市川三郷町",
        "南巨摩郡早川町",
        "南巨摩郡身延町",
        "南巨摩郡南部町",
        "南巨摩郡富士川町",
        "中巨摩郡昭和町",
        "南都留郡道志村",
        "南都留郡西桂町",
        "南都留郡忍野村",
        "南都留郡山中湖村",
        "南都留郡鳴沢村",
        "南都留郡富士河口湖町",
        "北都留郡小菅村",
        "北都留郡丹波山村",
    ),
    "長野県": (
        "長野市",
        "松本市",
        "上田市",
        "岡谷市",
        "飯田市",
        "諏訪市",
        "須坂市",
        "小諸市",
        "伊那市",
        "駒ヶ根市",
        "中野市",
        "大町市",
        "飯山市",
        "茅野市",
        "塩尻市",
        "佐久市",
        "千曲市",
        "東御市",
        "安曇野市",
        "南佐久郡小海町",
        "南佐久郡川上村",
        "南佐久郡南牧村",
        "南佐久郡南相木村",
        "南佐久郡北相木村",
        "南佐久郡佐久穂町",
        "北佐久郡軽井沢町",
        "北佐久郡御代田町",
        "北佐久郡立科町",
        "小県郡青木村",
        "小県郡長和町",
        "諏訪郡下諏訪町",
        "諏訪郡富士見町",
        "諏訪郡原村",
        "上伊那郡辰野町",
        "上伊那郡箕輪町",
        "上伊那郡飯島町",
        "上伊那郡南箕輪村",
        "上伊那郡中川村",
        "上伊那郡宮田村",
        "下伊那郡松川町",
        "下伊那郡高森町",
        "下伊那郡阿南町",
        "下伊那郡阿智村",
        "下伊那郡平谷村",
        "下伊那郡根羽村",
        "下伊那郡下條村",
        "下伊那郡売木村",
        "下伊那郡天龍村",
        "下伊那郡泰阜村",
        "下伊那郡喬木村",
        "下伊那郡豊丘村",
        "下伊那郡大鹿村",
        "木曽郡上松町",
        "木曽郡南木曽町",
        "木曽郡木祖村",
        "木曽郡王滝村",
        "木曽郡大桑村",
        "木曽郡木曽町",
        "東筑摩郡麻績村",
        "東筑摩郡生坂村",
        "東筑摩郡山形村",
        "東筑摩郡朝日村",
        "東筑摩郡筑北村",
        "北安曇郡池田町",
        "北安曇郡松川村",
        "北安曇郡白馬村",
        "北安曇郡小谷村",
        "埴科郡坂城町",
        "上高井郡小布施町",
        "上高井郡高山村",
        "下高井郡山ノ内町",
        "下高井郡木島平村",
        "下高井郡野沢温泉村",
        "上水内郡信濃町",
        "上水内郡小川村",
        "上水内郡飯綱町",
        "下水内郡栄村",
    ),
    "岐阜県": (
        "岐阜市",
        "大垣市",
        "高山市",
        "多治見市",
        "関市",
        "中津川市",
        "美濃市",
        "瑞浪市",
        "羽島市",
        "恵那市",
        "美濃加茂市",
        "土岐市",
        "各務原市",
        "可児市",
        "山県市",
        "瑞穂市",
        "飛騨市",
        "本巣市",
        "郡上市",
        "下呂市",
        "海津市",
        "羽島郡岐南町",
        "羽島郡笠松町",
        "養老郡養老町",
        "不破郡垂井町",
        "不破郡関ケ原町",
        "安八郡神戸町",
        "安八郡輪之内町",
        "安八郡安八町",
        "揖斐郡揖斐川町",
        "揖斐郡大野町",
        "揖斐郡池田町",
        "本巣郡北方町",
        "加茂郡坂祝町",
        "加茂郡富加町",
        "加茂郡川辺町",
        "加茂郡七宗町",
        "加茂郡八百津町",
        "加茂郡白川町",
        "加茂郡東白川村",
        "可児郡御嵩町",
        "大野郡白川村",
    ),
    "静岡県": (
        "静岡市葵区",
        "静岡市駿河区",
        "静岡市清水区",
        "浜松市中区",
        "浜松市東区",
        "浜松市西区",
        "浜松市南区",
        "浜松市北区",
        "浜松市浜北区",
        "浜松市天竜区",
        "沼津市",
        "熱海市",
        "三島市",
        "富士宮市",
        "伊東市",
        "島田市",
        "富士市",
        "磐田市",
        "焼津市",
        "掛川市",
        "藤枝市",
        "御殿場市",
        "袋井市",
        "下田市",
        "裾野市",
        "湖西市",
        "伊豆市",
        "御前崎市",
        "菊川市",
        "伊豆の国市",
        "牧之原市",
        "賀茂郡東伊豆町",
        "賀茂郡河津町",
        "賀茂郡南伊豆町",
        "賀茂郡松崎町",
        "賀茂郡西伊豆町",
        "田方郡函南町",
        "駿東郡清水町",
        "駿東郡長泉町",
        "駿東郡小山町",
        "榛原郡吉田町",
        "榛原郡川根本町",
        "周智郡森町",
    ),
    "愛知県": (
        "名古屋市千種区",
        "名古屋市東区",
        "名古屋市北区",
        "名古屋市西区",
        "名古屋市中村区",
        "名古屋市中区",
        "名古屋市昭和区",
        "名古屋市瑞穂区",
        "名古屋市熱田区",
        "名古屋市中川区",
        "名古屋市港区",
        "名古屋市南区",
        "名古屋市守山区",
        "名古屋市緑区",
        "名古屋市名東区",
        "名古屋市天白区",
        "豊橋市",
        "岡崎市",
        "一宮市",
        "瀬戸市",
        "半田市",
        "春日井市",
        "豊川市",
        "津島市",
        "碧南市",
        "刈谷市",
        "豊田市",
        "安城市",
        "西尾市",
        "蒲郡市",
        "犬山市",
        "常滑市",
        "江南市",
        "小牧市",
        "稲沢市",
        "新城市",
        "東海市",
        "大府市",
        "知多市",
        "知立市",
        "尾張旭市",
        "高浜市",
        "岩倉市",
        "豊明市",
        "日進市",
        "田原市",
        "愛西市",
        "清須市",
        "北名古屋市",
        "弥富市",
        "みよし市",
        "あま市",
        "長久手市",
        "愛知郡東郷町",
        "西春日井郡豊山町",
        "丹羽郡大口町",
        "丹羽郡扶桑町",
        "海部郡大治町",
        "海部郡蟹江町",
        "海部郡飛島村",
        "知多郡阿久比町",
        "知多郡東浦町",
        "知多郡南知多町",
        "知多郡美浜町",
        "知多郡武豊町",
        "額田郡幸田町",
        "北設楽郡設楽町",
        "北設楽郡東栄町",
        "北設楽郡豊根村",
    ),
    "三重県": (
        "津市",
        "四日市市",
        "伊勢市",
        "松阪市",
        "桑名市",
        "鈴鹿市",
        "名張市",
        "尾鷲市",
        "亀山市",
        "鳥羽市",
        "熊野市",
        "いなべ市",
        "志摩市",
        "伊賀市",
        "桑名郡木曽岬町",
        "員弁郡東員町",
        "三重郡菰野町",
        "三重郡朝日町",
        "三重郡川越町",
        "多気郡多気町",
        "多気郡明和町",
        "多気郡大台町",
        "度会郡玉城町",
        "度会郡度会町",
        "度会郡大紀町",
        "度会郡南伊勢町",
        "北牟婁郡紀北町",
        "南牟婁郡御浜町",
        "南牟婁郡紀宝町",
    ),
    "滋賀県": (
        "大津市",
        "彦根市",
        "長浜市",
        "近江八幡市",
        "草津市",
        "守山市",
        "栗東市",
        "甲賀市",
        "野洲市",
        "湖南市",
        "高島市",
        "東近江市",
        "米原市",
        "蒲生郡日野町",
        "蒲生郡竜王町",
        "愛知郡愛荘町",
        "犬上郡豊郷町",
        "犬上郡甲良町",
        "犬上郡多賀町",
    ),
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
    "広島県": (
        "広島市中区",
        "広島市東区",
        "広島市南区",
        "広島市西区",
        "広島市安佐南区",
        "広島市安佐北区",
        "広島市安芸区",
        "広島市佐伯区",
        "呉市",
        "竹原市",
        "三原市",
        "尾道市",
        "福山市",
        "府中市",
        "三次市",
        "庄原市",
        "大竹市",
        "東広島市",
        "廿日市市",
        "安芸高田市",
        "江田島市",
        "安芸郡府中町",
        "安芸郡海田町",
        "安芸郡熊野町",
        "安芸郡坂町",
        "山県郡安芸太田町",
        "山県郡北広島町",
        "豊田郡大崎上島町",
        "世羅郡世羅町",
        "神石郡神石高原町",
    ),
    "徳島県": (
        "徳島市",
        "鳴門市",
        "小松島市",
        "阿南市",
        "吉野川市",
        "阿波市",
        "美馬市",
        "三好市",
        "勝浦郡勝浦町",
        "勝浦郡上勝町",
        "名東郡佐那河内村",
        "名西郡石井町",
        "名西郡神山町",
        "那賀郡那賀町",
        "海部郡牟岐町",
        "海部郡美波町",
        "海部郡海陽町",
        "板野郡松茂町",
        "板野郡北島町",
        "板野郡藍住町",
        "板野郡板野町",
        "板野郡上板町",
        "美馬郡つるぎ町",
        "三好郡東みよし町",
    ),
    "香川県": (
        "高松市",
        "丸亀市",
        "坂出市",
        "善通寺市",
        "観音寺市",
        "さぬき市",
        "東かがわ市",
        "三豊市",
        "小豆郡土庄町",
        "小豆郡小豆島町",
        "木田郡三木町",
        "香川郡直島町",
        "綾歌郡宇多津町",
        "綾歌郡綾川町",
        "仲多度郡琴平町",
        "仲多度郡多度津町",
        "仲多度郡まんのう町",
    ),
    "愛媛県": (
        "松山市",
        "今治市",
        "宇和島市",
        "八幡浜市",
        "新居浜市",
        "西条市",
        "大洲市",
        "伊予市",
        "四国中央市",
        "西予市",
        "東温市",
        "越智郡上島町",
        "上浮穴郡久万高原町",
        "伊予郡松前町",
        "伊予郡砥部町",
        "喜多郡内子町",
        "西宇和郡伊方町",
        "北宇和郡松野町",
        "北宇和郡鬼北町",
        "南宇和郡愛南町",
    ),
    "高知県": (
        "高知市",
        "室戸市",
        "安芸市",
        "南国市",
        "土佐市",
        "須崎市",
        "宿毛市",
        "土佐清水市",
        "四万十市",
        "香南市",
        "香美市",
        "安芸郡東洋町",
        "安芸郡奈半利町",
        "安芸郡田野町",
        "安芸郡安田町",
        "安芸郡北川村",
        "安芸郡馬路村",
        "安芸郡芸西村",
        "長岡郡本山町",
        "長岡郡大豊町",
        "土佐郡土佐町",
        "土佐郡大川村",
        "吾川郡いの町",
        "吾川郡仁淀川町",
        "高岡郡中土佐町",
        "高岡郡佐川町",
        "高岡郡越知町",
        "高岡郡檮原町",
        "高岡郡日高村",
        "高岡郡津野町",
        "高岡郡四万十町",
        "幡多郡大月町",
        "幡多郡三原村",
        "幡多郡黒潮町",
    ),
    "大分県": (
        "大分市",
        "別府市",
        "中津市",
        "日田市",
        "佐伯市",
        "臼杵市",
        "津久見市",
        "竹田市",
        "豊後高田市",
        "杵築市",
        "宇佐市",
        "豊後大野市",
        "由布市",
        "国東市",
        "東国東郡姫島村",
        "速見郡日出町",
        "玖珠郡九重町",
        "玖珠郡玖珠町",
    ),
    "沖縄県": (
        "那覇市",
        "宜野湾市",
        "石垣市",
        "浦添市",
        "名護市",
        "糸満市",
        "沖縄市",
        "豊見城市",
        "うるま市",
        "宮古島市",
        "南城市",
        "国頭郡国頭村",
        "国頭郡大宜味村",
        "国頭郡東村",
        "国頭郡今帰仁村",
        "国頭郡本部町",
        "国頭郡恩納村",
        "国頭郡宜野座村",
        "国頭郡金武町",
        "国頭郡伊江村",
        "中頭郡読谷村",
        "中頭郡嘉手納町",
        "中頭郡北谷町",
        "中頭郡北中城村",
        "中頭郡中城村",
        "中頭郡西原町",
        "島尻郡与那原町",
        "島尻郡南風原町",
        "島尻郡渡嘉敷村",
        "島尻郡座間味村",
        "島尻郡粟国村",
        "島尻郡渡名喜村",
        "島尻郡南大東村",
        "島尻郡北大東村",
        "島尻郡伊平屋村",
        "島尻郡伊是名村",
        "島尻郡久米島町",
        "島尻郡八重瀬町",
        "宮古郡多良間村",
        "八重山郡竹富町",
        "八重山郡与那国町",
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
