"""Train, honestly evaluate, and save all artifacts.

Honesty rules baked in:
- Every reported metric is OUT-OF-FOLD: computed on patients the model never
  saw during training (stratified 5-fold cross-validation).
- Imputation and scaling live inside the pipelines, so they are re-fitted per
  fold - no leakage.
- The alert threshold is chosen by the stated recall rule, on out-of-fold
  scores only.

Run from the project root:  .venv\\Scripts\\python.exe src\\edp\\train.py
"""
import json
import sys
import time
from pathlib import Path

if __package__ in (None, ''):  # running as a script
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.model_selection import StratifiedKFold

from edp.data import load_clean, missingness_report
from edp.ensemble import UncertaintyEnsemble
from edp.neighbors import PatientsLikeYou
from edp.pipeline import build_baselines
from edp.risk import MIN_RECALL, select_threshold

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET = PROJECT_ROOT / 'datasets' / 'diabetes.csv'
MODELS_DIR = PROJECT_ROOT / 'models'
CV_FOLDS = 5
CV_MEMBERS = 40      # ensemble size inside each CV fold (speed)
FINAL_MEMBERS = 200  # ensemble size of the deployed model


def metric_block(y: np.ndarray, score: np.ndarray, thr: float) -> dict[str, float]:
    pred = (score >= thr).astype(int)
    return {
        'accuracy': round(accuracy_score(y, pred) * 100, 2),
        'precision': round(precision_score(y, pred) * 100, 2),
        'recall': round(recall_score(y, pred) * 100, 2),
        'f1': round(f1_score(y, pred) * 100, 2),
        'roc_auc': round(roc_auc_score(y, score) * 100, 2),
    }


def out_of_fold_scores(X: pd.DataFrame, y: pd.Series) -> dict[str, np.ndarray]:
    """OOF risk scores for the ensemble and each baseline."""
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=42)
    scores: dict[str, np.ndarray] = {
        name: np.zeros(len(y)) for name in ['Uncertainty Ensemble', *build_baselines()]
    }
    for fold, (tr, te) in enumerate(cv.split(X, y)):
        X_tr, y_tr = X.iloc[tr], y.iloc[tr]
        X_te = X.iloc[te]
        ens = UncertaintyEnsemble(n_members=CV_MEMBERS, random_state=42 + fold)
        ens.fit(X_tr, y_tr)
        scores['Uncertainty Ensemble'][te] = ens.predict_mean(X_te)
        for name, model in build_baselines().items():
            model.fit(X_tr, y_tr)
            scores[name][te] = model.predict_proba(X_te)[:, 1]
        print(f"  fold {fold + 1}/{CV_FOLDS} done")
    return scores


def calibration_bins(y: np.ndarray, score: np.ndarray, n_bins: int = 10) -> list[dict]:
    """Predicted vs observed risk per score decile - proof the numbers are honest."""
    order = np.argsort(score)
    bins = np.array_split(order, n_bins)
    return [
        {'predicted': round(float(score[b].mean()) * 100, 1),
         'observed': round(float(y[b].mean()) * 100, 1),
         'patients': len(b)}
        for b in bins if len(b)
    ]


def main() -> None:
    t0 = time.time()
    X, y = load_clean(DATASET)
    y_arr = y.to_numpy()
    print(f"Loaded {len(X)} patients, {X.shape[1]} features")

    print("Cross-validating (honest, out-of-fold)...")
    oof = out_of_fold_scores(X, y)
    ens_scores = oof['Uncertainty Ensemble']
    threshold = select_threshold(y_arr, ens_scores)
    print(f"Threshold from recall>={MIN_RECALL} rule: {threshold}")

    comparison = {name: metric_block(y_arr, s, threshold) for name, s in oof.items()}

    print(f"Training deployed ensemble ({FINAL_MEMBERS} members) on all data...")
    ensemble = UncertaintyEnsemble(n_members=FINAL_MEMBERS, random_state=42).fit(X, y)
    similar = PatientsLikeYou(n_neighbors=50).fit(X, y)

    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(ensemble, MODELS_DIR / 'ensemble.pkl')
    joblib.dump(similar, MODELS_DIR / 'neighbors.pkl')
    report = {
        'trained_on': f'{len(X)} patients (Pima study)',
        'cv_folds': CV_FOLDS,
        'cv_members': CV_MEMBERS,
        'final_members': FINAL_MEMBERS,
        'min_recall_rule': MIN_RECALL,
        'threshold': threshold,
        'deployed_metrics': comparison['Uncertainty Ensemble'],
        'model_comparison': comparison,
        'calibration': calibration_bins(y_arr, ens_scores),
        'population_medians': {k: round(float(v), 2) for k, v in X.median().items()},
        'missingness': missingness_report(DATASET).to_dict(orient='records'),
    }
    (MODELS_DIR / 'metrics.json').write_text(json.dumps(report, indent=2))

    print(json.dumps(comparison, indent=2))
    print(f"Artifacts saved to {MODELS_DIR} in {time.time() - t0:.0f}s")


if __name__ == '__main__':
    main()
