"""Prevention layer: the shared Recommendation type.

Each disease supplies its own rule set in its config. Rules are deliberately
NOT machine-learned: prevention advice must trace to a published clinical
guideline, not to a statistical artifact. Educational tool - not medical
advice; the UI displays that disclaimer.
"""
from typing import NamedTuple


class Recommendation(NamedTuple):
    title: str
    reason: str
    action: str
