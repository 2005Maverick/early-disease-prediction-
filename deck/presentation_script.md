# Presentation Script (simple) — read each slide's lines while it is on screen
**15 slides · 5 speakers · ~12 minutes**

---

## RIYANSH CHOUDHARY — Slides 1, 2, 3

**Slide 1 — Title**
Good morning everyone. Our project is the Early Disease Prediction System.
It predicts the risk of diabetes and heart disease before symptoms appear.
The special thing about our project is that it also tells you how confident it is about every prediction.
The app is live on the internet, and anyone can use it at the link on screen.

**Slide 2 — Problem & Solution**
First, the problem. Diabetes and heart disease grow silently for many years.
If we find the risk early, simple lifestyle changes can prevent the disease.
But normal ML projects only give one number, and they never tell you if you can trust that number.
Our solution has four parts. We use 200 models instead of one. We add a second opinion from real similar patients. We test everything honestly. And we give the patient a prevention plan.

**Slide 3 — Literature Review**
We studied four research works.
The first paper proves that tree-based models work better than deep learning on small medical data.
The second gives us the bootstrap method, which we use for uncertainty.
The third is the nearest-neighbour method, which becomes our second opinion.
The fourth is a famous medical trial that showed early action cuts diabetes by 58 percent.
Now Pranav will explain our data.

---

## PRANAV SINGH PURI — Slides 4, 5, 6

**Slide 4 — The Data**
We use two famous medical datasets.
The Pima diabetes dataset has 768 patients with 8 features.
The Cleveland heart dataset has 303 patients with 13 features.
There is a hidden problem in this data: 374 patients have insulin written as zero.
Zero insulin is impossible for a living person, so these are actually missing values.
Most projects ignore this. We treat them as missing and fill them with the median value, safely inside each training fold.

**Slide 5 — System Architecture**
Our system has two phases.
In the training phase, we clean the data, train the models, and test them honestly with 5-fold cross-validation.
In the serving phase, the user fills a form and presses Run Assessment. Only then do the models predict.
Two engines run: the Uncertainty Engine and Patients Like You.
Together they produce a full report with five sections.

**Slide 6 — The Uncertainty Engine**
This is the heart of our project.
We train 200 models instead of one. Each model is trained on a slightly different random sample of the patients.
So for one patient we get 200 answers.
The average of the answers is the risk score. The spread of the answers tells us how confident the system is.
Now Kartikya will show what this looks like.

---

## KARTIKYA YADAV — Slides 7, 8, 9

**Slide 7 — A Distribution, Not a Number**
Here you can see two real examples.
On the left is a healthy patient. All 200 models agree, so the band is only 1 to 2 percent wide.
On the right is a difficult patient. The models disagree, so the band is 65 to 96 percent wide.
The system shows its doubt instead of hiding it.

**Slide 8 — Patients Like You**
Our second opinion uses no model at all.
We find the 50 patients in the study who are most similar to the current patient.
Then we simply count how many of them got the disease.
In this example, the ensemble said 84.8 percent, and the similar patients said 78 percent.
Two completely different methods gave almost the same answer. That builds trust.

**Slide 9 — The Threshold Rule**
Every system needs a cut-off point to raise an alert.
We did not pick a random number. We used a medical rule: we must catch at least 85 percent of the real patients.
With this rule, the threshold becomes 23.8 percent for diabetes and 27.3 percent for heart disease.
Now Rudra will present our results.

---

## RUDRA — Slides 10, 11, 12

**Slide 10 — Results I: Benchmark**
We compared four models on the same data, with honest testing.
For diabetes, our ensemble scores 83.5 AUC — equal to or better than all baselines.
For heart disease, it scores 90.
One honest point: logistic regression is one point higher on heart disease.
We still chose the ensemble, because only the ensemble can also tell us its confidence.

**Slide 11 — Results II: It Knows When It Does Not Know**
This is our most important result.
We divided all patients into four groups, based on how wide their confidence band was.
In the narrowest group, the error rate is only 6 percent. In the widest group, it is 43 percent.
Heart disease shows the same pattern: 4 percent to 46 percent.
This proves the system really knows when it is not sure.
The bottom chart shows calibration: when we say 30 percent risk, about 30 out of 100 such patients really get the disease.

**Slide 12 — The Live Dashboard**
Our system is not just a demo. It is live on the internet at this address, and you can open it on your phone right now.
The same interface works for both diseases.
It shows the risk, the reasons behind it, a what-if simulator, and a prevention plan.
Now Sushant will conclude.

---

## SUSHANT JAISWAL — Slides 13, 14, 15

**Slide 13 — SWOT**
We also analysed our own project honestly.
Strengths: honest testing, useful uncertainty, two independent methods, and a live deployment.
Weaknesses: the datasets are small and old, and there is no external validation yet.
Opportunity: adding a third disease needs only one new config file.
Threat: people may trust it too much — so the app shows a disclaimer on every screen.

**Slide 14 — References**
These are our ten references. All of them are real published papers.

**Slide 15 — Thank You**
To summarise: 200 models vote, 50 similar patients give a second opinion, every number is tested honestly, and the system knows when it does not know.
The app is live at the link on screen.
Thank you. We are happy to answer your questions.

---

## Q&A — short answers

| Question | Short answer | Who |
|---|---|---|
| Why not deep learning? | Our data is too small — only 768 and 303 patients. Research shows tree models win here. | Riyansh |
| Why is your accuracy lower than other projects? | Their numbers are tested on data the model already saw. Ours are tested on unseen patients, so ours are real. | Pranav |
| Why 200 models? | Enough for a stable answer; more models change almost nothing and make the app slower. | Kartikya |
| Is the what-if a guarantee? | No, it shows what the model predicts, not a guaranteed medical effect. We say this in Limitations. | Kartikya |
| Why deploy the ensemble if logistic regression scored higher on heart? | The difference is only one point, and only the ensemble can tell us its confidence. | Rudra |
| Can a hospital use this? | Not yet — it needs clinical validation first. The app says this on every screen. | Sushant |
| How do you add a third disease? | One new config file plus one training run. | Sushant |

**Before presenting:** open the live app 5 minutes early and run one assessment for each disease, so it is fast during the demo.
