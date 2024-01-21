import hashlib
from typing import Self
from randomcolor import RandomColor
from src.enums import ColorCoding
from abc import ABC, abstractmethod


class IColorGenerator(ABC):
    @abstractmethod
    def generate(self, own: int) -> list[int]:
        pass


class RandomColorGenerator(IColorGenerator):
    def __init__(
            self,
            rand_color: RandomColor | None,
            hue: str | None = None,
            luminosity: str | None = "light"
    ) -> None:
        self._rand_color = rand_color
        self.hue = hue
        self.luminosity = luminosity

    @classmethod
    def from_unique_key(
        cls,
        unique_key: str,
        hue: str | None = None,
        luminosity: str | None = "light"
    ) -> Self:
        rand_color = cls._make_randomcolor(unique_key)
        return RandomColorGenerator(rand_color, hue, luminosity)
    
    @staticmethod
    def create_default() -> Self:
        return RandomColorGenerator(RandomColor(seed=42))
    
    @staticmethod
    def _make_randomcolor(unique_key: str) -> RandomColor:
        md5 = hashlib.md5(unique_key.encode())
        hex = md5.hexdigest()
        seed = int(hex, 16)
        return RandomColor(seed=seed)
    
    def generate(self, own: int = 0) -> list[int]:
        rgb = self._rand_color.generate(hue=self.hue, luminosity=self.luminosity, format_="Array(rgb)", count=1)[0]
        return [*rgb, 128]


class ArrivalColorGenerator(IColorGenerator):
    def generate(self, own: int) -> list[int]:
        match own:
            case 0:  # 未踏
                return [192, 192, 192, 64]
            case 1:  # 直接来訪
                return [0, 192, 255, 128]
            case 2:  # 遠征
                return [0, 255, 102, 128]
            case _:
                raise Exception(f"Invalid value: {own=}")


class ConstColorGenerator(IColorGenerator):
    def generate(self, own: int) -> list[int]:
        return [192, 192, 192, 64]


def make_color_generator(color_coding: ColorCoding, unique_key: str) -> IColorGenerator:
    match color_coding:
        case ColorCoding.OWNERSHIP:
            return ArrivalColorGenerator()
        case ColorCoding.RANDOM:
            return RandomColorGenerator.from_unique_key(unique_key)
        case ColorCoding.NOTHING:
            return ConstColorGenerator()
        case _:
            raise Exception(f"Invalid value: {color_coding=}")
