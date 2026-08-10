"""The Uncertainty Engine: a bootstrap ensemble that outputs a risk DISTRIBUTION.

One sentence for the professor: "We train 200 copies of the model, each on a
random resample of the patients; each copy gives its own risk estimate, and
the spread of those 200 answers is our uncertainty."

A patient the models agree on gets a narrow distribution (confident); an
unusual patient gets a wide one (the system visibly says 'less sure').
"""
import numpy as np
import pandas as pd
from sklearn.base import clone

from edp.pipeline import build_base_learner


class UncertaintyEnsemble:
    """Bootstrap ensemble of identical pipelines, each fit on a resample."""

    def __init__(self, n_members: int = 200, random_state: int = 42) -> None:
        if n_members < 2:
            raise ValueError("n_members must be >= 2")
        self.n_members = n_members
        self.random_state = random_state
        self.members_: list = []

    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'UncertaintyEnsemble':
        """Fit each member on a bootstrap resample containing both classes."""
        rng = np.random.RandomState(self.random_state)
        n = len(X)
        if n == 0:
            raise ValueError("Cannot fit on an empty dataset")
        members = []
        for i in range(self.n_members):
            for _ in range(20):  # redraw until both classes present
                idx = rng.randint(0, n, size=n)
                if y.iloc[idx].nunique() == 2:
                    break
            else:
                raise RuntimeError("Could not draw a bootstrap sample with both classes")
            member = clone(build_base_learner(random_state=self.random_state + i))
            member.fit(X.iloc[idx], y.iloc[idx])
            members.append(member)
        self.members_ = members
        return self

    def predict_dist(self, X: pd.DataFrame) -> np.ndarray:
        """All members' risk estimates; shape (n_members, n_rows)."""
        if not self.members_:
            raise RuntimeError("Ensemble is not fitted")
        return np.stack([m.predict_proba(X)[:, 1] for m in self.members_])

    def predict_mean(self, X: pd.DataFrame) -> np.ndarray:
        """The headline risk score: average of all members."""
        return self.predict_dist(X).mean(axis=0)

    def predict_interval(self, X: pd.DataFrame, low: float = 5.0,
                         high: float = 95.0) -> tuple[np.ndarray, np.ndarray]:
        """Confidence band: (low, high) percentiles across members."""
        dist = self.predict_dist(X)
        return (np.percentile(dist, low, axis=0),
                np.percentile(dist, high, axis=0))
