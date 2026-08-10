/* Presentation script as a Word document.
   Build:  node make_script_docx.js   (from the deck/ directory)          */
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
        Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
        Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

const INK = '1C1A17', OXBLOOD = '8E2F22', MUTED = '6B6156', MOSS = '3A6B35';

const p = (children, opts = {}) => new Paragraph({ children, ...opts });
const t = (text, opts = {}) => new TextRun({ text, font: 'Calibri', size: 22, color: INK, ...opts });

function speakerHeading(name, slides, theme) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 420, after: 120 },
    children: [
      new TextRun({ text: name, font: 'Cambria', size: 32, bold: true, color: OXBLOOD }),
      new TextRun({ text: `   —   Slides ${slides}  ·  ${theme}`, font: 'Cambria', size: 24, color: MUTED }),
    ],
  });
}
function slideHeading(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 260, after: 80 },
    children: [new TextRun({ text, font: 'Cambria', size: 26, bold: true, color: INK })],
  });
}
function speech(runs) {
  return new Paragraph({
    spacing: { after: 140, line: 300 },
    indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 6, color: 'D9CFBC', space: 12 } },
    children: runs.map(r => typeof r === 'string'
      ? t(r)
      : new TextRun({ font: 'Calibri', size: 22, color: INK, ...r })),
  });
}
const direction = (text) => ({ text, italics: true, color: MUTED });
const strong = (text) => ({ text, bold: true });

const S = [];

/* ---------- title block ---------- */
S.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60 },
  children: [new TextRun({ text: 'Presentation Script', font: 'Cambria', size: 52, bold: true, color: INK })],
}));
S.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 60 },
  children: [new TextRun({ text: 'Early Disease Prediction System — 15 slides · 5 speakers · ~13 minutes', font: 'Cambria', size: 26, italics: true, color: OXBLOOD })],
}));
S.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 320 },
  children: [new TextRun({ text: 'Handovers are written in. Don’t read slides aloud — the script says what the slide doesn’t.', font: 'Calibri', size: 21, color: MUTED })],
}));

/* ---------- Riyansh ---------- */
S.push(speakerHeading('RIYANSH CHOUDHARY', '1–3', 'the setup'));
S.push(slideHeading('Slide 1 — Title'));
S.push(speech([
  '“Good morning. We are presenting the ', strong('Early Disease Prediction System'),
  ' — it predicts a person’s risk of diabetes and heart disease ',
  { text: 'before symptoms appear', italics: true },
  '. But our project is really about one question: when a machine-learning model says ‘84% risk’ — ',
  strong('how do you know whether to trust it?'),
  ' Everything you’ll see today is our answer. The system is live on the internet right now, and every number in this presentation was measured honestly, on patients the model had never seen.”',
]));
S.push(slideHeading('Slide 2 — Problem & Solution'));
S.push(speech([
  '“Three problems with typical disease-prediction projects. One: these diseases develop silently, and we know early action works — the Diabetes Prevention Program trial cut diabetes incidence by 58% with lifestyle changes alone. Two: most ML tools give a single number with zero statement of confidence. Three: most projects evaluate on data the model has already seen — the accuracy is inflated.',
]));
S.push(speech([
  'Our solution has four parts ', direction('(gesture right)'),
  ': an Uncertainty Engine of 200 models, a completely model-free second opinion, strictly honest evaluation, and a preventive plan tied to clinical guidelines. My teammates will take you through each.”',
]));
S.push(slideHeading('Slide 3 — Literature Review'));
S.push(speech([
  '“Four pieces of prior work shaped our design. Grinsztajn’s 2022 NeurIPS paper shows tree-based models still beat deep learning on small tabular data — which is why we did NOT use a neural network for 768 patients. Efron and Breiman’s bootstrap gives us our uncertainty method. Cover and Hart’s nearest-neighbour idea from 1967 becomes our second opinion. And the DPP trial is the clinical proof that early prediction is worth doing at all. ',
  strong('Pranav will now show you the data — and a trap hidden inside it.'), '”',
]));

