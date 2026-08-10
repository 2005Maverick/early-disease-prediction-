/* Early Disease Prediction System — presentation deck.
   Build:  node make_deck.js   (from the deck/ directory)                  */
const pptxgen = require('pptxgenjs');

const INK = '1c1a17', WHITE = 'FFFFFF', OXBLOOD = '8e2f22', MOSS = '3a6b35',
      OCHRE = '9a6519', MUTED = '6b6156', LINE = 'd9cfbc', CARD = 'F6F2E9',
      PAPERTXT = 'faf6ef', SOFTRED = 'c9695c';
const HEAD = 'Cambria', BODY = 'Calibri';
const FIG = '../report/figures/', SCR = '../report/screens/';
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';

const shadow = () => ({ type: 'outer', color: '3a3128', blur: 8, offset: 2, angle: 90, opacity: 0.28 });

function title(slide, text, sub) {
  slide.addText(text, { x: 0.55, y: 0.32, w: W - 1.1, h: 0.75, fontFace: HEAD,
    fontSize: 30, bold: true, color: INK, margin: 0 });
  if (sub) slide.addText(sub, { x: 0.55, y: 1.02, w: W - 1.1, h: 0.4,
    fontFace: BODY, fontSize: 13, italic: true, color: MUTED, margin: 0 });
}
function circle(slide, x, y, d, label, fill) {
  slide.addShape('ellipse', { x, y, w: d, h: d, fill: { color: fill } });
  slide.addText(label, { x, y: y - 0.02, w: d, h: d, align: 'center',
    valign: 'middle', fontFace: HEAD, fontSize: d > 0.5 ? 16 : 13, bold: true,
    color: WHITE, margin: 0 });
}
function stat(slide, x, y, w, big, small, color) {
  slide.addText(big, { x, y, w, h: 0.85, fontFace: HEAD, fontSize: 40,
    bold: true, color, align: 'center', margin: 0 });
  slide.addText(small, { x, y: y + 0.85, w, h: 0.6, fontFace: BODY,
    fontSize: 11.5, color: MUTED, align: 'center', margin: 0 });
}

/* ---------- 1. TITLE (dark) ---------- */
{
  const s = pres.addSlide();
  s.background = { color: INK };
  s.addText('EARLY DISEASE PREDICTION SYSTEM', { x: 0.8, y: 1.0, w: W - 1.6,
    h: 0.4, fontFace: BODY, fontSize: 13, color: SOFTRED, charSpacing: 4,
    align: 'center', margin: 0 });
  s.addText('Risk Before Symptoms', { x: 0.8, y: 1.45, w: W - 1.6, h: 1.05,
    fontFace: HEAD, fontSize: 52, bold: true, color: PAPERTXT,
    align: 'center', margin: 0 });
  s.addText('Diabetes  ·  Heart Disease  —  with honest uncertainty, an independent second opinion, and a preventive plan',
    { x: 1.6, y: 2.55, w: W - 3.2, h: 0.55, fontFace: BODY, fontSize: 15,
      italic: true, color: 'c9c2b6', align: 'center', margin: 0 });

  const team = [
    ['Riyansh Choudhary', '500122039'], ['Pranav Singh Puri', '500122453'],
    ['Kartikya Yadav', '500122804'], ['Rudra', '500124508'],
    ['Sushant Jaiswal', '500123999']];
  const bw = 2.15, gap = 0.22, x0 = (W - (5 * bw + 4 * gap)) / 2;
  team.forEach(([n, id], i) => {
    const x = x0 + i * (bw + gap);
    s.addShape('roundRect', { x, y: 3.75, w: bw, h: 1.0, rectRadius: 0.07,
      fill: { color: '262019' }, line: { color: '4a4238', width: 0.75 } });
    s.addText(n, { x, y: 3.85, w: bw, h: 0.42, fontFace: BODY, fontSize: 12.5,
      bold: true, color: PAPERTXT, align: 'center', margin: 0 });
    s.addText('SAP ID ' + id, { x, y: 4.27, w: bw, h: 0.35, fontFace: BODY,
      fontSize: 10.5, color: '9a9284', align: 'center', margin: 0 });
  });
  s.addText([{ text: 'Mentor:  ', options: { bold: true, color: SOFTRED } },
             { text: 'Imran Khan', options: { color: PAPERTXT } }],
    { x: 0.8, y: 5.05, w: W - 1.6, h: 0.4, fontFace: BODY, fontSize: 14,
      align: 'center', margin: 0 });
  s.addText('Live:  healthpredictor092005.streamlit.app      Code:  github.com/2005Maverick/early-disease-prediction-',
    { x: 0.8, y: 6.55, w: W - 1.6, h: 0.4, fontFace: BODY, fontSize: 12,
      color: '9a9284', align: 'center', margin: 0 });
}

