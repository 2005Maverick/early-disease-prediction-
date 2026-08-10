"""Generate every result figure in the report from the real artifacts.

Run from the project root:
    .venv\\Scripts\\python.exe report\\make_figures.py

Recomputes honest out-of-fold scores (same folds as training) for all four
models and both diseases, then renders styled figures to report/figures/.
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (auc, confusion_matrix, precision_recall_curve,
                             roc_curve)
from sklearn.model_selection import StratifiedKFold

from edp.data import load_clean, load_raw, mark_missing
from edp.diseases import REGISTRY
from edp.drivers import compute_drivers
from edp.ensemble import UncertaintyEnsemble
from edp.pipeline import build_baselines
from edp.whatif import evaluate_scenarios

FIG_DIR = PROJECT_ROOT / 'report' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ---- Lab Report palette on print-white ----
INK = '#1c1a17'
OXBLOOD = '#8e2f22'
MOSS = '#3a6b35'
OCHRE = '#9a6519'
BLUE = '#2b4a6f'
MUTED = '#6b6156'
LINE = '#d9cfbc'
MODEL_COLORS = {'Uncertainty Ensemble': OXBLOOD, 'Logistic Regression': BLUE,
                'Random Forest': MOSS, 'Gradient Boosting': OCHRE}

plt.rcParams.update({
    'font.family': 'serif', 'font.serif': ['Georgia', 'DejaVu Serif'],
    'font.size': 10, 'axes.titlesize': 11, 'axes.labelsize': 10,
    'axes.edgecolor': INK, 'axes.linewidth': 0.8,
    'axes.grid': True, 'grid.color': LINE, 'grid.linewidth': 0.5,
    'figure.facecolor': 'white', 'savefig.dpi': 200,
    'savefig.bbox': 'tight', 'legend.frameon': False,
})

CV_MEMBERS = 40
DEMO = {  # example patients used in narrative figures
    'diabetes': {'high': [2, 190, 70, np.nan, 100, 40.0, 0.4, 55],
                 'low': [2, 85, 70, np.nan, 100, 21.0, 0.4, 25]},
}


def oof_scores(config):
    """OOF mean scores for all 4 models + ensemble member matrix (for widths)."""
    X, y = load_clean(config, PROJECT_ROOT)
    y_arr = y.to_numpy()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    means = {name: np.zeros(len(y)) for name in
             ['Uncertainty Ensemble', *build_baselines()]}
    members = np.zeros((CV_MEMBERS, len(y)))
    for fold, (tr, te) in enumerate(cv.split(X, y)):
        ens = UncertaintyEnsemble(n_members=CV_MEMBERS, random_state=42 + fold)
        ens.fit(X.iloc[tr], y.iloc[tr])
        dist = ens.predict_dist(X.iloc[te])
        members[:, te] = dist
        means['Uncertainty Ensemble'][te] = dist.mean(axis=0)
        for name, model in build_baselines().items():
            model.fit(X.iloc[tr], y.iloc[tr])
            means[name][te] = model.predict_proba(X.iloc[te])[:, 1]
        print(f"  {config.key} fold {fold + 1}/5")
    return X, y_arr, means, members


def fig_missingness(datas):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    for ax, (config, _, _, _, _) in zip(axes, datas):
        raw = mark_missing(load_raw(config, PROJECT_ROOT), config)
        counts = raw[list(config.features)].isna().sum()
        counts = counts[counts > 0].sort_values()
        labels = [config.friendly.get(c, c) for c in counts.index]
        if counts.empty:
            counts = pd.Series([0]); labels = ['(none)']
        ax.barh(labels, counts.values, color=OXBLOOD, height=0.6)
        for i, v in enumerate(counts.values):
            ax.text(v + max(counts.values) * 0.01, i, str(int(v)),
                    va='center', fontsize=9, color=MUTED)
        ax.set_title(f'{config.name} — hidden missing values')
        ax.set_xlabel('patients affected')
        ax.grid(axis='y', visible=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'missingness.png')
    plt.close(fig)


def fig_eda(config, X, y):
    cols = [c for c, _ in config.similar_axes] + \
           [c for c, _ in config.strip_fields if c not in
            [a for a, _ in config.similar_axes]][:2]
    cols = cols[:4]
    fig, axes = plt.subplots(1, len(cols), figsize=(9.5, 2.8))
    for ax, col in zip(axes, cols):
        for outcome, color, label in ((0, MOSS, 'healthy'),
                                      (1, OXBLOOD, 'developed disease')):
            vals = X[col][y == outcome].dropna()
            ax.hist(vals, bins=20, alpha=0.55, color=color, label=label,
                    density=True)
        ax.set_title(config.friendly.get(col, col), fontsize=10)
        ax.set_yticks([])
    axes[0].legend(fontsize=8, loc='upper right')
    fig.suptitle(f'{config.name}: feature distributions by outcome', y=1.04)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f'eda_{config.key}.png')
    plt.close(fig)


def fig_curves(datas, kind):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    for ax, (config, X, y, means, _) in zip(axes, datas):
        for name, score in means.items():
            if kind == 'roc':
                xs, ys, _ = roc_curve(y, score)
                label = f'{name} (AUC {auc(xs, ys):.3f})'
            else:
                p, r, _ = precision_recall_curve(y, score)
                xs, ys = r, p
                label = name
            ax.plot(xs, ys, color=MODEL_COLORS[name], lw=1.6, label=label)
        if kind == 'roc':
            ax.plot([0, 1], [0, 1], ls='--', c=MUTED, lw=0.8)
            ax.set_xlabel('False positive rate'); ax.set_ylabel('True positive rate')
        else:
            ax.axhline(y.mean(), ls='--', c=MUTED, lw=0.8)
            ax.set_xlabel('Recall'); ax.set_ylabel('Precision')
        ax.set_title(config.name)
        ax.legend(fontsize=7.5, loc='lower right' if kind == 'roc' else 'lower left')
    fig.tight_layout()
    fig.savefig(FIG_DIR / f'{kind}.png')
    plt.close(fig)


def fig_confusion(datas):
    fig, axes = plt.subplots(2, 4, figsize=(9.5, 5))
    for row, (config, X, y, means, _) in enumerate(datas):
        thr = json.loads((PROJECT_ROOT / 'models' / config.key /
                          'metrics.json').read_text())['threshold']
        for col, (name, score) in enumerate(means.items()):
            ax = axes[row][col]
            cm = confusion_matrix(y, (score >= thr).astype(int))
            ax.imshow(cm, cmap='Reds', vmin=0)
            for (i, j), v in np.ndenumerate(cm):
                ax.text(j, i, str(v), ha='center', va='center', fontsize=10,
                        color=INK if v < cm.max() * 0.6 else 'white')
            ax.set_xticks([0, 1], ['pred 0', 'pred 1'], fontsize=8)
            ax.set_yticks([0, 1], ['true 0', 'true 1'], fontsize=8)
            ax.set_title(f'{name}\n({config.name})', fontsize=8.5)
            ax.grid(visible=False)
    fig.suptitle('Confusion matrices at each disease\'s alert threshold', y=1.0)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'confusion.png')
    plt.close(fig)


def fig_threshold_rule(datas):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, (config, X, y, means, _) in zip(axes, datas):
        report = json.loads((PROJECT_ROOT / 'models' / config.key /
                             'metrics.json').read_text())
        score = means['Uncertainty Ensemble']
        thrs = np.linspace(0.01, 0.9, 200)
        precs, recs = [], []
        for t in thrs:
            pred = score >= t
            tp = (pred & (y == 1)).sum()
            precs.append(tp / pred.sum() if pred.sum() else 1.0)
            recs.append(tp / y.sum())
        ax.plot(thrs, recs, color=OXBLOOD, lw=1.6, label='Recall')
        ax.plot(thrs, precs, color=BLUE, lw=1.6, label='Precision')
        ax.axhline(0.85, ls=':', c=MUTED, lw=1)
        ax.text(0.62, 0.865, 'recall floor 85%', fontsize=8, color=MUTED)
        chosen = report['threshold']
        ax.axvline(chosen, ls='--', c=INK, lw=1)
        ax.text(chosen + 0.015, 0.06, f'chosen {chosen:.3f}', fontsize=8,
                color=INK, rotation=90)
        ax.set_xlabel('Decision threshold'); ax.set_ylabel('Metric value')
        ax.set_ylim(0, 1.02)
        ax.set_title(config.name)
        ax.legend(fontsize=8, loc='center right')
    fig.suptitle('The alert threshold is a stated rule, not a magic number', y=1.03)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'threshold_rule.png')
    plt.close(fig)


def fig_calibration(datas):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, (config, X, y, means, _) in zip(axes, datas):
        score = means['Uncertainty Ensemble']
        order = np.argsort(score)
        bins = np.array_split(order, 10)
        pred = [score[b].mean() * 100 for b in bins]
        obs = [y[b].mean() * 100 for b in bins]
        ax.plot([0, 100], [0, 100], ls='--', c=MUTED, lw=0.8)
        ax.plot(pred, obs, 'o-', color=OXBLOOD, ms=5, lw=1.4)
        ax.set_xlabel('Mean predicted risk (%)')
        ax.set_ylabel('Observed disease rate (%)')
        ax.set_title(config.name)
        ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    fig.suptitle('Calibration: predicted risk vs what actually happened '
                 '(out-of-fold deciles)', y=1.03)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'calibration.png')
    plt.close(fig)


def fig_uncertainty_error(datas):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.2))
    for ax, (config, X, y, means, members) in zip(axes, datas):
        thr = json.loads((PROJECT_ROOT / 'models' / config.key /
                          'metrics.json').read_text())['threshold']
        width = np.percentile(members, 95, axis=0) - \
            np.percentile(members, 5, axis=0)
        pred = (means['Uncertainty Ensemble'] >= thr).astype(int)
        err = (pred != y).astype(int)
        qs = np.quantile(width, [0, .25, .5, .75, 1.0])
        rates, labels = [], []
        for lo, hi, lab in zip(qs[:-1], qs[1:], ['narrowest', 'narrow',
                                                 'wide', 'widest']):
            mask = (width >= lo) & (width <= hi)
            rates.append(err[mask].mean() * 100)
            labels.append(lab)
        ax.bar(labels, rates, color=[MOSS, OCHRE, '#b3471f', OXBLOOD],
               width=0.62)
        for i, v in enumerate(rates):
            ax.text(i, v + 0.6, f'{v:.0f}%', ha='center', fontsize=9,
                    color=MUTED)
        ax.set_ylabel('Error rate (%)')
        ax.set_xlabel('Confidence-band width (quartiles)')
        ax.set_title(config.name)
        ax.grid(axis='x', visible=False)
    fig.suptitle('The system knows when it does not know: wider bands, '
                 'more mistakes', y=1.04)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'uncertainty_error.png')
    plt.close(fig)


def fig_patient_figures():
    """Risk distributions, drivers and what-if for the demo diabetes patients."""
    config = REGISTRY['diabetes']
    ens = joblib.load(PROJECT_ROOT / 'models' / 'diabetes' / 'ensemble.pkl')
    report = json.loads((PROJECT_ROOT / 'models' / 'diabetes' /
                         'metrics.json').read_text())
    thr = report['threshold']
    hi = pd.DataFrame([DEMO['diabetes']['high']], columns=list(config.features))
    lo = pd.DataFrame([DEMO['diabetes']['low']], columns=list(config.features))
    d_hi = ens.predict_dist(hi)[:, 0]
    d_lo = ens.predict_dist(lo)[:, 0]

    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    for ax, d, title in ((axes[0], d_lo, 'Low-risk patient — models agree'),
                         (axes[1], d_hi, 'High-risk patient — honest spread')):
        ax.hist(d * 100, bins=np.arange(0, 102, 2.5), color=OXBLOOD, alpha=0.9)
        ax.axvline(d.mean() * 100, c=INK, lw=1.6)
        ax.axvline(thr * 100, c=MUTED, ls='--', lw=1.2)
        ax.set_xlim(0, 100)
        ax.set_title(f'{title}\nmean {d.mean() * 100:.1f}% · band '
                     f'{np.percentile(d, 5) * 100:.0f}–'
                     f'{np.percentile(d, 95) * 100:.0f}%', fontsize=9.5)
        ax.set_xlabel('Predicted risk (%)'); ax.set_ylabel('Models')
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'dist_examples.png')
    plt.close(fig)

    medians = pd.Series(report['population_medians'])
    drivers = compute_drivers(ens.predict_mean, hi, medians)
    drivers = [d for d in drivers if abs(d.risk_delta) >= 0.005]
    fig, ax = plt.subplots(figsize=(7, 2.8))
    names = [config.friendly.get(d.feature, d.feature) for d in drivers][::-1]
    deltas = [d.risk_delta * 100 for d in drivers][::-1]
    ax.barh(names, deltas, color=[OXBLOOD if v > 0 else MOSS for v in deltas],
            height=0.6)
    ax.axvline(0, c=INK, lw=0.8)
    ax.set_xlabel('Adds to risk (percentage points)')
    ax.set_title('Personal risk drivers — high-risk example patient')
    ax.grid(axis='y', visible=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'drivers_example.png')
    plt.close(fig)

    scenarios = config.build_scenarios(hi)
    results = evaluate_scenarios(ens.predict_mean, hi, scenarios)
    fig, ax = plt.subplots(figsize=(7, 2.6))
    labels = [r.label for r in results][::-1]
    deltas = [r.risk_delta * 100 for r in results][::-1]
    ax.barh(labels, deltas, color=[MOSS if v < 0 else OXBLOOD for v in deltas],
            height=0.6)
    ax.axvline(0, c=INK, lw=0.8)
    ax.set_xlabel('Risk change (percentage points)')
    ax.set_title('What-if scenarios — same patient, one change at a time')
    ax.grid(axis='y', visible=False)
    fig.tight_layout()
    fig.savefig(FIG_DIR / 'whatif_example.png')
    plt.close(fig)


def main() -> None:
    datas = []
    for config in REGISTRY.values():
        print(f'OOF for {config.name}...')
        X, y, means, members = oof_scores(config)
        datas.append((config, X, y, means, members))

    fig_missingness(datas)
    for config, X, y, _, _ in datas:
        fig_eda(config, X, pd.Series(y))
    fig_curves(datas, 'roc')
    fig_curves(datas, 'pr')
    fig_confusion(datas)
    fig_threshold_rule(datas)
    fig_calibration(datas)
    fig_uncertainty_error(datas)
    fig_patient_figures()
    print('Figures written to', FIG_DIR)
    for p in sorted(FIG_DIR.glob('*.png')):
        print(' ', p.name)


if __name__ == '__main__':
    main()
