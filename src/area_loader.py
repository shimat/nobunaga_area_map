from collections.abc import Iterable
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Literal, Optional
import pydantic_yaml
import streamlit as st


class ViewState(BaseModel):
    latitude: float
    longitude: float
    zoom: float


class OneCorrespondence(BaseModel):
    own: Literal[0, 1, 2] = Field(default=0)
    towns: tuple[str, ...] = Field(min_length=1)
    koku: Optional[int] = Field(default=None, ge=0)


class Correspondences(BaseModel):
    pref_city: str
    values: tuple[OneCorrespondence, ...]


class OneAreaData(BaseModel):
    view_state: ViewState
    correspondences: tuple[OneCorrespondence, ...]


class AllAreasData(BaseModel):
    view_state: ViewState
    areas: dict[str, OneAreaData]

    def get_all_correspondences(self) -> list[Correspondences]:
        return [Correspondences(pref_city=pref_city, values=area.correspondences)
                for pref_city, area in self.areas.items()]

    def get_one_area_correspondences(self, pref_city: str) -> list[Correspondences]:
        return [Correspondences(pref_city=pref_city, values=self.areas[pref_city].correspondences)]

    def get_multiple_areas_correspondences(self, pref_city_list: Iterable[str]) -> list[Correspondences]:
        return [Correspondences(pref_city=pref_city, values=self.areas[pref_city].correspondences)
                for pref_city in pref_city_list]


@st.cache_data
def load_area_data(prefecture_name: str) -> AllAreasData:
    path = Path(f"data/correspondences/{prefecture_name}.yaml")
    y = path.read_text(encoding="utf-8-sig")
    return pydantic_yaml.parse_yaml_raw_as(AllAreasData, y)
