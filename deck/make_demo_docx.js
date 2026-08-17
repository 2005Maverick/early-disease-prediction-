/* Live demo script (demo + system explanation combined) as a Word document.
   Build:  node make_demo_docx.js   (from the deck/ directory)            */
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
        Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

const INK = '1C1A17', OXBLOOD = '8E2F22', MUTED = '6B6156', MOSS = '3A6B35';

// [heading, explains, [ ['do'|'say'|'note', text], ... ]]
const STEPS = [
  ['PREPARATION (before the professor arrives)', null, [
    ['note', '1.  Open healthpredictor092005.streamlit.app 5 minutes early.'],
    ['note', '2.  Run one assessment for Diabetes and one for Heart disease — this wakes the server so the demo is fast.'],
    ['note', '3.  Backup if internet fails: run locally with  streamlit run ui/main.py'],
  ]],
  ['STEP 1 — The front page', 'explains the design and the data', [
    ['do', 'Show the front page. Point at the three steps in the middle, then at the empty form on the left.'],
    ['say', 'This is our Early Disease Prediction System, live on the internet. It predicts diabetes and heart-disease risk before symptoms appear.'],
    ['say', 'Notice the screen: there is no prediction yet. We designed the system so that nothing is predicted until real patient data is entered and the button is pressed.'],
    ['say', 'Behind this page, the system has already learned from two famous medical datasets: the Pima diabetes study with 768 patients, and the Cleveland heart study with 303 patients.'],
    ['say', 'While cleaning this data we found a hidden problem: 374 patients had insulin written as zero. Zero insulin is impossible — those were actually missing values. We treat them as missing and fill them with the median, safely inside each training fold, so no test information leaks into training.'],
    ['say', 'Now let me show you how a prediction works.'],
  ]],
  ['STEP 2 — Run a healthy patient', 'explains the Uncertainty Engine', [
    ['do', 'Keep Diabetes selected. Enter:  Glucose 85 · BMI 21 · Age 25.  Click Run assessment. When the report appears, point at the histogram.'],
    ['say', 'I am entering a healthy young person: glucose 85, BMI 21, age 25. Now I press Run Assessment.'],
    ['say', 'Here is what just happened behind the button: we do not use one model — we use two hundred.'],
    ['say', 'Each of the 200 models is the same pipeline — fill missing values, scale, gradient boosting — but each one was trained on a slightly different random sample of the patients. This is called bootstrapping.'],
    ['say', 'So for this patient, the system just collected 200 separate answers.'],
    ['say', 'The average of those answers is the risk score — about 1 percent.'],
    ['say', 'And this histogram you see IS those 200 answers. They all agree, so the bar is a needle, and the confidence band is only 1 to 2 percent wide.'],
    ['say', 'When the models agree, the system is confident — and it shows that.'],
  ]],
  ['STEP 3 — Run a high-risk patient', 'explains what uncertainty means', [
    ['do', 'Change to:  Glucose 190 · BMI 40 · Age 55.  Click Run assessment. Point at the wide histogram.'],
    ['say', 'Now a high-risk patient: glucose 190, BMI 40, age 55.'],
    ['say', 'The risk jumps to about 85 percent — Very High. But look at the histogram now: the 200 answers are spread from 65 to 96 percent.'],
    ['say', 'Why? Because this patient is unusual, and models trained on different samples of the data genuinely disagree about him.'],
    ['say', 'Most ML systems would hide this and print one confident number. Ours shows the disagreement — because we proved, with honest testing, that when the band is narrow the system is wrong only 6 percent of the time, and when the band is wide, it is wrong 43 percent of the time.'],
    ['say', 'So the width of this bar is real information: it tells the doctor when to order a proper lab test.'],
  ]],
  ['STEP 4 — Patients Like You tab', 'explains the second opinion', [
    ['do', 'Click the Patients Like You tab. Point at the headline number, then the chart.'],
    ['say', 'Machine-learning models can be wrong in strange ways, so we added a second opinion that uses no model at all.'],
    ['say', 'Here is how it works: the system puts all measurements on the same scale, then finds the 50 real patients from the study who are mathematically closest to our patient — the 50 most similar people.'],
    ['say', 'Then it simply counts: how many of those 50 actually developed diabetes? About 78 percent.'],
    ['say', 'Our ensemble said 85, the similar patients say 78 — two completely different methods, almost the same answer. When two independent methods agree, we can trust the result more. And when they disagree, the app says so — that patient deserves extra caution.'],
    ['say', 'In this chart, the diamond is our patient, and the colored dots are his 50 nearest neighbours — red ones developed the disease.'],
  ]],
  ['STEP 5 — What-If Simulator tab', 'explains how the advice is computed', [
    ['do', 'Click the What-If Simulator tab. Point at the bars.'],
    ['say', 'Prediction alone does not help a patient. So the system also answers: what would change the risk?'],
    ['say', 'Each row here takes the patient’s data, changes exactly one value — for example glucose reduced by 30 — and runs all 200 models again from scratch.'],
    ['say', 'The result: lowering glucose by 30 points drops the risk from 85 to about 72 percent.'],
    ['say', 'This is computed live by the real models, not written by hand. It turns a prediction into a plan of action.'],
  ]],
  ['STEP 6 — Preventive Plan tab', 'explains why rules, not the model', [
    ['do', 'Click the Preventive Plan tab. Point at one advice entry.'],
    ['say', 'For the actual medical advice we made a deliberate design decision: the advice is NOT generated by the model.'],
    ['say', 'Every line here comes from published clinical guidelines — for example, glucose between 140 and 199 means impaired glucose tolerance.'],
    ['say', 'Each advice shows the patient’s own value and the medical range that triggered it — so every sentence can be traced back to a guideline, not to a statistical artifact.'],
    ['say', 'And here at the bottom: a clear disclaimer that this is an educational tool, not medical advice.'],
  ]],
  ['STEP 7 — Data & Model Lab tab', 'explains the honest evaluation', [
    ['do', 'Click the Data & Model Lab tab. Scroll slowly, pointing at each section as you mention it.'],
    ['say', 'This tab exists for one reason: so a reviewer can check us.'],
    ['say', 'First — the hidden missing values I mentioned, counted per feature.'],
    ['say', 'Second — our metrics. Every number here is out-of-fold: we split the data five times, and each model was always tested on patients it had never seen. Diabetes: 83.5 ROC AUC. Heart disease: 90.'],
    ['say', 'Third — we compare four models on identical data. Honestly: on heart disease, simple logistic regression scores one point higher. We still deploy the ensemble, because it is the only model that also tells us its confidence — which you saw is real information.'],
    ['say', 'Fourth — the alert threshold is not a random 0.5. It comes from a stated rule: catch at least 85 percent of the real patients. The rule gives 23.8 percent for diabetes.'],
    ['say', 'And last — the calibration chart: when the system says 30 percent risk, about 30 out of 100 such patients really developed the disease. The points sit on the diagonal — our probabilities mean what they say.'],
  ]],
  ['STEP 8 — Switch to Heart disease', 'explains the plug-in architecture', [
    ['do', 'In the sidebar select Heart disease. Enter:  Age 63 · Sex Male · Resting BP 145 · Cholesterol 280 · Max heart rate 120 · tick "Chest pain during exercise" · ST depression 2.5.  Click Run assessment.'],
    ['say', 'Finally — the architecture. Watch what happens when I switch the disease.'],
    ['say', 'The whole form changed: now it asks for cholesterol, blood pressure, heart rate — heart features.'],
    ['say', 'This works because of our plug-in design: every disease is just one configuration file that declares its dataset, its features, its form, and its medical rules. The engine — the 200 models, the neighbours, the explanations, this whole interface — is shared.'],
    ['say', 'Each disease has its own separately trained ensemble, saved as a model file that loads on demand.'],
    ['say', 'I enter an older patient with high cholesterol and chest pain during exercise... and run. Very high risk — same five sections, completely different disease.'],
    ['say', 'Adding a third disease would need exactly one new config file and one training run.'],
  ]],
  ['STEP 9 — Close', null, [
    ['say', 'So that is the whole system, shown live: two hundred models vote, fifty similar patients give a second opinion, every number is tested honestly, the advice traces to medical guidelines — and the system knows when it does not know.'],
    ['say', 'Professor — if you would like, give us any values, and we will enter them right now.'],
  ]],
  ['IF SOMETHING GOES WRONG', null, [
    ['note', 'Slow first load:  say calmly "the free server is waking up — a few seconds." Happens only once.'],
    ['note', 'A number differs slightly from this script:  read the real number from the screen. Never argue with your own app.'],
    ['note', 'No internet:  run locally with  streamlit run ui/main.py'],
    ['note', 'Professor asks a value you don’t know (like insulin):  tick the "unknown" checkbox and say: "the system fills unknown values with the study median — it is built for incomplete data."'],
  ]],
];

