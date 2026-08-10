"""The 'Patients Like You' engine: risk from the 50 most similar real patients.

One sentence for the professor: "We standardize all health measurements, find
the 50 patients in the study closest to this one, and simply report how many
of them actually developed diabetes."

No model at all — a second, completely independent opinion the user can
compare against the Uncertainty Engine. When both agree, trust rises.
"""
from typing import NamedTuple

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


class NeighborView(NamedTuple):
    """Result of a similarity query."""
    n_neighbors: int
    n_diabetic: int
    risk: float                    # fraction of neighbors who developed diabetes
    neighbor_rows: pd.DataFrame    # original feature rows + Outcome, for plotting


class PatientsLikeYou:
    """Nearest-neighbor lookup over the standardized study population."""

    def __init__(self, n_neighbors: int = 50) -> None:
        if n_neighbors < 1:
            raise ValueError("n_neighbors must be >= 1")
        self.n_neighbors = n_neighbors
        self._imputer = SimpleImputer(strategy='median')
        self._scaler = StandardScaler()
        self._index: NearestNeighbors | None = None
        self._X: pd.DataFrame | None = None
        self._y: pd.Series | None = None

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'PatientsLikeYou':
        if len(X) < self.n_neighbors:
            raise ValueError("Population smaller than n_neighbors")
        matrix = self._scaler.fit_transform(self._imputer.fit_transform(X))
        self._index = NearestNeighbors(n_neighbors=self.n_neighbors).fit(matrix)
        self._X = X.reset_index(drop=True)
        self._y = y.reset_index(drop=True)
        return self

    def query(self, patient: pd.DataFrame) -> NeighborView:
        """Find the most similar patients to a single-row patient frame."""
        if self._index is None or self._X is None or self._y is None:
            raise RuntimeError("PatientsLikeYou is not fitted")
        if len(patient) != 1:
            raise ValueError("query expects exactly one patient row")
        vec = self._scaler.transform(self._imputer.transform(patient))
        _, idx = self._index.kneighbors(vec)
        neighbor_idx = idx[0]
        outcomes = self._y.iloc[neighbor_idx]
        rows = self._X.iloc[neighbor_idx].assign(Outcome=outcomes.values)
        n_diabetic = int(outcomes.sum())
        return NeighborView(
            n_neighbors=len(neighbor_idx),
            n_diabetic=n_diabetic,
            risk=round(n_diabetic / len(neighbor_idx), 4),
            neighbor_rows=rows.reset_index(drop=True),
        )
