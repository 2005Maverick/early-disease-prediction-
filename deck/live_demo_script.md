# Live Demo Script — show the professor the real website
**~5 minutes · one person drives (mouse), one person speaks (or one does both)**
Read the "Say" lines out loud. Do the "Do" steps on screen.

---

## PREPARATION (before the professor arrives)

1. Open **healthpredictor092005.streamlit.app** in the browser, 5 minutes early.
2. Run one assessment for Diabetes and one for Heart disease — this wakes the server, so everything is fast during the demo.
3. Keep the tab open with the sidebar visible.
4. **Backup if the internet fails:** run it locally — open a terminal in the project folder and type `streamlit run ui/main.py`.

---

## STEP 1 — Open the site

**Do:** Show the front page (refresh if needed).

**Say:**
"This is our system, running live on the internet.
Please notice one thing: there is no prediction on the screen yet.
The system first explains itself in three steps, and waits for real patient data.
Nothing is predicted until we press the button. We designed it this way on purpose."

---

## STEP 2 — A healthy patient

**Do:** Keep **Diabetes** selected. In the form enter:
- Glucose: **85**
- BMI: **21**
- Age: **25**
(leave the rest as they are) → click **Run assessment**.

**Say:**
"Let us first test a healthy young person. Glucose 85, BMI 21, age 25.
We press Run Assessment... and here is the report.
The risk is about 1 percent.
And look at the histogram — all 200 models agree. The confidence band is only 1 to 2 percent wide.
The system is sure, and it shows us that it is sure."

---

## STEP 3 — A high-risk patient

**Do:** Change the form to:
- Glucose: **190**
- BMI: **40**
- Age: **55**
→ click **Run assessment**.

**Say:**
"Now a high-risk patient. Glucose 190, BMI 40, age 55.
The risk jumps to about 85 percent — Very High.
But look at the histogram now. It is wide — from 65 to 96 percent.
The system is honest: this case is serious, but it is also less certain.
A normal ML system would hide this. Ours shows it."

---

## STEP 4 — Patients Like You (click the second tab)

**Do:** Click the **Patients Like You** tab.

**Say:**
"This is our second opinion — and it uses no model at all.
The system found the 50 real patients from the medical study who are most similar to this person.
Most of them developed diabetes — about 78 percent.
So two completely different methods gave almost the same answer. That builds trust.
The chart shows where our patient sits compared to the whole study — the diamond is our patient."

---

## STEP 5 — What-If Simulator (third tab)

**Do:** Click the **What-If Simulator** tab.

**Say:**
"Now the most practical part. What can this patient actually do?
Each row here changes one value and runs all 200 models again.
For example: if the patient lowers glucose by 30 points, the risk falls from 85 to about 72 percent.
This turns a prediction into an action."

---

## STEP 6 — Preventive Plan (fourth tab)

**Do:** Click the **Preventive Plan** tab.

**Say:**
"The prevention plan is not written by the model — it is written from real medical guidelines.
Every advice line shows the patient's own value, and the medical range that triggered the advice.
And at the bottom there is a clear disclaimer: this is an educational tool, not medical advice."

---

## STEP 7 — Data & Model Lab (fifth tab)

**Do:** Click the **Data & Model Lab** tab. Scroll slowly.

**Say:**
"This tab is for reviewers — like you, professor.
Here is the hidden missing data we found and fixed.
Here are our honest metrics, tested only on patients the models never saw.
Here is the comparison of four models, our threshold rule, and the calibration chart.
Nothing is hidden."

---

## STEP 8 — Switch to Heart disease

**Do:** In the sidebar select **Heart disease**. Enter:
- Age: **63**
- Sex: **Male**
- Resting blood pressure: **145**
- Total cholesterol: **280**
- Max heart rate achieved: **120**
- Tick **Chest pain during exercise**
- ST depression: **2.5**
→ click **Run assessment**.

**Say:**
"And now watch this — we switch to heart disease.
The form changes to heart features: cholesterol, blood pressure, heart rate.
We enter an older patient with high cholesterol and chest pain during exercise... and run.
Very high risk. Same interface, same five sections — completely different disease.
This is our plug-in design: one engine, many diseases. Adding a third disease needs only one new config file."

---

## STEP 9 — Close (back on screen)

**Say:**
"That is the full system: honest prediction, visible confidence, a second opinion, and an action plan.
Professor — if you would like, give us any values, and we will enter them live right now."

*(This invitation is the strongest possible ending — the system handles any input safely, including unknown values.)*

---

## IF SOMETHING GOES WRONG

- **Slow first load:** say calmly "the free server is waking up — it takes a few seconds." It only happens once.
- **A number is slightly different from this script:** that is fine — read the real number from the screen. Never argue with your own app.
- **No internet:** run locally with `streamlit run ui/main.py` — everything works the same.
- **Professor asks a value you don't know (like insulin):** tick the "unknown" checkbox and say: "the system fills unknown values with the study median — it is built for incomplete data."