/* ---------- 2. PROBLEM & SOLUTION ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Problem Statement & Our Solution');
  const colW = (W - 1.1 - 0.5) / 2;
  // problem card
  s.addShape('roundRect', { x: 0.55, y: 1.55, w: colW, h: 5.35,
    rectRadius: 0.09, fill: { color: CARD }, shadow: shadow() });
  circle(s, 0.95, 1.95, 0.55, '!', INK);
  s.addText('The Problem', { x: 1.7, y: 1.98, w: colW - 1.4, h: 0.5,
    fontFace: HEAD, fontSize: 20, bold: true, color: INK, margin: 0 });
  s.addText([
    { text: 'Diabetes and heart disease develop silently for years — but early lifestyle intervention cuts diabetes incidence by 58% (DPP trial).', options: { bullet: true, breakLine: true } },
    { text: 'Typical ML prototypes output a single risk number with no statement of confidence — the user cannot tell 84% they should trust from 84% they should not.', options: { bullet: true, breakLine: true } },
    { text: 'Most projects report accuracy on data the model partially saw, and silently feed the Pima dataset’s impossible zeros in as real measurements.', options: { bullet: true } },
  ], { x: 0.95, y: 2.75, w: colW - 0.8, h: 3.9, fontFace: BODY, fontSize: 14,
    color: INK, paraSpaceAfter: 14, margin: 0 });
  // solution card
  const x2 = 0.55 + colW + 0.5;
  s.addShape('roundRect', { x: x2, y: 1.55, w: colW, h: 5.35,
    rectRadius: 0.09, fill: { color: WHITE }, line: { color: OXBLOOD, width: 1.25 }, shadow: shadow() });
  circle(s, x2 + 0.4, 1.95, 0.55, '✓', OXBLOOD);
  s.addText('Our Solution', { x: x2 + 1.15, y: 1.98, w: colW - 1.4, h: 0.5,
    fontFace: HEAD, fontSize: 20, bold: true, color: OXBLOOD, margin: 0 });
  s.addText([
    { text: 'An Uncertainty Engine — 200 bootstrap-trained models produce a risk distribution per patient, whose spread is honest confidence.', options: { bullet: true, breakLine: true } },
    { text: 'Patients Like You — a model-free 50-nearest-neighbour second opinion; agreement between independent methods builds trust.', options: { bullet: true, breakLine: true } },
    { text: 'Every metric strictly out-of-fold; the alert threshold derived from a stated clinical rule (recall ≥ 85%).', options: { bullet: true, breakLine: true } },
    { text: 'Explanations and a guideline-based preventive plan turn the score into action.', options: { bullet: true } },
  ], { x: x2 + 0.4, y: 2.75, w: colW - 0.8, h: 3.9, fontFace: BODY,
    fontSize: 14, color: INK, paraSpaceAfter: 12, margin: 0 });
}

/* ---------- 3. LITERATURE REVIEW ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Literature Review',
    'Four strands of prior work shaped the design.');
  const rows = [
    ['Grinsztajn, Oyallon & Varoquaux (2022, NeurIPS)',
     'Why tree-based models still outperform deep learning on typical tabular data — justifies gradient boosting as our base learner at 768 / 303 patients.'],
    ['Efron (1979)  ·  Breiman (1996)',
     'The bootstrap and bagging — training many models on resamples. We keep the averaged prediction for accuracy and expose the full spread as per-patient uncertainty.'],
    ['Cover & Hart (1967)',
     'Nearest-neighbour pattern classification — the oldest idea in the field becomes our model-free second opinion and a case-based explanation clinicians find natural.'],
    ['Diabetes Prevention Program (2002, NEJM)',
     'Lifestyle intervention cut type-2 diabetes incidence by 58% — the clinical evidence that early, actionable prediction is worth building.'],
  ];
  rows.forEach(([head, body], i) => {
    const y = 1.62 + i * 1.32;
    circle(s, 0.62, y + 0.1, 0.5, String(i + 1), OXBLOOD);
    s.addText(head, { x: 1.35, y, w: W - 2.0, h: 0.42, fontFace: HEAD,
      fontSize: 15.5, bold: true, color: INK, margin: 0 });
    s.addText(body, { x: 1.35, y: y + 0.42, w: W - 2.0, h: 0.8,
      fontFace: BODY, fontSize: 13, color: MUTED, margin: 0 });
  });
}

/* ---------- 4. DATA ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'The Data',
    'Two classical clinical study datasets — and the trap most projects fall into.');
  const cw = 3.85;
  const card = (x, name, src, rows) => {
    s.addShape('roundRect', { x, y: 1.6, w: cw, h: 3.0, rectRadius: 0.09,
      fill: { color: CARD }, shadow: shadow() });
    s.addText(name, { x: x + 0.3, y: 1.82, w: cw - 0.6, h: 0.45,
      fontFace: HEAD, fontSize: 19, bold: true, color: OXBLOOD, margin: 0 });
    s.addText(src, { x: x + 0.3, y: 2.26, w: cw - 0.6, h: 0.35,
      fontFace: BODY, fontSize: 11, italic: true, color: MUTED, margin: 0 });
    s.addText(rows.map((t, i) => ({ text: t,
      options: { bullet: true, breakLine: i < rows.length - 1 } })),
      { x: x + 0.3, y: 2.68, w: cw - 0.6, h: 1.8, fontFace: BODY,
        fontSize: 12.5, color: INK, paraSpaceAfter: 7, margin: 0 });
  };
  card(0.55, 'Diabetes', 'Pima study — NIDDK',
    ['768 patients, 8 features', 'glucose, BMI, insulin, age, family history…', '34.9% developed the disease']);
  card(0.55 + cw + 0.4, 'Heart disease', 'Cleveland Clinic — UCI',
    ['303 patients, 13 features', 'cholesterol, max heart rate, ST depression…', '45.9% diagnosed with disease']);
  // hidden zeros callout
  const x3 = 0.55 + 2 * (cw + 0.4);
  s.addShape('roundRect', { x: x3, y: 1.6, w: W - x3 - 0.55, h: 3.0,
    rectRadius: 0.09, fill: { color: INK }, shadow: shadow() });
  s.addText('374 / 768', { x: x3, y: 1.85, w: W - x3 - 0.55, h: 0.8,
    fontFace: HEAD, fontSize: 40, bold: true, color: SOFTRED,
    align: 'center', margin: 0 });
  s.addText('Pima patients with a physiologically impossible ZERO recorded for insulin — hidden missing data most projects feed to the model as real.',
    { x: x3 + 0.3, y: 2.72, w: W - x3 - 1.15, h: 1.6, fontFace: BODY,
      fontSize: 12.5, color: PAPERTXT, align: 'center', margin: 0 });
  s.addImage({ path: FIG + 'missingness.png', x: 2.3, y: 4.85, w: 8.7, h: 2.32,
    shadow: shadow() });
}

/* ---------- 5. ARCHITECTURE ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'System Architecture',
    'Train once offline; serve per patient online. Nothing is predicted until the user asks.');
  s.addImage({ path: FIG + 'arch_system.png', x: 1.29, y: 1.55, w: 10.75, h: 5.6,
    shadow: shadow() });
}

/* ---------- 6. DEEP DIVE I — UNCERTAINTY ENGINE ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Deep Dive I — The Uncertainty Engine');
  s.addImage({ path: FIG + 'arch_ensemble.png', x: 0.55, y: 1.62, w: 8.1, h: 3.28,
    shadow: shadow() });
  const x2 = 8.95, w2 = W - x2 - 0.55;
  s.addShape('roundRect', { x: x2, y: 1.62, w: w2, h: 3.28, rectRadius: 0.09,
    fill: { color: CARD } });
  s.addText('Configuration', { x: x2 + 0.25, y: 1.78, w: w2 - 0.5, h: 0.4,
    fontFace: HEAD, fontSize: 15, bold: true, color: INK, margin: 0 });
  s.addText([
    { text: 'Members:  200 pipelines', options: { breakLine: true } },
    { text: 'Each:  impute → scale → boosting', options: { breakLine: true } },
    { text: 'Trees:  100 per member, depth 3', options: { breakLine: true } },
    { text: 'Training:  bootstrap resamples', options: { breakLine: true } },
    { text: 'Seeds:  42 – 241', options: { breakLine: true } },
    { text: 'Hyperparameters:  library defaults', options: {} },
  ], { x: x2 + 0.25, y: 2.2, w: w2 - 0.5, h: 2.5, fontFace: BODY,
    fontSize: 12.5, color: INK, paraSpaceAfter: 8, margin: 0 });
  s.addText([{ text: 'Why chosen.  ', options: { bold: true, color: OXBLOOD } },
    { text: 'Gradient-boosted trees are the strongest learners at this data scale; bootstrapping 200 of them turns one opinion into a distribution. Deliberately untuned — with ~600 training rows per fold, aggressive tuning fits noise, so evaluation integrity was prioritised over a possible extra AUC point.', options: { color: INK } }],
    { x: 0.55, y: 5.15, w: W - 1.1, h: 1.15, fontFace: BODY, fontSize: 14,
      margin: 0 });
  s.addText('“We ask 200 slightly different models and plot all their answers.”',
    { x: 0.55, y: 6.45, w: W - 1.1, h: 0.5, fontFace: HEAD, fontSize: 16,
      italic: true, color: OXBLOOD, align: 'center', margin: 0 });
}

/* ---------- 7. DEEP DIVE II — RISK DISTRIBUTION ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Deep Dive II — A Distribution, Not a Number');
  s.addImage({ path: FIG + 'dist_examples.png', x: 0.85, y: 1.6, w: 11.6, h: 3.85,
    shadow: shadow() });
  stat(s, 1.6, 5.7, 3.2, '1–2%', 'band width when the 200 models agree\n(clear low-risk patient)', MOSS);
  stat(s, 5.05, 5.7, 3.2, '65–96%', 'band width for an ambiguous patient —\nthe system says so, visibly', OCHRE);
  stat(s, 8.5, 5.7, 3.2, '90%', 'confidence band shown with every\nsingle assessment', OXBLOOD);
}

/* ---------- 8. DEEP DIVE III — PATIENTS LIKE YOU ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Deep Dive III — Patients Like You');
  s.addImage({ path: SCR + 'diab_similar.png', x: 0.55, y: 1.6, w: 7.9, h: 4.1,
    shadow: shadow() });
  const x2 = 8.85, w2 = W - x2 - 0.55;
  s.addText([
    { text: 'No model at all.  ', options: { bold: true, color: OXBLOOD, breakLine: true } },
    { text: 'Standardize every feature, find the 50 most similar patients in the study, report how many actually developed the disease.', options: { breakLine: true } },
  ], { x: x2, y: 1.7, w: w2, h: 1.9, fontFace: BODY, fontSize: 14, color: INK,
    paraSpaceAfter: 8, margin: 0 });
  s.addText([
    { text: 'Because it shares no machinery with the ensemble, agreement is real evidence — and disagreement flags an unusual patient, exactly when caution is right. The interface states which case applies.', options: {} },
  ], { x: x2, y: 3.5, w: w2, h: 2.1, fontFace: BODY, fontSize: 14,
    color: INK, margin: 0 });
  s.addText('Example: 84.8% (ensemble)  vs  78% (similar patients) — methods agree.',
    { x: 0.55, y: 6.05, w: W - 1.1, h: 0.5, fontFace: HEAD, fontSize: 15,
      italic: true, color: MOSS, align: 'center', margin: 0 });
}

/* ---------- 9. DEEP DIVE IV — THRESHOLD RULE ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Deep Dive IV — The Alert Threshold Is a Stated Rule');
  s.addImage({ path: FIG + 'threshold_rule.png', x: 0.85, y: 1.6, w: 11.6, h: 4.38,
    shadow: shadow() });
  s.addText([{ text: 'Rule:  ', options: { bold: true, color: OXBLOOD } },
    { text: 'among all thresholds with out-of-fold recall ≥ 85% — never miss more than 15% of true future patients — choose the one with the best precision.  Result: alert at 23.8% (diabetes) and 27.3% (heart disease). The rule and its consequence are shown inside the application.', options: { color: INK } }],
    { x: 0.85, y: 6.2, w: 11.6, h: 1.0, fontFace: BODY, fontSize: 14, margin: 0 });
}

/* ---------- 10. RESULTS I — BENCHMARK ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Results I — Model Benchmark',
    'Four models, identical folds, every number out-of-fold. ROC AUC shown; full table in the report.');
  s.addChart('bar', [
    { name: 'Diabetes',
      labels: ['Uncertainty\nEnsemble', 'Logistic\nRegression', 'Random\nForest', 'Gradient\nBoosting'],
      values: [83.5, 83.5, 83.3, 82.6] },
    { name: 'Heart disease',
      labels: ['Uncertainty\nEnsemble', 'Logistic\nRegression', 'Random\nForest', 'Gradient\nBoosting'],
      values: [90.0, 90.9, 91.2, 88.5] },
  ], {
    x: 0.55, y: 1.75, w: 7.6, h: 4.6,
    chartColors: [OXBLOOD, MOSS],
    showValue: true, dataLabelPosition: 'outEnd', dataLabelFontFace: BODY,
    dataLabelFontSize: 10, dataLabelColor: INK, dataLabelFormatCode: '0.0',
    valAxisMinVal: 75, valAxisMaxVal: 95,
    catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
    catAxisLabelFontFace: BODY, valAxisLabelFontFace: BODY,
    catAxisLabelFontSize: 10, valAxisLabelFontSize: 10,
    valGridLine: { color: 'e5ddcc', size: 0.5 },
    catGridLine: { style: 'none' },
    showLegend: true, legendPos: 'b', legendFontFace: BODY, legendFontSize: 11,
    showTitle: true, title: 'ROC AUC (%) — out-of-fold, 5-fold CV',
    titleFontFace: HEAD, titleFontSize: 13, titleColor: INK,
    barGapWidthPct: 60,
  });
  const x2 = 8.6, w2 = W - x2 - 0.55;
  stat(s, x2, 1.8, w2, '85%+', 'recall on both diseases —\nby construction, not by luck', OXBLOOD);
  stat(s, x2, 3.5, w2, '90.0', 'heart-disease ROC AUC of the\ndeployed ensemble', MOSS);
  s.addText('Honest note: on the smaller Cleveland data, simpler baselines edge ahead by ~1 AUC point. The ensemble still wins deployment — it is the only model that also outputs trustworthy uncertainty (next slide).',
    { x: x2, y: 5.15, w: w2, h: 1.9, fontFace: BODY, fontSize: 12.5,
      italic: true, color: MUTED, margin: 0 });
}

/* ---------- 11. RESULTS II — UNCERTAINTY IS INFORMATIVE ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'Results II — The System Knows When It Does Not Know');
  s.addImage({ path: FIG + 'uncertainty_error.png', x: 0.7, y: 1.55, w: 8.35, h: 2.97,
    shadow: shadow() });
  s.addImage({ path: FIG + 'calibration.png', x: 0.7, y: 4.72, w: 6.7, h: 2.53,
    shadow: shadow() });
  stat(s, 9.35, 1.7, 3.4, '6% → 43%', 'error rate, narrowest to widest\nconfidence bands (diabetes)', OXBLOOD);
  stat(s, 9.35, 3.4, 3.4, '4% → 46%', 'the same effect on\nheart disease', OCHRE);
  s.addText('Calibrated too: patients told “about 30% risk” develop the disease about 30% of the time (bottom).',
    { x: 7.75, y: 5.35, w: 5.0, h: 1.5, fontFace: BODY, fontSize: 13,
      color: INK, margin: 0 });
}

/* ---------- 12. LIVE DASHBOARD ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'The Live Dashboard',
    'Deployed and public — a gated flow: intake form → Run assessment → report. No phantom predictions.');
  s.addImage({ path: SCR + 'diab_findings.png', x: 0.55, y: 1.65, w: 6.05, h: 3.7,
    shadow: shadow() });
  s.addImage({ path: SCR + 'heart_findings.png', x: 6.85, y: 1.65, w: 5.95, h: 3.0,
    shadow: shadow() });
  s.addText('One engine, two diseases — same interface serving the diabetes (left) and heart-disease (right) models.',
    { x: 6.85, y: 4.8, w: 5.9, h: 0.9, fontFace: BODY, fontSize: 12.5,
      color: MUTED, margin: 0 });
  s.addShape('roundRect', { x: 2.9, y: 5.85, w: 7.5, h: 0.95, rectRadius: 0.1,
    fill: { color: INK }, shadow: shadow() });
  s.addText('healthpredictor092005.streamlit.app', { x: 2.9, y: 5.85, w: 7.5,
    h: 0.95, fontFace: HEAD, fontSize: 20, bold: true, color: PAPERTXT,
    align: 'center', valign: 'middle', margin: 0 });
}

/* ---------- 13. SWOT ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'SWOT Analysis');
  const qw = (W - 1.1 - 0.4) / 2, qh = 2.62;
  const quads = [
    ['Strengths', MOSS, 0.55, 1.55, [
      'Every metric out-of-fold; probabilities calibrated',
      'Uncertainty demonstrably informative (6% → 43% error)',
      'Two independent methods cross-check each other',
      'Deployed, tested (15 tests), reproducible figures']],
    ['Weaknesses', OCHRE, 0.55 + qw + 0.4, 1.55, [
      'Small, decades-old cohorts (768 / 303 patients)',
      'No external validation on a modern population',
      'Bootstrap bands capture sampling uncertainty only',
      'What-if is model response, not causal effect']],
    ['Opportunities', OXBLOOD, 0.55, 1.55 + qh + 0.35, [
      'Third disease = one config file + retrain (registry design)',
      'Conformal prediction for formal coverage guarantees',
      'External validation on modern cohorts (e.g. NHANES)',
      'Longitudinal mode: track risk across assessments']],
    ['Threats', INK, 0.55 + qw + 0.4, 1.55 + qh + 0.35, [
      'Not clinically validated — must not drive real decisions',
      'Cohort bias limits transfer across populations',
      'Users may over-trust a polished interface — mitigated by visible uncertainty and in-product disclaimers']],
  ];
  quads.forEach(([name, color, x, y, items]) => {
    s.addShape('roundRect', { x, y, w: qw, h: qh, rectRadius: 0.09,
      fill: { color: CARD }, shadow: shadow() });
    s.addText(name, { x: x + 0.28, y: y + 0.14, w: qw - 0.56, h: 0.42,
      fontFace: HEAD, fontSize: 16, bold: true, color, margin: 0 });
    s.addText(items.map((t, i) => ({ text: t,
      options: { bullet: true, breakLine: i < items.length - 1 } })),
      { x: x + 0.28, y: y + 0.6, w: qw - 0.56, h: qh - 0.75, fontFace: BODY,
        fontSize: 11.5, color: INK, paraSpaceAfter: 5, margin: 0 });
  });
}

/* ---------- 14. REFERENCES ---------- */
{
  const s = pres.addSlide();
  s.background = { color: WHITE };
  title(s, 'References');
  const refs1 = [
    '[1] L. Breiman, “Bagging predictors,” Machine Learning, 24(2), 1996.',
    '[2] J. H. Friedman, “Greedy function approximation: a gradient boosting machine,” Annals of Statistics, 29(5), 2001.',
    '[3] L. Grinsztajn, E. Oyallon, G. Varoquaux, “Why do tree-based models still outperform deep learning on typical tabular data?,” NeurIPS, 2022.',
    '[4] B. Efron, “Bootstrap methods: another look at the jackknife,” Annals of Statistics, 7(1), 1979.',
    '[5] T. Cover, P. Hart, “Nearest neighbor pattern classification,” IEEE Trans. Information Theory, 13(1), 1967.'];
  const refs2 = [
    '[6] J. W. Smith et al., “Using the ADAP learning algorithm to forecast the onset of diabetes mellitus,” Proc. SCAMC, 1988.',
    '[7] R. Detrano et al., “International application of a new probability algorithm for the diagnosis of coronary artery disease,” Am. J. Cardiology, 64(5), 1989.',
    '[8] Diabetes Prevention Program Research Group, “Reduction in the incidence of type 2 diabetes…,” NEJM, 346(6), 2002.',
    '[9] A. Niculescu-Mizil, R. Caruana, “Predicting good probabilities with supervised learning,” ICML, 2005.',
    '[10] F. Pedregosa et al., “Scikit-learn: machine learning in Python,” JMLR, 12, 2011.'];
  const opts = { fontFace: BODY, fontSize: 12, color: INK, paraSpaceAfter: 12, margin: 0 };
  s.addText(refs1.map((t, i) => ({ text: t, options: { breakLine: i < refs1.length - 1 } })),
    { x: 0.55, y: 1.7, w: 6.0, h: 5.3, ...opts });
  s.addText(refs2.map((t, i) => ({ text: t, options: { breakLine: i < refs2.length - 1 } })),
    { x: 6.9, y: 1.7, w: 6.0, h: 5.3, ...opts });
}

