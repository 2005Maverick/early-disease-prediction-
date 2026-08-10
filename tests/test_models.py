"""Integration tests for the ensemble and similarity engines (small but real)."""
import numpy as np
import pandas as pd
import pytest

from edp.diseases.diabetes import FEATURES as ALL_FEATURES
from edp.ensemble import UncertaintyEnsemble
from edp.neighbors import PatientsLikeYou

pytestmark = pytest.mark.integration


@pytest.fixture(scope='module')
def toy_population() -> tuple[pd.DataFrame, pd.Series]:
    """120 synthetic patients where glucose and BMI genuinely drive outcome."""
    rng = np.random.RandomState(0)
    n = 120
    X = pd.DataFrame({
        'Pregnancies': rng.randint(0, 10, n),
        'Glucose': rng.normal(120, 30, n).clip(70, 200),
        'BloodPressure': rng.normal(70, 10, n),
        'SkinThickness': rng.normal(25, 8, n),
        'Insulin': rng.normal(100, 40, n).clip(15, 300),
        'BMI': rng.normal(31, 6, n).clip(18, 50),
        'DiabetesPedigreeFunction': rng.uniform(0.1, 1.5, n),
        'Age': rng.randint(21, 70, n),
    }, columns=list(ALL_FEATURES))
    logit = 0.05 * (X['Glucose'] - 120) + 0.15 * (X['BMI'] - 31)
    y = pd.Series((1 / (1 + np.exp(-logit)) > rng.uniform(size=n)).astype(int))
    return X, y


def test_ensemble_distribution_shape_and_bounds(toy_population) -> None:
    X, y = toy_population
    ens = UncertaintyEnsemble(n_members=5, random_state=0).fit(X, y)
    dist = ens.predict_dist(X.head(3))
    assert dist.shape == (5, 3)
    assert ((dist >= 0) & (dist <= 1)).all()
    lo, hi = ens.predict_interval(X.head(3))
    assert (lo <= hi).all()
    mean = ens.predict_mean(X.head(3))
    assert ((mean >= lo) & (mean <= hi)).all()


def test_ensemble_separates_extreme_patients(toy_population) -> None:
    X, y = toy_population
    ens = UncertaintyEnsemble(n_members=5, random_state=0).fit(X, y)
    low = X.head(1).assign(Glucose=80.0, BMI=20.0)
    high = X.head(1).assign(Glucose=195.0, BMI=45.0)
    assert ens.predict_mean(high)[0] > ens.predict_mean(low)[0]


def test_neighbors_returns_valid_view(toy_population) -> None:
    X, y = toy_population
    plu = PatientsLikeYou(n_neighbors=20).fit(X, y)
    view = plu.query(X.head(1))
    assert view.n_neighbors == 20
    assert 0.0 <= view.risk <= 1.0
    assert view.n_diabetic == int(view.neighbor_rows['Outcome'].sum())
    assert len(view.neighbor_rows) == 20


def test_neighbors_rejects_multi_row_query(toy_population) -> None:
    X, y = toy_population
    plu = PatientsLikeYou(n_neighbors=10).fit(X, y)
    with pytest.raises(ValueError):
        plu.query(X.head(2))
