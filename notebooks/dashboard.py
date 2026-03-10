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
    # Resolve model path relative to this notebook's location
    MODEL_PATH = Path(__file__).parent.parent / "model" / "model.joblib"
    model = joblib.load(MODEL_PATH)

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
    label = int(model.predict(X)[0])
    probability = float(model.predict_proba(X)[0][1])
    risk_label = "HIGH RISK" if label == 1 else "LOW RISK"

    age_years = round(patient["age"] / 365)
    chol_map = {1: "Normal", 2: "Above normal", 3: "Well above normal"}
    gluc_map  = {1: "Normal", 2: "Above normal", 3: "Well above normal"}

    return (
        MODEL_PATH,
        X,
        age_years,
        chol_map,
        gluc_map,
        label,
        model,
        patient,
        probability,
        risk_label,
    )


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
    return


if __name__ == "__main__":
    app.run()
