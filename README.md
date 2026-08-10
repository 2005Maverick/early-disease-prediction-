# Early Disease Prediction System

Predicts **diabetes and heart disease** risk before symptoms appear from
lifestyle, demographic and clinical data — with honest uncertainty, an
independent second opinion, and a personalized prevention plan.

One disease-agnostic engine, many diseases: each disease is a config object
(dataset, features, intake form, what-if scenarios, prevention rules); the
uncertainty ensemble, similarity engine, explanations and UI are shared.
Adding a disease means adding one config file and retraining.

## What makes this different

1. **A risk *distribution*, not just a number.** 200 models are trained on
   bootstrap resamples of the study; each gives its own risk estimate. The
   spread of the 200 answers is the system's uncertainty — a patient the
   models disagree on visibly gets a wide band.
2. **A second, model-free opinion.** "Patients Like You" finds the 50 most
   similar real patients and reports how many actually developed diabetes.
   Two independent methods agreeing builds trust; disagreement flags caution.
3. **The dataset's hidden missing data is fixed.** Zeros in Glucose, BMI,
   Insulin, BloodPressure and SkinThickness are physiologically impossible —
   they are undocumented missing values. We mark them missing and impute per
   training fold (no leakage). Most projects on this dataset miss this.
4. **Every reported metric is out-of-fold.** 5-fold cross-validation;
   the model is always scored on patients it never saw.
5. **The alert threshold is a stated rule** — recall ≥ 85% ("never miss more
   than 15% of true diabetics"), then maximize precision. Not a magic number.
6. **Explanations without jargon.** Personal risk drivers = "replace your
   glucose with a typical value → risk falls X points". What-if simulator =
   re-run all 200 models with one lifestyle change applied.

## Architecture

```
datasets/
  diabetes.csv   Pima study, 768 patients
  heart.csv      UCI Cleveland study, 303 patients
src/edp/
  diseases/      One config per disease: features, intake form,
                 what-if scenarios, prevention rules  (base.py = contract)
  data.py        Data layer      hidden missing values → imputed per fold
  pipeline.py    Base learner    impute → scale → gradient boosting
  ensemble.py    Uncertainty Engine   200 bootstrap models → distribution
  neighbors.py   Patients Like You    standardized 50-nearest-neighbors
  risk.py        Decision layer  threshold from the recall rule; risk tiers
  drivers.py     Explanation     median-substitution risk drivers
  whatif.py      Explanation     generic scenario evaluation
  recommend.py   Prevention      shared Recommendation type
  train.py       Trains + honestly evaluates EVERY disease → models/<key>/
ui/              Streamlit dashboard (disease selector + 5 report sections)
tests/           pytest suite (unit + integration)
```

## Run it

```bash
pip install -r requirements.txt
python src/edp/train.py            # train + evaluate (~2 min, run once)
streamlit run ui/main.py           # launch the dashboard
pytest                             # run the test suite
```

## Honest performance (5-fold out-of-fold)

See `models/metrics.json` after training — the dashboard's **Data & Model
Lab** tab displays all metrics, the model comparison and the calibration
proof. In-sample numbers are never reported anywhere.

## Disclaimer

Educational project. Not medical advice, not clinically validated.
Dataset: National Institute of Diabetes and Digestive and Kidney Diseases
(Pima Indians Diabetes Database).
