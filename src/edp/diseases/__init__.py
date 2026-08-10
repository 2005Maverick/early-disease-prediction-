"""Disease registry: every supported disease, keyed by artifact folder name."""
from edp.diseases.base import DiseaseConfig
from edp.diseases.diabetes import CONFIG as DIABETES
from edp.diseases.heart import CONFIG as HEART

REGISTRY: dict[str, DiseaseConfig] = {c.key: c for c in (DIABETES, HEART)}