/* ---------- 15. THANK YOU (dark) ---------- */
{
  const s = pres.addSlide();
  s.background = { color: INK };
  s.addText('Thank You', { x: 0.8, y: 2.2, w: W - 1.6, h: 1.1, fontFace: HEAD,
    fontSize: 54, bold: true, color: PAPERTXT, align: 'center', margin: 0 });
  s.addText('Questions & Discussion', { x: 0.8, y: 3.35, w: W - 1.6, h: 0.6,
    fontFace: BODY, fontSize: 20, italic: true, color: SOFTRED,
    align: 'center', margin: 0 });
  s.addText('Early Disease Prediction System  ·  Diabetes & Heart Disease  ·  200 models, honest uncertainty',
    { x: 0.8, y: 4.3, w: W - 1.6, h: 0.5, fontFace: BODY, fontSize: 14,
      color: 'c9c2b6', align: 'center', margin: 0 });
  s.addText('Try it live:  healthpredictor092005.streamlit.app',
    { x: 0.8, y: 5.15, w: W - 1.6, h: 0.5, fontFace: HEAD, fontSize: 17,
      bold: true, color: PAPERTXT, align: 'center', margin: 0 });
}

pres.writeFile({ fileName: 'Early_Disease_Prediction_System.pptx' })
  .then(() => console.log('deck written'));