const S = [];
S.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 200, after: 60 },
  children: [new TextRun({ text: 'Live Demo Script', font: 'Cambria', size: 52, bold: true, color: INK })],
}));
S.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 320 },
  children: [new TextRun({ text: 'The website replaces the slides: at every step you show something on screen and explain how the system works behind it. About 8–10 minutes.', font: 'Cambria', size: 24, italics: true, color: OXBLOOD })],
}));

for (const [heading, explains, lines] of STEPS) {
  const runs = [new TextRun({ text: heading, font: 'Cambria', size: 29, bold: true, color: OXBLOOD })];
  if (explains) runs.push(new TextRun({ text: `   →  ${explains}`, font: 'Cambria', size: 22, italics: true, color: MUTED }));
  S.push(new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 340, after: 110 }, children: runs }));
  for (const [kind, text] of lines) {
    if (kind === 'do') {
      S.push(new Paragraph({
        spacing: { after: 130 },
        children: [
          new TextRun({ text: 'DO:  ', font: 'Calibri', size: 23, bold: true, color: MOSS }),
          new TextRun({ text, font: 'Calibri', size: 23, color: INK }),
        ],
      }));
    } else if (kind === 'say') {
      S.push(new Paragraph({
        spacing: { after: 90, line: 310 }, indent: { left: 480 },
        children: [new TextRun({ text, font: 'Calibri', size: 24, color: INK })],
      }));
    } else {
      S.push(new Paragraph({
        spacing: { after: 90, line: 300 },
        children: [new TextRun({ text, font: 'Calibri', size: 22, italics: true, color: MUTED })],
      }));
    }
  }
}

const doc = new Document({
  styles: { default: { document: { run: { font: 'Calibri', size: 24 } } } },
  sections: [{
    properties: { page: { margin: { top: 1100, bottom: 1100, left: 1250, right: 1250 } } },
    headers: { default: new Header({ children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: 'Early Disease Prediction System — Live Demo Script',
        font: 'Cambria', size: 17, color: MUTED })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ children: [PageNumber.CURRENT], font: 'Calibri', size: 18, color: MUTED })] })] }) },
    children: S,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('Live_Demo_Script.docx', buf);
  console.log('docx written');
});
