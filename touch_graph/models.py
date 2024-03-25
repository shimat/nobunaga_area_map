import shapely  # type: ignore
from typing import NamedTuple


class TownPolygon(NamedTuple):
    prefecture: str
    city: str
    town: str
    polygon: shapely.Polygon

    @property
    def name(self) -> str:
        return f"{self.prefecture}_{self.city}_{self.town}"

    def __str__(self) -> str:
        return self.name
