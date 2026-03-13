import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Feature columns expected by the model (in order)
FEATURES = [
    "age",  # int, days
    "height",  # int, cm
    "weight",  # float, kg
    "gender",  # categorical: 1 or 2
    "ap_hi",  # int, systolic blood pressure
    "ap_lo",  # int, diastolic blood pressure
    "cholesterol",  # 1: normal, 2: above normal, 3: well above normal
    "gluc",  # 1: normal, 2: above normal, 3: well above normal
    "smoke",  # binary
    "alco",  # binary
    "active",  # binary
]

TARGET = "cardio"  # binary: 0 = no disease, 1 = disease present

# Risk threshold: probabilities at or above this value are flagged as HIGH RISK
RISK_THRESHOLD = 0.5


def classify_risk(probability: float) -> str:
    """Convert a predicted probability into a human-readable risk label.

    This is a *pure function* with no side effects — it is easy to unit test
    in isolation, without training a model or loading any files.

    Separating this decision logic from the model pipeline is good practice:
    you can change the threshold or the label wording here, and the unit test
    immediately tells you whether the behaviour is still correct.

    Args:
        probability: Predicted probability of cardiovascular disease (0.0 – 1.0).

    Returns:
        "HIGH RISK" if probability >= RISK_THRESHOLD, otherwise "LOW RISK".

    Raises:
        ValueError: if probability is outside [0, 1].

    Examples:
        >>> classify_risk(0.9)
        'HIGH RISK'
        >>> classify_risk(0.3)
        'LOW RISK'
        >>> classify_risk(0.5)   # at boundary → HIGH RISK
        'HIGH RISK'
    """
    if not 0.0 <= probability <= 1.0:
        raise ValueError(f"probability must be in [0, 1], got {probability}")
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "LOW RISK"


def train_model(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
    """Train a logistic regression classifier for cardiovascular risk.

    Features are automatically scaled via a StandardScaler so that variables
    with very different magnitudes (e.g. age in days vs cholesterol 1-3) are
    treated fairly by the model.

    Args:
        df: DataFrame containing all feature columns and the target column.
        target: Name of the binary target column (default: "cardio").

    Returns:
        A fitted sklearn Pipeline (StandardScaler → LogisticRegression).
    """
    X = df.drop(columns=[target])
    y = df[target]

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def untested_helper(x):
    x = 1 + 2
    return x
