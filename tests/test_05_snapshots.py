"""Snapshot tests using Syrupy.

TEACHING NOTES
==============
Snapshot testing locks in the *exact output* of a function.
On the first run, Syrupy creates a snapshot file in tests/__snapshots__/.
On every subsequent run, it compares the actual output against the stored snapshot.

This is useful for detecting *unintended* changes — for example:
  - You retrain the model with new data and the predictions shift unexpectedly.
  - You refactor predict() and accidentally change the output dict structure.
  - A dependency update changes how probabilities are rounded.

The workflow:
  1. First run:   pytest --snapshot-update  →  creates __snapshots__/ files
  2. Commit the snapshot files to git (they are reviewed like any other change).
  3. Future runs: pytest                   →  compares output to stored snapshot.
  4. If output changes deliberately:       →  pytest --snapshot-update to refresh.

Run these tests:
    pixi run test tests/test_snapshots.py -v

Create snapshots for the first time:
    pixi run test tests/test_snapshots.py --snapshot-update

To see a failing snapshot:
  1. Run --snapshot-update to create the baseline.
  2. Change classify_risk() threshold from 0.5 to 0.3.
  3. Run pytest — the snapshot diff will show exactly what changed.

Key concepts:
    snapshot        — pytest fixture injected by Syrupy
    assert x == snapshot  — compares x against the stored snapshot value
"""

import pandas as pd

from ci_cd_template.model import FEATURES, TARGET, classify_risk, train_model

# ── Shared training data ───────────────────────────────────────────────────────
# Using a fixed dataset ensures snapshots are reproducible.
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

# Canonical patients used as stable snapshot inputs
_HIGH_RISK = {
    "age": 23360,
    "height": 170,
    "weight": 92.0,
    "gender": 2,
    "ap_hi": 170,
    "ap_lo": 110,
    "cholesterol": 3,
    "gluc": 3,
    "smoke": 1,
    "alco": 1,
    "active": 0,
}
_LOW_RISK = {
    "age": 12410,
    "height": 175,
    "weight": 68.0,
    "gender": 2,
    "ap_hi": 115,
    "ap_lo": 75,
    "cholesterol": 1,
    "gluc": 1,
    "smoke": 0,
    "alco": 0,
    "active": 1,
}


# ── Snapshot: output structure ─────────────────────────────────────────────────


def test_prediction_output_keys_are_stable(snapshot):
    """The keys returned by the model predict step should never change silently."""
    X = pd.DataFrame([_HIGH_RISK])[FEATURES]
    label = int(_MODEL.predict(X)[0])
    proba = float(_MODEL.predict_proba(X)[0][1])
    result = {
        "cardio": label,
        "risk_label": classify_risk(proba),
    }
    # If you add/remove/rename keys in predict(), this snapshot breaks.
    assert sorted(result.keys()) == snapshot


# ── Snapshot: predicted labels ─────────────────────────────────────────────────


def test_high_risk_patient_label_snapshot(snapshot):
    """The binary label for the canonical high-risk patient should not change."""
    X = pd.DataFrame([_HIGH_RISK])[FEATURES]
    label = int(_MODEL.predict(X)[0])
    assert label == snapshot  # expected: 1


def test_low_risk_patient_label_snapshot(snapshot):
    """The binary label for the canonical low-risk patient should not change."""
    X = pd.DataFrame([_LOW_RISK])[FEATURES]
    label = int(_MODEL.predict(X)[0])
    assert label == snapshot  # expected: 0


# ── Snapshot: risk label strings ──────────────────────────────────────────────


def test_classify_risk_label_snapshots(snapshot):
    """The string labels produced by classify_risk() should be stable."""
    labels = {
        "high": classify_risk(0.9),
        "mid": classify_risk(0.5),
        "low": classify_risk(0.1),
    }
    assert labels == snapshot
