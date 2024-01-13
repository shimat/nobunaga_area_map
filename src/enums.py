from enum import StrEnum


class MapType(StrEnum):
    NOBUNAGA_AREAS = "「信長の野望 出陣」の各エリア"
    ALL_TOWNS = "全町名"


class ColorCoding(StrEnum):
    OWNERSHIP = "領有"
    RANDOM = "ランダム"
    NOTHING = "なし"
