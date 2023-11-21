from pathlib import Path
from pydantic import BaseModel, Field
from typing import Literal
import pydantic_yaml


class ViewState(BaseModel):
    latitude: float
    longitude: float
    zoom: float


class OneCorrespondence(BaseModel):
    own: Literal[0, 1, 2] = Field(default=0)
    towns: list[str] = Field(default=list())


class OneAreaData(BaseModel):
    view_state: ViewState
    correspondences: dict[str, OneCorrespondence | None]


class Correspondences(BaseModel):
    pref_city: str
    values: dict[str, OneCorrespondence | None]
    

class AllAreasData(BaseModel):
    view_state: ViewState
    areas: dict[str, OneAreaData]

    def get_all_correspondences(self) -> list[Correspondences]:
        return [Correspondences(pref_city=pref_city, values=area.correspondences)
                for pref_city, area in self.areas.items()]
    
    def get_one_area_correspondences(self, pref_city: str) -> list[Correspondences]:
        return [Correspondences(pref_city=pref_city, values=self.areas[pref_city].correspondences)]


def load_area_data(prefecture_name: str) -> AllAreasData:
    path = Path(f"data/correspondences_{prefecture_name}.yaml")
    y = path.read_text(encoding="utf-8-sig")
    return pydantic_yaml.parse_yaml_raw_as(AllAreasData, y)
