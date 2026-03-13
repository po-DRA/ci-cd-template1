"""Tests for the cardiovascular risk classifier."""

from pathlib import Path

import joblib
import pandas as pd
import pytest

from ci_cd_template.model import FEATURES, TARGET

# Resolve the model path relative to the project root (works from any cwd)
MODEL_PATH = Path(__file__).parent.parent / "model" / "model.joblib"


def test_train_model_returns_pipeline(trained_model):
    """train_model() should return a fitted sklearn Pipeline."""
    from sklearn.pipeline import Pipeline

    assert isinstance(trained_model, Pipeline)


def test_model_predicts_binary_labels(trained_model, sample_df):
    """All predictions should be 0 or 1 (binary classification)."""
    X = sample_df.drop(columns=[TARGET])
    preds = trained_model.predict(X)
    assert set(preds).issubset({0, 1})


def test_model_predicts_probabilities(trained_model, sample_df):
    """predict_proba() should return values in [0, 1] for each class."""
    X = sample_df.drop(columns=[TARGET])
    proba = trained_model.predict_proba(X)
    assert proba.shape[1] == 2
    assert (proba >= 0).all() and (proba <= 1).all()


def test_high_risk_patient_classified_as_cardio(trained_model, high_risk_patient):
    """A clearly high-risk patient profile should be predicted as cardio=1."""
    X = pd.DataFrame([high_risk_patient])[FEATURES]
    pred = trained_model.predict(X)[0]
    assert pred == 1, f"Expected cardio=1 for high-risk patient, got {pred}"


def test_low_risk_patient_classified_as_no_cardio(trained_model, low_risk_patient):
    """A clearly low-risk patient profile should be predicted as cardio=0."""
    X = pd.DataFrame([low_risk_patient])[FEATURES]
    pred = trained_model.predict(X)[0]
    assert pred == 0, f"Expected cardio=0 for low-risk patient, got {pred}"


@pytest.mark.skipif(
    not MODEL_PATH.exists(),
    reason="model/model.joblib not found — run `pixi run train` first",
)
def test_saved_model_predicts_high_risk(high_risk_patient):
    """The persisted model should correctly flag a high-risk patient."""
    model = joblib.load(MODEL_PATH)
    X = pd.DataFrame([high_risk_patient])[FEATURES]
    pred = model.predict(X)[0]
    assert pred == 1
