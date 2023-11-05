from pathlib import Path
from pydantic import BaseModel, Field
from typing import TypeAlias
import pydantic_yaml


class ViewState(BaseModel):
    latitude: float
    longitude: float
    zoom: float


class Correspondence(BaseModel):
    own: bool = Field(default=False)
    towns: list[str] = Field(default=list())


Correspondences: TypeAlias = dict[str, Correspondence | None]


class OneAreaData(BaseModel):
    view_state: ViewState
    correspondences: Correspondences


class AllAreasData(BaseModel):
    view_state: ViewState
    areas: dict[str, OneAreaData]

    def get_all_correspondences(self) -> Correspondences:
        merged: dict[str, Correspondence] = {}
        for a in self.areas.values():
            merged.update(a.correspondences)
        return merged


# @st.cache_data
def load_area_data_json() -> AllAreasData:
    path = Path("correspondences.json")
    j = path.read_text(encoding="utf-8-sig")
    return AllAreasData.model_validate_json(j)


def load_area_data() -> AllAreasData:
    path = Path("correspondences.yaml")
    y = path.read_text(encoding="utf-8-sig")
    return pydantic_yaml.parse_yaml_raw_as(AllAreasData, y)