/* ---------- Pranav ---------- */
S.push(speakerHeading('PRANAV SINGH PURI', '4–6', 'data & the engine'));
S.push(slideHeading('Slide 4 — The Data'));
S.push(speech([
  '“We use two classical clinical datasets: the Pima diabetes study — 768 patients, 8 features — and the Cleveland heart study — 303 patients, 13 features.',
]));
S.push(speech([
  'Now the trap ', direction('(point at the dark card)'), ': ',
  strong('374 of the 768 Pima patients have insulin recorded as zero.'),
  ' A blood insulin of zero is physiologically impossible — these are hidden missing values. Most projects on this dataset feed them to the model as real numbers and never notice. We mark them as missing and impute the study median — and crucially, the imputation is re-fitted inside every training fold, so no information ever leaks from test data into training.”',
]));
S.push(slideHeading('Slide 5 — System Architecture'));
S.push(speech([
  '“The system has two phases. Offline ', direction('(trace the top row)'),
  ': load the data, repair the missing values, evaluate honestly with 5-fold cross-validation, save the trained models. Online ',
  direction('(bottom row)'), ': a patient fills the intake form — and note, ',
  strong('nothing is predicted until they press ‘Run assessment’'),
  '. There is no phantom prediction sitting on screen for a patient nobody entered. Then two independent engines score them, and a five-section report is produced.”',
]));
S.push(slideHeading('Slide 6 — Deep Dive I: The Uncertainty Engine'));
S.push(speech([
  '“Here’s the heart of the system. One sentence: ',
  strong('we ask 200 slightly different models and plot all their answers.'),
  ' Each of the 200 is the same pipeline — impute, scale, gradient boosting — but each is trained on its own bootstrap resample of the patients, so each has a slightly different view of the world. One patient in, 200 opinions out.',
]));
S.push(speech([
  'Notice we deliberately did NOT tune hyperparameters — with only ~600 training rows per fold, tuning mostly fits noise. We chose evaluation integrity over squeezing one more AUC point. ',
  strong('Kartikya will show you what those 200 opinions look like.'), '”',
]));

/* ---------- Kartikya ---------- */
S.push(speakerHeading('KARTIKYA YADAV', '7–9', 'what makes it trustworthy'));
S.push(slideHeading('Slide 7 — A Distribution, Not a Number'));
S.push(speech([
  '“This is what the patient actually sees. Left: a clearly healthy patient — all 200 models agree, the histogram is a needle, the confidence band is one to two percent wide. Right: an ambiguous patient — the models genuinely disagree, and the band is 65 to 96 percent wide. ',
  strong('The system doesn’t hide its doubt — it draws it.'),
  ' A doctor reading the right-hand chart knows instantly: order a proper test.”',
]));
S.push(slideHeading('Slide 8 — Patients Like You'));
S.push(speech([
  '“Our second opinion uses ', strong('no model at all'),
  '. We standardize every measurement, find the 50 real patients in the study most similar to this one, and simply report how many of them actually developed the disease. In this example: the ensemble said 84.8%, the fifty most-similar patients said 78% — two completely independent methods, agreeing. When they disagree, the interface says so — and that’s exactly the patient who deserves extra caution.”',
]));
S.push(slideHeading('Slide 9 — The Threshold Rule'));
S.push(speech([
  '“Every alert system needs a threshold — most projects use 0.5 because it’s the default. Ours comes from a stated medical rule: ',
  strong('never miss more than 15% of true future patients'),
  ' — recall at least 85% — and among all thresholds that satisfy that, take the most precise one. ',
  direction('(point at the dashed lines)'),
  ' That gives 23.8% for diabetes, 27.3% for heart disease. The rule is written inside the app itself, so nothing is a magic number. ',
  strong('Rudra has the results.'), '”',
]));

/* ---------- Rudra ---------- */
S.push(speakerHeading('RUDRA', '10–12', 'results & the live system'));
S.push(slideHeading('Slide 10 — Results I: Benchmark'));
S.push(speech([
  '“Four models, identical folds, every number out-of-fold. On diabetes, our ensemble matches or beats all three baselines — 83.5 AUC. On heart disease we reach 90.0.',
]));
S.push(speech([
  'And an honest note we want to make ourselves before you ask ',
  direction('(point at the italic text)'),
  ': on the smaller heart dataset, logistic regression is actually one point ahead on AUC. We still deploy the ensemble — because it is the only model that also tells you ',
  strong('how sure it is'),
  '. The next slide shows that this is worth far more than one AUC point.”',
]));
S.push(slideHeading('Slide 11 — Results II: It Knows When It Doesn’t Know  ⭐'));
S.push(speech([
  direction('(Pause. This is the money slide — take your time.)'),
]));
S.push(speech([
  '“We sorted all patients by how wide their confidence band was, and measured the error rate in each group. Narrowest bands: ',
  strong('6% error'), '. Widest: ', strong('43%'),
  '. Same pattern on heart disease: 4 to 46.',
]));
S.push(speech([
  'Read that staircase again: when the 200 models agree, they are almost never wrong. When they disagree, the system ',
  { text: 'says so', italics: true },
  ' — and that is precisely where the mistakes live. ',
  strong('The uncertainty is not decoration; it is measurably informative.'),
  ' And below — the calibration plot — when we say 30% risk, roughly 30 of 100 such patients really develop the disease. The probabilities mean what they say.”',
]));
S.push(slideHeading('Slide 12 — The Live Dashboard'));
S.push(speech([
  '“This is not a mock-up — it’s deployed, public, at this URL, and you can open it on your phone right now. Same interface, both diseases: diabetes on the left, heart on the right. Intake form, run assessment, full report — risk drivers, a what-if simulator that answers ‘what if this patient lost 5 BMI points’, and a preventive plan citing real guideline ranges. ',
  strong('Sushant will close with an honest self-assessment.'), '”',
]));

