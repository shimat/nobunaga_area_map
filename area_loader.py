from pathlib import Path
from pydantic import BaseModel, Field
from typing import Literal
import pydantic_yaml


class ViewState(BaseModel):
    latitude: float
    longitude: float
    zoom: float


class OneCorrespondence(BaseModel):
    own: Literal["no", "expedition", "arrived"] = Field(default="no")
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


# @st.cache_data
def load_area_data_json() -> AllAreasData:
    path = Path("correspondences.json")
    j = path.read_text(encoding="utf-8-sig")
    return AllAreasData.model_validate_json(j)


def load_area_data() -> AllAreasData:
    path = Path("correspondences.yaml")
    y = path.read_text(encoding="utf-8-sig")
    return pydantic_yaml.parse_yaml_raw_as(AllAreasData, y)
