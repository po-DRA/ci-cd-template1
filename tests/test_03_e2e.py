"""End-to-end (E2E) test for the full data → train → predict pipeline.

TEACHING NOTES
==============
End-to-end tests verify that all pieces of the system work together correctly,
from the real input (data.csv) all the way to the final output (a prediction).

Compare to unit tests:
  Unit test  — tests ONE function in isolation (no files, no pipeline)
  E2E test   — tests the WHOLE system from start to finish using real artefacts

Trade-offs:
  + Catches integration bugs that unit tests miss
  + Tests the system the way a user/production code would use it
  - Slower (reads files, trains a model)
  - Harder to pinpoint the cause of failure
  - Requires the full environment to be set up

Design exercise (think through, don't just run):
  Suppose you had a web API that receives patient data and returns a risk score.
  What would an E2E test for *that* look like?
    1. Start the API server.
    2. POST a patient payload to /predict.
    3. Assert the response JSON has the right shape and a valid risk label.
    4. Shut down the server.

  The test here does the same thing, just without the HTTP layer.

Run this file alone:
    pixi run test tests/test_e2e.py -v

To break this test, try:
  - Deleting data/data.csv  →  FileNotFoundError during training
  - Setting a very high fail_under threshold in pyproject.toml
  - Changing RISK_THRESHOLD to 1.1 in model.py  →  all labels become "LOW RISK"
    and the accuracy assertion may fail
"""

from pathlib import Path

import pandas as pd
import pytest

from ci_cd_template.model import FEATURES, TARGET, classify_risk, train_model
from ci_cd_template.predict import predict

# Locate project root relative to this test file (works from any working directory)
ROOT = Path(__file__).parent.parent
DATA_PATH = ROOT / "data" / "data.csv"
MODEL_PATH = ROOT / "model" / "model.joblib"


@pytest.fixture(scope="module")
def full_pipeline():
    """Load real data, train a model, and return both for assertions."""
    df = pd.read_csv(DATA_PATH)
    model = train_model(df, target=TARGET)
    return model, df


def test_data_file_exists():
    """data/data.csv must exist and be readable before training can happen."""
    assert DATA_PATH.exists(), f"Missing data file: {DATA_PATH}"
    df = pd.read_csv(DATA_PATH)
    assert len(df) > 0, "data.csv is empty"


def test_data_has_expected_columns():
    """data.csv must contain all feature columns plus the target."""
    df = pd.read_csv(DATA_PATH)
    expected = set(FEATURES) | {TARGET}
    assert expected.issubset(df.columns), (
        f"Missing columns: {expected - set(df.columns)}"
    )


def test_data_target_is_binary():
    """The cardio column must contain only 0 and 1 values."""
    df = pd.read_csv(DATA_PATH)
    unique_values = set(df[TARGET].unique())
    assert unique_values.issubset({0, 1}), (
        f"cardio column contains unexpected values: {unique_values}"
    )


def test_pipeline_trains_and_predicts_on_real_data(full_pipeline):
    """The model must train on real data and return predictions for all rows."""
    model, df = full_pipeline
    X = df[FEATURES]
    preds = model.predict(X)
    assert len(preds) == len(df)
    assert set(preds).issubset({0, 1})


def test_pipeline_accuracy_above_threshold(full_pipeline):
    """The model should achieve at least 80% accuracy on its own training data.

    Note: training accuracy is NOT a measure of generalisability, but it tells
    us the model has at least learned *something* from the data.
    For a real project you would use a held-out test set or cross-validation.
    """
    model, df = full_pipeline
    X = df[FEATURES]
    y = df[TARGET]
    accuracy = (model.predict(X) == y).mean()
    assert accuracy >= 0.80, (
        f"Training accuracy too low: {accuracy:.1%} (expected >= 80%)"
    )


def test_risk_label_pipeline_end_to_end(full_pipeline):
    """Every prediction through the full pipeline must produce a valid risk label."""
    model, df = full_pipeline
    X = df[FEATURES]
    probas = model.predict_proba(X)[:, 1]  # probability of cardio=1
    labels = [classify_risk(float(p)) for p in probas]
    assert all(label in {"HIGH RISK", "LOW RISK"} for label in labels)


@pytest.mark.skipif(
    not MODEL_PATH.exists(),
    reason="model/model.joblib not found — run pixi run train first",
)
def test_predict_function_end_to_end():
    """The predict() function loads the saved model and returns a valid result dict."""
    high_risk_patient = {
        "age": 21900,
        "height": 165,
        "weight": 95.0,
        "gender": 1,
        "ap_hi": 160,
        "ap_lo": 100,
        "cholesterol": 3,
        "gluc": 2,
        "smoke": 1,
        "alco": 0,
        "active": 0,
    }
    result = predict(high_risk_patient, model_path=MODEL_PATH)
    assert set(result.keys()) == {"cardio", "probability", "risk_label"}
    assert result["cardio"] in {0, 1}
    assert 0.0 <= result["probability"] <= 1.0
    assert result["risk_label"] in {"HIGH RISK", "LOW RISK"}