/* ---------- Sushant ---------- */
S.push(speakerHeading('SUSHANT JAISWAL', '13–15', 'honesty & close'));
S.push(slideHeading('Slide 13 — SWOT'));
S.push(speech([
  '“We evaluated our own project the way a reviewer would. Strengths: honest metrics, informative uncertainty, two independent methods, deployed and tested. Weaknesses — we name them ourselves: the cohorts are small and decades old, there’s no external validation, and bootstrap bands capture sampling uncertainty only. The biggest threat is over-trust: a polished interface can look more authoritative than it is — which is exactly why the uncertainty band and the disclaimer are on every single screen. Opportunities: the architecture is a plug-in registry — ',
  strong('a third disease costs one configuration file and a retraining run.'), '”',
]));
S.push(slideHeading('Slide 14 — References'));
S.push(speech([
  '“All ten references are real and checkable — from Efron’s 1979 bootstrap paper to the 2022 NeurIPS work on tabular learning.” ',
  direction('(Don’t linger — 10 seconds, move on.)'),
]));
S.push(slideHeading('Slide 15 — Thank You'));
S.push(speech([
  '“To sum up in one breath: ',
  strong('two hundred models vote, fifty similar patients give a second opinion, every number is measured honestly — and the system knows when it does not know.'),
  ' The app is live at the link on screen. Thank you — we’re happy to take questions.”',
]));

/* ---------- Q&A table ---------- */
S.push(new Paragraph({
  heading: HeadingLevel.HEADING_1, pageBreakBefore: true,
  spacing: { before: 200, after: 160 },
  children: [new TextRun({ text: 'Q&A Prep — likely questions, who answers', font: 'Cambria', size: 32, bold: true, color: OXBLOOD })],
}));

const QA = [
  ['“Why not deep learning / CNNs?”',
   '768 & 303 patients — two to three orders of magnitude too small; Grinsztajn 2022 shows trees win on tabular data. Point back to slide 3.', 'Riyansh'],
  ['“Why are these metrics lower than other projects’ 95%?”',
   'Theirs are usually in-sample. Ours are out-of-fold — measured on unseen patients. Lower and true beats higher and false.', 'Pranav'],
  ['“How does imputation not leak?”',
   'The imputer lives inside the pipeline, so it is re-fitted per fold on training data only.', 'Pranav'],
  ['“Why 200 models? Why not 50 or 1000?”',
   'Enough for a stable distribution; doubling changes bands by under a point; 200 keeps the artifact ~36 MB and predictions instant (cached).', 'Kartikya'],
  ['“Is the what-if causal?”',
   'No — it is the model’s response to a changed input, not a guaranteed clinical effect. Named openly in Limitations.', 'Kartikya'],
  ['“Logistic regression beat you on heart — why deploy the ensemble?”',
   'Within one AUC point, and only the ensemble gives informative uncertainty — the 4→46% error staircase on slide 11.', 'Rudra'],
  ['“Could a hospital use this?”',
   'Not without clinical validation and recalibration on a modern local cohort — it is an educational prototype and says so in-product.', 'Sushant'],
  ['“How would you add a third disease?”',
   'One config file (features, form, rules) plus one training run — the registry design. Offer to show src/edp/diseases/.', 'Sushant'],
];

const cell = (text, opts = {}) => new TableCell({
  width: { size: opts.w, type: WidthType.DXA },
  shading: opts.head ? { type: ShadingType.CLEAR, fill: 'F6F2E9' } : undefined,
  margins: { top: 90, bottom: 90, left: 130, right: 130 },
  children: [new Paragraph({ children: [new TextRun({
    text, font: 'Calibri', size: 20, bold: !!opts.head, color: INK })] })],
});

S.push(new Table({
  columnWidths: [3100, 5300, 1200],
  width: { size: 9600, type: WidthType.DXA },
  rows: [
    new TableRow({ tableHeader: true, children: [
      cell('Question', { w: 3100, head: true }),
      cell('Answer with', { w: 5300, head: true }),
      cell('Who', { w: 1200, head: true })] }),
    ...QA.map(([q, a, w]) => new TableRow({ children: [
      cell(q, { w: 3100 }), cell(a, { w: 5300 }), cell(w, { w: 1200 })] })),
  ],
}));

S.push(new Paragraph({
  spacing: { before: 280 },
  children: [
    new TextRun({ text: 'Logistics:  ', font: 'Calibri', size: 22, bold: true, color: MOSS }),
    new TextRun({ text: 'open the live app 5 minutes before presenting (the free tier sleeps — first load takes a minute) and run one assessment on each disease, so everything is cached and instant if the professor asks for a live demo.', font: 'Calibri', size: 22, color: INK }),
  ],
}));

const doc = new Document({
  styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
  sections: [{
    properties: { page: { margin: { top: 1100, bottom: 1100, left: 1250, right: 1250 } } },
    headers: { default: new Header({ children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: 'Early Disease Prediction System — Presentation Script',
        font: 'Cambria', size: 17, color: MUTED })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: 'Calibri', size: 18, color: MUTED })] })] }) },
    children: S,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('Presentation_Script.docx', buf);
  console.log('docx written');
});
