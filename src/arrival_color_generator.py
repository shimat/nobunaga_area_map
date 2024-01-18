import hashlib
from typing import Self
from randomcolor import RandomColor
from src.enums import ColorCoding


class ArrivalColorGenerator:
    def __init__(self, color_coding: ColorCoding, rand_color: RandomColor | None) -> None:
        self._color_coding = color_coding
        self._rand_color = rand_color

    @classmethod
    def from_unique_key(cls, color_coding: ColorCoding, unique_key: str) -> Self:
        rand_color = None
        if color_coding == ColorCoding.RANDOM:
            rand_color = cls._make_randomcolor(unique_key)
        return ArrivalColorGenerator(color_coding, rand_color)

    @staticmethod
    def create_default() -> Self:
        return ArrivalColorGenerator(ColorCoding.RANDOM, RandomColor(seed=42))

    @staticmethod
    def _make_randomcolor(unique_key: str) -> RandomColor:
        md5 = hashlib.md5(unique_key.encode())
        hex = md5.hexdigest()
        seed = int(hex, 16)
        return RandomColor(seed=seed)

    def generate(self, own: int) -> list[int]:
        match self._color_coding:
            case ColorCoding.OWNERSHIP.value:
                match own:
                    case 0:  # 未踏
                        return [192, 192, 192, 64]
                    case 1:  # 直接来訪
                        return [0, 192, 255, 128]
                    case 2:  # 遠征
                        return [0, 255, 102, 128]
                    case _:
                        raise Exception(f"Invalid value: {own=}")
            case ColorCoding.RANDOM.value:
                rgb = self._rand_color.generate(luminosity="light", format_="Array(rgb)", count=1)[0]
                return [*rgb, 128]
            case ColorCoding.NOTHING.value:
                return [192, 192, 192, 64]
            case _:
                raise Exception(f"Invalid value: {self._color_coding=}")

