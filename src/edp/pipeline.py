"""Base learner and baselines.

Every model is a Pipeline so imputation and scaling are re-fitted inside each
training fold / bootstrap sample — the test data can never leak into them.

The base learner (gradient boosting) is deliberately one strong, standard
model: the novelty of this project is NOT an exotic model, it is what we build
around it — bootstrap uncertainty, a similarity engine, and honest evaluation.
"""
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


def _wrap(name: str, estimator) -> Pipeline:
    return Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('scale', StandardScaler()),
        (name, estimator),
    ])


def build_base_learner(random_state: int = RANDOM_STATE) -> Pipeline:
    """One member of the uncertainty ensemble: impute -> scale -> boosting."""
    return _wrap('boosting', GradientBoostingClassifier(random_state=random_state))


def build_baselines() -> dict[str, Pipeline]:
    """Single-model baselines for the honest comparison table in the app."""
    return {
        'Logistic Regression': _wrap('logistic', LogisticRegression(
            max_iter=2000, random_state=RANDOM_STATE)),
        'Random Forest': _wrap('forest', RandomForestClassifier(
            n_estimators=300, min_samples_leaf=3, random_state=RANDOM_STATE)),
        'Gradient Boosting': _wrap('boosting', GradientBoostingClassifier(
            random_state=RANDOM_STATE)),
    }
