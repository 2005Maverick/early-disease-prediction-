# Live Demo Script — explain the whole system while showing the website
**~8–10 minutes. The website replaces the slides: at every step you show something on screen and explain how the system works behind it.**
Read the "Say" lines out loud. Do the "Do" steps on screen.

---

## PREPARATION (before the professor arrives)

1. Open **healthpredictor092005.streamlit.app** 5 minutes early.
2. Run one assessment for Diabetes and one for Heart disease — this wakes the server so the demo is fast.
3. Backup if internet fails: run locally with `streamlit run ui/main.py`.

---

## STEP 1 — The front page  →  explain THE DESIGN and THE DATA

**Do:** Show the front page. Point at the three steps in the middle, then at the empty form on the left.

**Say:**
"This is our Early Disease Prediction System, live on the internet. It predicts diabetes and heart-disease risk before symptoms appear.
Notice the screen: there is no prediction yet. We designed the system so that nothing is predicted until real patient data is entered and the button is pressed.
Behind this page, the system has already learned from two famous medical datasets: the Pima diabetes study with 768 patients, and the Cleveland heart study with 303 patients.
While cleaning this data we found a hidden problem: 374 patients had insulin written as zero. Zero insulin is impossible — those were actually missing values. We treat them as missing and fill them with the median, safely inside each training fold, so no test information leaks into training.
Now let me show you how a prediction works."

---

## STEP 2 — Run a healthy patient  →  explain THE UNCERTAINTY ENGINE

**Do:** Keep **Diabetes** selected. Enter **Glucose 85, BMI 21, Age 25**. Click **Run assessment**. When the report appears, point at the histogram.

**Say:**
"I am entering a healthy young person: glucose 85, BMI 21, age 25. Now I press Run Assessment.
Here is what just happened behind the button: we do not use one model — we use two hundred.
Each of the 200 models is the same pipeline — fill missing values, scale, gradient boosting — but each one was trained on a slightly different random sample of the patients. This is called bootstrapping.
So for this patient, the system just collected 200 separate answers.
The average of those answers is the risk score — about 1 percent.
And this histogram you see IS those 200 answers. They all agree, so the bar is a needle, and the confidence band is only 1 to 2 percent wide.
When the models agree, the system is confident — and it shows that."

---

## STEP 3 — Run a high-risk patient  →  explain WHAT UNCERTAINTY MEANS

**Do:** Change to **Glucose 190, BMI 40, Age 55**. Click **Run assessment**. Point at the wide histogram.

**Say:**
"Now a high-risk patient: glucose 190, BMI 40, age 55.
The risk jumps to about 85 percent — Very High. But look at the histogram now: the 200 answers are spread from 65 to 96 percent.
Why? Because this patient is unusual, and models trained on different samples of the data genuinely disagree about him.
Most ML systems would hide this and print one confident number. Ours shows the disagreement — because we proved, with honest testing, that when the band is narrow the system is wrong only 6 percent of the time, and when the band is wide, it is wrong 43 percent of the time.
So the width of this bar is real information: it tells the doctor when to order a proper lab test."

---

## STEP 4 — Patients Like You tab  →  explain THE SECOND OPINION

**Do:** Click the **Patients Like You** tab. Point at the headline number, then the chart.

**Say:**
"Machine-learning models can be wrong in strange ways, so we added a second opinion that uses no model at all.
Here is how it works: the system puts all measurements on the same scale, then finds the 50 real patients from the study who are mathematically closest to our patient — the 50 most similar people.
Then it simply counts: how many of those 50 actually developed diabetes? About 78 percent.
Our ensemble said 85, the similar patients say 78 — two completely different methods, almost the same answer. When two independent methods agree, we can trust the result more. And when they disagree, the app says so — that patient deserves extra caution.
In this chart, the diamond is our patient, and the colored dots are his 50 nearest neighbours — red ones developed the disease."

---

## STEP 5 — What-If Simulator tab  →  explain HOW ADVICE IS COMPUTED

**Do:** Click the **What-If Simulator** tab. Point at the bars.

**Say:**
"Prediction alone does not help a patient. So the system also answers: what would change the risk?
Each row here takes the patient's data, changes exactly one value — for example glucose reduced by 30 — and runs all 200 models again from scratch.
The result: lowering glucose by 30 points drops the risk from 85 to about 72 percent.
This is computed live by the real models, not written by hand. It turns a prediction into a plan of action."

---

## STEP 6 — Preventive Plan tab  →  explain WHY RULES, NOT THE MODEL

**Do:** Click the **Preventive Plan** tab. Point at one advice entry.

**Say:**
"For the actual medical advice we made a deliberate design decision: the advice is NOT generated by the model.
Every line here comes from published clinical guidelines — for example, glucose between 140 and 199 means impaired glucose tolerance.
Each advice shows the patient's own value and the medical range that triggered it — so every sentence can be traced back to a guideline, not to a statistical artifact.
And here at the bottom: a clear disclaimer that this is an educational tool, not medical advice."

---

## STEP 7 — Data & Model Lab tab  →  explain THE HONEST EVALUATION

**Do:** Click the **Data & Model Lab** tab. Scroll slowly, pointing at each section as you mention it.

**Say:**
"This tab exists for one reason: so a reviewer can check us.
First — the hidden missing values I mentioned, counted per feature.
Second — our metrics. Every number here is out-of-fold: we split the data five times, and each model was always tested on patients it had never seen. Diabetes: 83.5 ROC AUC. Heart disease: 90.
Third — we compare four models on identical data. Honestly: on heart disease, simple logistic regression scores one point higher. We still deploy the ensemble, because it is the only model that also tells us its confidence — which you saw is real information.
Fourth — the alert threshold is not a random 0.5. It comes from a stated rule: catch at least 85 percent of the real patients. The rule gives 23.8 percent for diabetes.
And last — the calibration chart: when the system says 30 percent risk, about 30 out of 100 such patients really developed the disease. The points sit on the diagonal — our probabilities mean what they say."

---

## STEP 8 — Switch to Heart disease  →  explain THE PLUG-IN ARCHITECTURE

**Do:** In the sidebar select **Heart disease**. Enter: **Age 63, Sex Male, Resting BP 145, Cholesterol 280, Max heart rate 120, tick "Chest pain during exercise", ST depression 2.5**. Click **Run assessment**.

**Say:**
"Finally — the architecture. Watch what happens when I switch the disease.
The whole form changed: now it asks for cholesterol, blood pressure, heart rate — heart features.
This works because of our plug-in design: every disease is just one configuration file that declares its dataset, its features, its form, and its medical rules. The engine — the 200 models, the neighbours, the explanations, this whole interface — is shared.
Each disease has its own separately trained ensemble, saved as a model file that loads on demand.
I enter an older patient with high cholesterol and chest pain during exercise... and run. Very high risk — same five sections, completely different disease.
Adding a third disease would need exactly one new config file and one training run."

---

## STEP 9 — Close

**Say:**
"So that is the whole system, shown live: two hundred models vote, fifty similar patients give a second opinion, every number is tested honestly, the advice traces to medical guidelines — and the system knows when it does not know.
Professor — if you would like, give us any values, and we will enter them right now."

---

## IF SOMETHING GOES WRONG

- **Slow first load:** say calmly "the free server is waking up — a few seconds." Happens only once.
- **A number differs slightly from this script:** read the real number from the screen. Never argue with your own app.
- **No internet:** run locally with `streamlit run ui/main.py`.
- **Professor asks a value you don't know (like insulin):** tick the "unknown" checkbox and say: "the system fills unknown values with the study median — it is built for incomplete data."
