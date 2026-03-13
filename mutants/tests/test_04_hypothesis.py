"""Property-based tests using Hypothesis.

TEACHING NOTES
==============
Example-based tests (test_unit.py, test_model.py) check a small set of
hand-picked inputs. Property-based testing asks:

  "Does this guarantee hold for *any* valid input, not just the ones I thought of?"

Hypothesis generates hundreds of random inputs that satisfy your constraints,
then tries to find one that breaks the property. If it does, it *shrinks* the
failing input to the smallest possible example, making it easy to debug.

Run these tests:
    pixi run test tests/test_hypothesis.py -v

To see Hypothesis in action when it finds a bug, try changing classify_risk()
in model.py to always return "LOW RISK":
    return "LOW RISK"
Then run the tests — Hypothesis will report the smallest probability >= 0.5
that it found to break the property.

Key concepts:
    @given       — declares the test as property-based with a strategy
    st.floats()  — generates random float values within the specified range
    assume()     — skip inputs that don't satisfy a precondition (use sparingly)
"""

import pandas as pd
from hypothesis import given, settings
from hypothesis import strategies as st

from ci_cd_template.model import (
    FEATURES,
    RISK_THRESHOLD,
    TARGET,
    classify_risk,
    train_model,
)

# ── Helpers ───────────────────────────────────────────────────────────────────

# A module-level model trained once and reused by all prediction property tests.
# This avoids training a model inside each generated test case (very slow).
_TRAINING_DATA = pd.DataFrame(
    {
        "age": [21900, 23725, 20075, 22640, 25550, 12775, 14600, 13505, 15695, 11315],
        "height": [165, 170, 158, 175, 162, 175, 158, 170, 165, 162],
        "weight": [85.0, 92.0, 78.0, 95.0, 88.0, 72.0, 55.0, 68.0, 62.0, 58.0],
        "gender": [1, 2, 1, 2, 1, 2, 1, 2, 1, 1],
        "ap_hi": [160, 170, 145, 155, 180, 115, 105, 120, 112, 110],
        "ap_lo": [100, 110, 95, 100, 110, 75, 68, 78, 72, 70],
        "cholesterol": [3, 3, 2, 3, 3, 1, 1, 1, 1, 1],
        "gluc": [2, 3, 1, 2, 3, 1, 1, 1, 1, 1],
        "smoke": [1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        "alco": [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        "active": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
        TARGET: [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    }
)
_MODEL = train_model(_TRAINING_DATA, target=TARGET)


# ── Strategies (input generators) ─────────────────────────────────────────────

# Each strategy generates random valid values for one feature column.
patient_strategy = st.fixed_dictionaries(
    {
        "age": st.integers(min_value=10950, max_value=25550),  # 30–70 years
        "height": st.integers(min_value=140, max_value=210),  # cm
        "weight": st.floats(min_value=40.0, max_value=200.0, allow_nan=False),
        "gender": st.sampled_from([1, 2]),
        "ap_hi": st.integers(min_value=70, max_value=250),  # mmHg
        "ap_lo": st.integers(min_value=40, max_value=150),
        "cholesterol": st.sampled_from([1, 2, 3]),
        "gluc": st.sampled_from([1, 2, 3]),
        "smoke": st.sampled_from([0, 1]),
        "alco": st.sampled_from([0, 1]),
        "active": st.sampled_from([0, 1]),
    }
)


# ── Property tests for classify_risk() ───────────────────────────────────────


@given(prob=st.floats(min_value=0.0, max_value=1.0, allow_nan=False))
def test_classify_risk_always_returns_valid_label(prob):
    """classify_risk() must always return exactly one of two strings."""
    result = classify_risk(prob)
    assert result in {"HIGH RISK", "LOW RISK"}


@given(prob=st.floats(min_value=RISK_THRESHOLD, max_value=1.0, allow_nan=False))
def test_classify_risk_high_for_any_probability_at_or_above_threshold(prob):
    """Any probability >= RISK_THRESHOLD must be 'HIGH RISK'."""
    assert classify_risk(prob) == "HIGH RISK"


@given(prob=st.floats(min_value=0.0, max_value=RISK_THRESHOLD - 1e-9, allow_nan=False))
def test_classify_risk_low_for_any_probability_below_threshold(prob):
    """Any probability strictly below RISK_THRESHOLD must be 'LOW RISK'."""
    assert classify_risk(prob) == "LOW RISK"


# ── Property tests for model predictions ──────────────────────────────────────


@settings(max_examples=50)  # reduce to keep the test suite fast
@given(patient=patient_strategy)
def test_prediction_is_always_binary(patient):
    """For any valid patient, the model must predict exactly 0 or 1."""
    X = pd.DataFrame([patient])[FEATURES]
    pred = int(_MODEL.predict(X)[0])
    assert pred in {0, 1}, f"Expected 0 or 1, got {pred}"


@settings(max_examples=50)
@given(patient=patient_strategy)
def test_probability_is_always_in_unit_interval(patient):
    """For any valid patient, predict_proba must return a value in [0, 1]."""
    X = pd.DataFrame([patient])[FEATURES]
    proba = float(_MODEL.predict_proba(X)[0][1])
    assert 0.0 <= proba <= 1.0, f"Probability out of range: {proba}"


@settings(max_examples=50)
@given(patient=patient_strategy)
def test_risk_label_matches_predicted_label(patient):
    """The risk label from classify_risk must be consistent with the binary label."""
    X = pd.DataFrame([patient])[FEATURES]
    pred = int(_MODEL.predict(X)[0])
    proba = float(_MODEL.predict_proba(X)[0][1])
    label = classify_risk(proba)
    if pred == 1:
        assert label == "HIGH RISK"
    else:
        assert label == "LOW RISK"
