# Presentation Script — Early Disease Prediction System
**15 slides · 5 speakers · ~13 minutes total (~50 sec/slide)**
Handovers are written in. Don't read slides aloud — the script says what the slide doesn't.

---

## RIYANSH CHOUDHARY — Slides 1–3 (the setup)

### Slide 1 — Title
> "Good morning. We are presenting the **Early Disease Prediction System** — it predicts a person's risk of diabetes and heart disease *before symptoms appear*. But our project is really about one question: when a machine-learning model says '84% risk' — **how do you know whether to trust it?** Everything you'll see today is our answer. The system is live on the internet right now, and every number in this presentation was measured honestly, on patients the model had never seen."

### Slide 2 — Problem & Solution
> "Three problems with typical disease-prediction projects. One: these diseases develop silently, and we know early action works — the Diabetes Prevention Program trial cut diabetes incidence by 58% with lifestyle changes alone. Two: most ML tools give a single number with zero statement of confidence. Three: most projects evaluate on data the model has already seen — the accuracy is inflated.
> Our solution has four parts *(gesture right)*: an Uncertainty Engine of 200 models, a completely model-free second opinion, strictly honest evaluation, and a preventive plan tied to clinical guidelines. My teammates will take you through each."

### Slide 3 — Literature Review
> "Four pieces of prior work shaped our design. Grinsztajn's 2022 NeurIPS paper shows tree-based models still beat deep learning on small tabular data — which is why we did NOT use a neural network for 768 patients. Efron and Breiman's bootstrap gives us our uncertainty method. Cover and Hart's nearest-neighbour idea from 1967 becomes our second opinion. And the DPP trial is the clinical proof that early prediction is worth doing at all.
> **Pranav will now show you the data — and a trap hidden inside it.**"

---

## PRANAV SINGH PURI — Slides 4–6 (data & the engine)

### Slide 4 — The Data
> "We use two classical clinical datasets: the Pima diabetes study — 768 patients, 8 features — and the Cleveland heart study — 303 patients, 13 features.
> Now the trap *(point at the dark card)*: **374 of the 768 Pima patients have insulin recorded as zero.** A blood insulin of zero is physiologically impossible — these are hidden missing values. Most projects on this dataset feed them to the model as real numbers and never notice. We mark them as missing and impute the study median — and crucially, the imputation is re-fitted inside every training fold, so no information ever leaks from test data into training."

### Slide 5 — System Architecture
> "The system has two phases. Offline *(trace the top row)*: load the data, repair the missing values, evaluate honestly with 5-fold cross-validation, save the trained models. Online *(bottom row)*: a patient fills the intake form — and note, **nothing is predicted until they press 'Run assessment'**. There is no phantom prediction sitting on screen for a patient nobody entered. Then two independent engines score them, and a five-section report is produced."

### Slide 6 — Deep Dive I: The Uncertainty Engine
> "Here's the heart of the system. One sentence: **we ask 200 slightly different models and plot all their answers.** Each of the 200 is the same pipeline — impute, scale, gradient boosting — but each is trained on its own bootstrap resample of the patients, so each has a slightly different view of the world. One patient in, 200 opinions out.
> Notice we deliberately did NOT tune hyperparameters — with only ~600 training rows per fold, tuning mostly fits noise. We chose evaluation integrity over squeezing one more AUC point.
> **Kartikya will show you what those 200 opinions look like.**"

---

## KARTIKYA YADAV — Slides 7–9 (what makes it trustworthy)

### Slide 7 — A Distribution, Not a Number
> "This is what the patient actually sees. Left: a clearly healthy patient — all 200 models agree, the histogram is a needle, the confidence band is one to two percent wide. Right: an ambiguous patient — the models genuinely disagree, and the band is 65 to 96 percent wide. **The system doesn't hide its doubt — it draws it.** A doctor reading the right-hand chart knows instantly: order a proper test."

### Slide 8 — Patients Like You
> "Our second opinion uses **no model at all**. We standardize every measurement, find the 50 real patients in the study most similar to this one, and simply report how many of them actually developed the disease. In this example: the ensemble said 84.8%, the fifty most-similar patients said 78% — two completely independent methods, agreeing. When they disagree, the interface says so — and that's exactly the patient who deserves extra caution."

### Slide 9 — The Threshold Rule
> "Every alert system needs a threshold — most projects use 0.5 because it's the default. Ours comes from a stated medical rule: **never miss more than 15% of true future patients** — recall at least 85% — and among all thresholds that satisfy that, take the most precise one. *(point at the dashed lines)* That gives 23.8% for diabetes, 27.3% for heart disease. The rule is written inside the app itself, so nothing is a magic number.
> **Rudra has the results.**"

