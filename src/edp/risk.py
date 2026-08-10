"""Decision layer: the alert threshold comes from a stated rule, not a magic number.

Rule: choose the smallest threshold whose out-of-fold recall is still at least
MIN_RECALL (we refuse to miss more than ~15% of true diabetics), then among
those pick the one with the best precision. Missing a diabetic costs more
than a false alarm — that asymmetry is the whole justification.
"""
from typing import NamedTuple

import numpy as np

MIN_RECALL = 0.85


class RiskTier(NamedTuple):
    name: str
    color: str


def select_threshold(y_true: np.ndarray, y_score: np.ndarray,
                     min_recall: float = MIN_RECALL) -> float:
    """Best precision among thresholds that keep recall >= min_recall."""
    y_true = np.asarray(y_true)
    y_score = np.asarray(y_score)
    if y_true.sum() == 0:
        raise ValueError("No positive cases in y_true")
    best_thr, best_prec = None, -1.0
    for thr in np.unique(np.round(y_score, 3)):
        pred = y_score >= thr
        tp = int((pred & (y_true == 1)).sum())
        recall = tp / y_true.sum()
        precision = tp / pred.sum() if pred.sum() else 0.0
        if recall >= min_recall and precision > best_prec:
            best_thr, best_prec = float(thr), precision
    if best_thr is None:
        raise ValueError(f"No threshold achieves recall >= {min_recall}")
    return best_thr


def classify(probability: float, threshold: float) -> RiskTier:
    """Map a risk probability to a human tier. Threshold splits alert/no-alert."""
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be in [0, 1]")
    if probability < min(0.15, threshold / 2):
        return RiskTier('Low', '#2e9e4f')
    if probability < threshold:
        return RiskTier('Moderate', '#e6a817')
    if probability < max(0.60, threshold + 0.15):
        return RiskTier('High', '#e05c2a')
    return RiskTier('Very High', '#c92a2a')
