import hashlib
from randomcolor import RandomColor
from src.enums import ColorCoding


class ArrivalColorGenerator:
    def __init__(self, color_coding: ColorCoding, unique_key: str) -> None:
        self._color_coding = color_coding
        if color_coding == ColorCoding.RANDOM:
            self._rand_color = self._make_randomcolor(unique_key)

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

