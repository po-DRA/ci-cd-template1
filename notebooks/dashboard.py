import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import joblib
    import pandas as pd
    from pathlib import Path
    from ci_cd_template.model import FEATURES
    return FEATURES, Path, joblib, mo, pd


@app.cell
def _(FEATURES, Path, joblib, pd):
    # Resolve paths relative to this notebook's location
    ROOT = Path(__file__).parent.parent
    MODEL_PATH = ROOT / "model" / "model.joblib"
    DATA_PATH  = ROOT / "data" / "data.csv"

    model = joblib.load(MODEL_PATH)
    df    = pd.read_csv(DATA_PATH)

    # --- Example patient (edit these values to try different profiles) ---
    patient = {
        "age":         21900,   # days  (~60 years: age_years * 365)
        "height":      165,     # cm
        "weight":      85.0,    # kg
        "gender":      1,       # 1 = woman, 2 = man
        "ap_hi":       160,     # systolic blood pressure (mmHg)
        "ap_lo":       100,     # diastolic blood pressure (mmHg)
        "cholesterol": 3,       # 1=normal  2=above normal  3=well above normal
        "gluc":        2,       # 1=normal  2=above normal  3=well above normal
        "smoke":       1,       # 0=no  1=yes
        "alco":        0,       # 0=no  1=yes
        "active":      0,       # 0=no  1=yes
    }

    X = pd.DataFrame([patient])[FEATURES]
    label       = int(model.predict(X)[0])
    probability = float(model.predict_proba(X)[0][1])
    risk_label  = "HIGH RISK" if label == 1 else "LOW RISK"

    age_years = round(patient["age"] / 365)
    chol_map  = {1: "Normal", 2: "Above normal", 3: "Well above normal"}
    gluc_map  = {1: "Normal", 2: "Above normal", 3: "Well above normal"}

    # --- Sensitivity: vary one feature at a time from the baseline patient ---
    _scenarios = [
        ("Baseline (high-risk patient)",          patient),
        ("Lower BP: ap_hi 160 → 120",             {**patient, "ap_hi": 120, "ap_lo": 75}),
        ("Normal cholesterol: 3 → 1",             {**patient, "cholesterol": 1}),
        ("Non-smoker: smoke 1 → 0",               {**patient, "smoke": 0}),
        ("Younger: age 60 → 35 years",            {**patient, "age": 12775}),
        ("All risk factors normalised",            {**patient, "ap_hi": 115, "ap_lo": 75,
                                                    "cholesterol": 1, "gluc": 1,
                                                    "smoke": 0, "age": 12775}),
    ]
    sensitivity_rows = []
    for _desc, _p in _scenarios:
        _prob = float(model.predict_proba(pd.DataFrame([_p])[FEATURES])[0][1])
        _lbl  = "HIGH RISK" if _prob >= 0.5 else "LOW RISK"
        sensitivity_rows.append((_desc, f"{_prob:.1%}", _lbl))

    return (
        DATA_PATH,
        MODEL_PATH,
        ROOT,
        X,
        age_years,
        chol_map,
        df,
        gluc_map,
        label,
        model,
        patient,
        probability,
        risk_label,
        sensitivity_rows,
    )


@app.cell
def _(df, mo):
    _n_high = int((df["cardio"] == 1).sum())
    _n_low  = int((df["cardio"] == 0).sum())

    # Add age_years as first column so learners can read age without mental arithmetic
    _df_display = df.head().copy()
    _df_display.insert(1, "age_years", (_df_display["age"] / 365).round().astype(int))

    mo.vstack([
        mo.md(f"""
## Dataset preview

{len(df)} patients · {len(df.columns)} columns · **{_n_high} high-risk** (cardio=1) · **{_n_low} low-risk** (cardio=0)

`age` is stored in days (original dataset format) — `age_years` is added here for readability.

**Column legend**

| Column | Full name | Unit / values |
|---|---|---|
| `age` | Age | days (÷ 365 = years) |
| `age_years` | Age in years | years (display only) |
| `height` | Height | cm |
| `weight` | Weight | kg |
| `gender` | Gender | 1 = woman · 2 = man |
| `ap_hi` | Systolic blood pressure | mmHg (normal < 130) |
| `ap_lo` | Diastolic blood pressure | mmHg (normal < 85) |
| `cholesterol` | Cholesterol level | 1 = normal · 2 = above normal · 3 = well above normal |
| `gluc` | Glucose level | 1 = normal · 2 = above normal · 3 = well above normal |
| `smoke` | Smoker | 0 = no · 1 = yes |
| `alco` | Alcohol intake | 0 = no · 1 = yes |
| `active` | Physically active | 0 = no · 1 = yes |
| `cardio` | Cardiovascular disease (target) | 0 = no disease · 1 = disease present |

> For a real project, full EDA goes here: distributions, correlations, missing-value checks.
        """),
        mo.ui.table(_df_display),
    ])


@app.cell
def _(age_years, chol_map, gluc_map, mo, patient, probability, risk_label):
    mo.md(f"""
# Cardiovascular Risk Dashboard

## Patient Profile

| Feature | Value |
|---------|-------|
| Age | {age_years} years ({patient['age']} days) |
| Height | {patient['height']} cm |
| Weight | {patient['weight']} kg |
| Gender | {"Woman" if patient['gender'] == 1 else "Man"} |
| Systolic BP (ap\\_hi) | {patient['ap_hi']} mmHg |
| Diastolic BP (ap\\_lo) | {patient['ap_lo']} mmHg |
| Cholesterol | {chol_map[patient['cholesterol']]} |
| Glucose | {gluc_map[patient['gluc']]} |
| Smoker | {"Yes" if patient['smoke'] else "No"} |
| Alcohol intake | {"Yes" if patient['alco'] else "No"} |
| Physically active | {"Yes" if patient['active'] else "No"} |

## Prediction

**Cardiovascular disease risk: {risk_label}**

Probability of cardiovascular disease: **{probability:.1%}**

> Model: Logistic Regression with StandardScaler (trained on synthetic data)
    """)


@app.cell
def _(mo, sensitivity_rows):
    _header = "| Scenario | Probability | Risk label |\n|---|---|---|\n"
    _rows   = "\n".join(
        f"| {desc} | {prob} | {lbl} |"
        for desc, prob, lbl in sensitivity_rows
    )
    mo.md(f"""
## Feature sensitivity

How does changing one risk factor at a time affect the prediction?

{_header}{_rows}

> Each row changes a single feature from the baseline patient above.
> The last row sets all modifiable risk factors to healthy values.
    """)


if __name__ == "__main__":
    app.run()
