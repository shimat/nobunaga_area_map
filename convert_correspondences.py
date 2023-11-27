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


class OneCorrespondence2(BaseModel):
    towns: tuple[str, ...] = Field(min_length=1)
    z_own: Literal[0, 1, 2] = Field(default=0)

    @classmethod
    def from_1(cls, area_name: str, corr: OneCorrespondence | None) -> "OneCorrespondence2":
        if corr is None:
            corr = OneCorrespondence(own=0, towns=[])
        return OneCorrespondence2(
            z_own=corr.own,
            towns=(area_name,) + tuple(corr.towns)
        )


class OneAreaData2(BaseModel):
    a_view_state: ViewState
    correspondences: tuple[OneCorrespondence2, ...]

    @classmethod
    def from_1(cls, data: OneAreaData) -> "OneAreaData2":
        return OneAreaData2(
            a_view_state=data.view_state,
            correspondences=tuple(
                OneCorrespondence2.from_1(area_name, corr) for area_name, corr in data.correspondences.items()
            )
        )

class AllAreasData2(BaseModel):
    a_view_state: ViewState
    areas: dict[str, OneAreaData2]

    @classmethod
    def from_1(cls, data: AllAreasData) -> "AllAreasData2":
        return AllAreasData2(
            a_view_state=data.view_state,
            areas={pref_city: OneAreaData2.from_1(area) for pref_city, area in data.areas.items()}
        )


def load_area_data(prefecture_name: str) -> AllAreasData:
    path = Path(f"data/correspondences/{prefecture_name}.yaml")
    y = path.read_text(encoding="utf-8-sig")
    return pydantic_yaml.parse_yaml_raw_as(AllAreasData, y)



def remove_own0(yaml: str) -> str:
    import re

    yaml = re.sub(r"own: 0.*\n", "\n", yaml, flags=re.MULTILINE)

    yaml = re.sub(r"\n\s+\n", "\n", yaml, flags=re.MULTILINE)

    return yaml

def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python convert_correspondences.py <prefecture_name>")
        sys.exit(1)
    pref = sys.argv[1]

    area_data = load_area_data(pref)
    # print(area_data)

    area_data2 = AllAreasData2.from_1(area_data)
    result_yaml = pydantic_yaml.to_yaml_str(area_data2,)

    result_yaml = result_yaml.replace("a_view_state:", "view_state:")
    result_yaml = result_yaml.replace("z_own:", "own:")
    result_yaml = remove_own0(result_yaml)

    Path(f"{pref}_dst.yaml").write_text(result_yaml, encoding="utf-8-sig")


if __name__ == "__main__":
    main()
