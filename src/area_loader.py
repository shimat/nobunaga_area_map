from collections.abc import Iterable
from functools import reduce
from pathlib import Path
from typing import Literal, Optional

import pydantic_yaml
import streamlit as st
from pydantic import BaseModel, Field

from src.conditional_decorator import conditional_decorator


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
        return [Correspondences(pref_city=pref_city, values=area.correspondences) for pref_city, area in self.areas.items()]

    def get_one_area_correspondences(self, pref_city: str) -> list[Correspondences]:
        return [Correspondences(pref_city=pref_city, values=self.areas[pref_city].correspondences)]

    def get_multiple_areas_correspondences(self, pref_city_list: Iterable[str]) -> list[Correspondences]:
        return [Correspondences(pref_city=pref_city, values=self.areas[pref_city].correspondences) for pref_city in pref_city_list]


@conditional_decorator(st.cache_data, "local" not in st.secrets)
def load_area_data(prefecture_name: str) -> AllAreasData:
    path = next(Path("data/correspondences/").glob(f"*{prefecture_name}.yaml"))
    # path = Path(f"data/correspondences/{prefecture_name}.yaml")
    y = path.read_text(encoding="utf-8-sig")
    return pydantic_yaml.parse_yaml_raw_as(AllAreasData, y)


def load_region_data(region_name: str, prefecture_names: Iterable[str]) -> AllAreasData:
    view_state_data = load_area_data(region_name).view_state
    areas_data = reduce(lambda d1, d2: d1 | d2, (load_area_data(pn).areas for pn in prefecture_names))
    return AllAreasData(view_state=view_state_data, areas=areas_data)
