/* Live demo script as a Word document.
   Build:  node make_demo_docx.js   (from the deck/ directory)            */
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
        Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

const INK = '1C1A17', OXBLOOD = '8E2F22', MUTED = '6B6156', MOSS = '3A6B35';

// [heading, [ ['do'|'say'|'note', text], ... ]]
const STEPS = [
  ['PREPARATION (before the professor arrives)', [
    ['note', '1.  Open healthpredictor092005.streamlit.app in the browser, 5 minutes early.'],
    ['note', '2.  Run one assessment for Diabetes and one for Heart disease — this wakes the server, so everything is fast during the demo.'],
    ['note', '3.  Keep the tab open with the sidebar visible.'],
    ['note', '4.  Backup if the internet fails: run it locally — open a terminal in the project folder and type:  streamlit run ui/main.py'],
  ]],
  ['STEP 1 — Open the site', [
    ['do', 'Show the front page (refresh if needed).'],
    ['say', 'This is our system, running live on the internet.'],
    ['say', 'Please notice one thing: there is no prediction on the screen yet.'],
    ['say', 'The system first explains itself in three steps, and waits for real patient data.'],
    ['say', 'Nothing is predicted until we press the button. We designed it this way on purpose.'],
  ]],
  ['STEP 2 — A healthy patient', [
    ['do', 'Keep Diabetes selected. Enter:  Glucose 85  ·  BMI 21  ·  Age 25  (leave the rest as they are). Click Run assessment.'],
    ['say', 'Let us first test a healthy young person. Glucose 85, BMI 21, age 25.'],
    ['say', 'We press Run Assessment... and here is the report.'],
    ['say', 'The risk is about 1 percent.'],
    ['say', 'And look at the histogram — all 200 models agree. The confidence band is only 1 to 2 percent wide.'],
    ['say', 'The system is sure, and it shows us that it is sure.'],
  ]],
  ['STEP 3 — A high-risk patient', [
    ['do', 'Change the form to:  Glucose 190  ·  BMI 40  ·  Age 55.  Click Run assessment.'],
    ['say', 'Now a high-risk patient. Glucose 190, BMI 40, age 55.'],
    ['say', 'The risk jumps to about 85 percent — Very High.'],
    ['say', 'But look at the histogram now. It is wide — from 65 to 96 percent.'],
    ['say', 'The system is honest: this case is serious, but it is also less certain.'],
    ['say', 'A normal ML system would hide this. Ours shows it.'],
  ]],
  ['STEP 4 — Patients Like You (second tab)', [
    ['do', 'Click the Patients Like You tab.'],
    ['say', 'This is our second opinion — and it uses no model at all.'],
    ['say', 'The system found the 50 real patients from the medical study who are most similar to this person.'],
    ['say', 'Most of them developed diabetes — about 78 percent.'],
    ['say', 'So two completely different methods gave almost the same answer. That builds trust.'],
    ['say', 'The chart shows where our patient sits compared to the whole study — the diamond is our patient.'],
  ]],
  ['STEP 5 — What-If Simulator (third tab)', [
    ['do', 'Click the What-If Simulator tab.'],
    ['say', 'Now the most practical part. What can this patient actually do?'],
    ['say', 'Each row here changes one value and runs all 200 models again.'],
    ['say', 'For example: if the patient lowers glucose by 30 points, the risk falls from 85 to about 72 percent.'],
    ['say', 'This turns a prediction into an action.'],
  ]],
  ['STEP 6 — Preventive Plan (fourth tab)', [
    ['do', 'Click the Preventive Plan tab.'],
    ['say', 'The prevention plan is not written by the model — it is written from real medical guidelines.'],
    ['say', 'Every advice line shows the patient’s own value, and the medical range that triggered the advice.'],
    ['say', 'And at the bottom there is a clear disclaimer: this is an educational tool, not medical advice.'],
  ]],
  ['STEP 7 — Data & Model Lab (fifth tab)', [
    ['do', 'Click the Data & Model Lab tab. Scroll slowly.'],
    ['say', 'This tab is for reviewers — like you, professor.'],
    ['say', 'Here is the hidden missing data we found and fixed.'],
    ['say', 'Here are our honest metrics, tested only on patients the models never saw.'],
    ['say', 'Here is the comparison of four models, our threshold rule, and the calibration chart.'],
    ['say', 'Nothing is hidden.'],
  ]],
  ['STEP 8 — Switch to Heart disease', [
    ['do', 'In the sidebar select Heart disease. Enter:  Age 63  ·  Sex Male  ·  Resting BP 145  ·  Cholesterol 280  ·  Max heart rate 120  ·  tick "Chest pain during exercise"  ·  ST depression 2.5.  Click Run assessment.'],
    ['say', 'And now watch this — we switch to heart disease.'],
    ['say', 'The form changes to heart features: cholesterol, blood pressure, heart rate.'],
    ['say', 'We enter an older patient with high cholesterol and chest pain during exercise... and run.'],
    ['say', 'Very high risk. Same interface, same five sections — completely different disease.'],
    ['say', 'This is our plug-in design: one engine, many diseases. Adding a third disease needs only one new config file.'],
  ]],
  ['STEP 9 — Close', [
    ['say', 'That is the full system: honest prediction, visible confidence, a second opinion, and an action plan.'],
    ['say', 'Professor — if you would like, give us any values, and we will enter them live right now.'],
    ['note', 'This invitation is the strongest possible ending — the system handles any input safely, including unknown values.'],
  ]],
  ['IF SOMETHING GOES WRONG', [
    ['note', 'Slow first load:  say calmly "the free server is waking up — it takes a few seconds." It only happens once.'],
    ['note', 'A number is slightly different from this script:  read the real number from the screen. Never argue with your own app.'],
    ['note', 'No internet:  run locally with  streamlit run ui/main.py  — everything works the same.'],
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
  children: [new TextRun({ text: 'Show the professor the real website — about 5 minutes. One person drives the mouse, one person reads the "Say" lines (or one person does both).', font: 'Cambria', size: 24, italics: true, color: OXBLOOD })],
}));

for (const [heading, lines] of STEPS) {
  S.push(new Paragraph({
    heading: HeadingLevel.HEADING_1, spacing: { before: 340, after: 110 },
    children: [new TextRun({ text: heading, font: 'Cambria', size: 29, bold: true, color: OXBLOOD })],
  }));
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
