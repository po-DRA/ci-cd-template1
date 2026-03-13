"""Shared test fixtures for the ci_cd_template test suite."""

import pandas as pd
import pytest

from ci_cd_template.model import train_model


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Small synthetic cardiovascular dataset with clear class separation.

    High-risk patients (cardio=1): older age, high blood pressure, high cholesterol.
    Low-risk patients (cardio=0): younger, normal BP, normal cholesterol, active.
    """
    return pd.DataFrame(
        {
            # age in days: ~60 yr = 21900, ~35 yr = 12775
            "age": [
                21900,
                23725,
                20075,
                22640,
                25550,
                12775,
                14600,
                13505,
                15695,
                11315,
            ],
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
            "cardio": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        }
    )


@pytest.fixture
def trained_model(sample_df):
    """A freshly trained LogisticRegression pipeline (no file I/O required)."""
    return train_model(sample_df, target="cardio")


@pytest.fixture
def high_risk_patient() -> dict:
    """Feature dict for a clearly high-risk patient (expected: cardio=1)."""
    return {
        "age": 23360,  # ~64 years
        "height": 170,
        "weight": 92.0,
        "gender": 2,
        "ap_hi": 170,  # high systolic
        "ap_lo": 110,  # high diastolic
        "cholesterol": 3,  # well above normal
        "gluc": 3,
        "smoke": 1,
        "alco": 1,
        "active": 0,
    }


@pytest.fixture
def low_risk_patient() -> dict:
    """Feature dict for a clearly low-risk patient (expected: cardio=0)."""
    return {
        "age": 12410,  # ~34 years
        "height": 175,
        "weight": 68.0,
        "gender": 2,
        "ap_hi": 115,  # normal systolic
        "ap_lo": 75,  # normal diastolic
        "cholesterol": 1,  # normal
        "gluc": 1,
        "smoke": 0,
        "alco": 0,
        "active": 1,
    }
