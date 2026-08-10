"""The disease config contract: everything disease-specific lives in one object.

The engine (ensemble, neighbors, drivers, what-if evaluation, risk tiers,
training, UI) is disease-agnostic; each disease supplies data locations,
feature semantics, intake form fields, scenarios, and prevention rules.
"""
from dataclasses import dataclass, field
from typing import Callable

import pandas as pd

from edp.recommend import Recommendation
from edp.whatif import Scenario

# Form field kinds understood by the intake renderer:
#   number          {col,label,min,max,default[,step,format,help]}
#   number_unknown  number + an "unknown" checkbox -> NaN
#   select          {col,label,options:[(label,value),...],default_index}
#   select_unknown  select + trailing "Unknown" option -> NaN
#   flag            checkbox -> 1/0
FormField = dict


@dataclass(frozen=True)
class DiseaseConfig:
    key: str                       # artifact folder name
    name: str                      # display name
    dataset: str                   # csv path relative to project root
    features: tuple[str, ...]
    target: str
    zero_missing: tuple[str, ...]  # columns where 0 is an impossible value
    friendly: dict[str, str]       # column -> human label
    strip_fields: tuple[tuple[str, str], ...]      # (col, label) summary strip
    similar_axes: tuple[tuple[str, str], tuple[str, str]]  # (col,label) x, y
    form_spec: tuple[FormField, ...]
    build_scenarios: Callable[[pd.DataFrame], list[Scenario]]
    build_recommendations: Callable[[pd.DataFrame, float], list[Recommendation]]
    dataset_note: str = ''
    extra: dict = field(default_factory=dict)