---

## RUDRA — Slides 10–12 (results & the live system)

### Slide 10 — Results I: Benchmark
> "Four models, identical folds, every number out-of-fold. On diabetes, our ensemble matches or beats all three baselines — 83.5 AUC. On heart disease we reach 90.0.
> And an honest note we want to make ourselves before you ask *(point at italic text)*: on the smaller heart dataset, logistic regression is actually one point ahead on AUC. We still deploy the ensemble — because it is the only model that also tells you **how sure it is**. The next slide shows that this is worth far more than one AUC point."

### Slide 11 — Results II: It Knows When It Doesn't Know ⭐
> *(Pause. This is the money slide — take your time.)*
> "We sorted all patients by how wide their confidence band was, and measured the error rate in each group. Narrowest bands: **6% error**. Widest: **43%**. Same pattern on heart disease: 4 to 46.
> Read that staircase again: when the 200 models agree, they are almost never wrong. When they disagree, the system *says so* — and that is precisely where the mistakes live. **The uncertainty is not decoration; it is measurably informative.** And below — the calibration plot — when we say 30% risk, roughly 30 of 100 such patients really develop the disease. The probabilities mean what they say."

### Slide 12 — The Live Dashboard
> "This is not a mock-up — it's deployed, public, at this URL, and you can open it on your phone right now. Same interface, both diseases: diabetes on the left, heart on the right. Intake form, run assessment, full report — risk drivers, a what-if simulator that answers 'what if this patient lost 5 BMI points', and a preventive plan citing real guideline ranges.
> **Sushant will close with an honest self-assessment.**"

---

## SUSHANT JAISWAL — Slides 13–15 (honesty & close)

### Slide 13 — SWOT
> "We evaluated our own project the way a reviewer would. Strengths: honest metrics, informative uncertainty, two independent methods, deployed and tested. Weaknesses — we name them ourselves: the cohorts are small and decades old, there's no external validation, and bootstrap bands capture sampling uncertainty only. The biggest threat is over-trust: a polished interface can look more authoritative than it is — which is exactly why the uncertainty band and the disclaimer are on every single screen. Opportunities: the architecture is a plug-in registry — **a third disease costs one configuration file and a retraining run**."

### Slide 14 — References
> "All ten references are real and checkable — from Efron's 1979 bootstrap paper to the 2022 NeurIPS work on tabular learning." *(Don't linger — 10 seconds, move on.)*

### Slide 15 — Thank You
> "To sum up in one breath: **two hundred models vote, fifty similar patients give a second opinion, every number is measured honestly — and the system knows when it does not know.** The app is live at the link on screen. Thank you — we're happy to take questions."

---

## Q&A PREP — likely questions, who answers

| Question | Answer with | Who |
|---|---|---|
| "Why not deep learning / CNNs?" | 768 & 303 patients — 2–3 orders of magnitude too small; Grinsztajn 2022 shows trees win on tabular data. Slide 3. | Riyansh |
| "Why are these metrics lower than other projects' 95%?" | Theirs are usually in-sample. Ours are out-of-fold — measured on unseen patients. Lower and *true* beats higher and false. | Pranav |
| "How does imputation not leak?" | Imputer lives *inside* the pipeline → re-fitted per fold on training data only. | Pranav |
| "Why 200 models? Why not 50 or 1000?" | Enough for a stable distribution; doubling changes bands by <1 point; 200 keeps the artifact ~36 MB and predictions instant (cached). | Kartikya |
| "Is the what-if causal?" | No — it's the model's response to a changed input, not a guaranteed clinical effect. Named in Limitations. | Kartikya |
| "Logistic regression beat you on heart — why deploy the ensemble?" | Within 1 AUC point, and only the ensemble gives informative uncertainty (slide 11's 4→46% staircase). | Rudra |
| "Could a hospital use this?" | Not without clinical validation and recalibration on a modern local cohort — it's an educational prototype and says so in-product. | Sushant |
| "How would you add a third disease?" | One config file (features, form, rules) + one training run — the registry design. Offer to show `src/edp/diseases/` if they want proof. | Sushant |

**Logistics:** open the live app 5 minutes before presenting (free tier sleeps — first load takes a minute) and run one assessment on each disease so everything is cached and instant if the professor asks for a live demo.
