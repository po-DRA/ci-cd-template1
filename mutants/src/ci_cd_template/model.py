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
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


def classify_risk(probability: float) -> str:
    args = [probability]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_classify_risk__mutmut_orig, x_classify_risk__mutmut_mutants, args, kwargs, None)


def x_classify_risk__mutmut_orig(probability: float) -> str:
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


def x_classify_risk__mutmut_1(probability: float) -> str:
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
    if 0.0 <= probability <= 1.0:
        raise ValueError(f"probability must be in [0, 1], got {probability}")
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_2(probability: float) -> str:
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
    if not 1.0 <= probability <= 1.0:
        raise ValueError(f"probability must be in [0, 1], got {probability}")
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_3(probability: float) -> str:
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
    if not 0.0 < probability <= 1.0:
        raise ValueError(f"probability must be in [0, 1], got {probability}")
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_4(probability: float) -> str:
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
    if not 0.0 <= probability < 1.0:
        raise ValueError(f"probability must be in [0, 1], got {probability}")
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_5(probability: float) -> str:
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
    if not 0.0 <= probability <= 2.0:
        raise ValueError(f"probability must be in [0, 1], got {probability}")
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_6(probability: float) -> str:
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
        raise ValueError(None)
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_7(probability: float) -> str:
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
    return "XXHIGH RISKXX" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_8(probability: float) -> str:
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
    return "high risk" if probability >= RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_9(probability: float) -> str:
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
    return "HIGH RISK" if probability > RISK_THRESHOLD else "LOW RISK"


def x_classify_risk__mutmut_10(probability: float) -> str:
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
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "XXLOW RISKXX"


def x_classify_risk__mutmut_11(probability: float) -> str:
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
    return "HIGH RISK" if probability >= RISK_THRESHOLD else "low risk"

x_classify_risk__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_classify_risk__mutmut_1': x_classify_risk__mutmut_1, 
    'x_classify_risk__mutmut_2': x_classify_risk__mutmut_2, 
    'x_classify_risk__mutmut_3': x_classify_risk__mutmut_3, 
    'x_classify_risk__mutmut_4': x_classify_risk__mutmut_4, 
    'x_classify_risk__mutmut_5': x_classify_risk__mutmut_5, 
    'x_classify_risk__mutmut_6': x_classify_risk__mutmut_6, 
    'x_classify_risk__mutmut_7': x_classify_risk__mutmut_7, 
    'x_classify_risk__mutmut_8': x_classify_risk__mutmut_8, 
    'x_classify_risk__mutmut_9': x_classify_risk__mutmut_9, 
    'x_classify_risk__mutmut_10': x_classify_risk__mutmut_10, 
    'x_classify_risk__mutmut_11': x_classify_risk__mutmut_11
}
x_classify_risk__mutmut_orig.__name__ = 'x_classify_risk'


def train_model(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
    args = [df, target]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_train_model__mutmut_orig, x_train_model__mutmut_mutants, args, kwargs, None)


def x_train_model__mutmut_orig(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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


def x_train_model__mutmut_1(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
    X = None
    y = df[target]

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_2(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
    X = df.drop(columns=None)
    y = df[target]

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_3(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
    y = None

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_4(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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

    pipeline = None
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_5(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
        None
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_6(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("XXscalerXX", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_7(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("SCALER", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_8(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("XXclassifierXX", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_9(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("CLASSIFIER", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_10(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("classifier", LogisticRegression(max_iter=None, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_11(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("classifier", LogisticRegression(max_iter=1000, random_state=None)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_12(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("classifier", LogisticRegression(random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_13(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("classifier", LogisticRegression(max_iter=1000, )),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_14(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("classifier", LogisticRegression(max_iter=1001, random_state=42)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_15(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
            ("classifier", LogisticRegression(max_iter=1000, random_state=43)),
        ]
    )
    pipeline.fit(X, y)
    return pipeline


def x_train_model__mutmut_16(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
    pipeline.fit(None, y)
    return pipeline


def x_train_model__mutmut_17(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
    pipeline.fit(X, None)
    return pipeline


def x_train_model__mutmut_18(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
    pipeline.fit(y)
    return pipeline


def x_train_model__mutmut_19(df: pd.DataFrame, target: str = TARGET) -> Pipeline:
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
    pipeline.fit(X, )
    return pipeline

x_train_model__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_train_model__mutmut_1': x_train_model__mutmut_1, 
    'x_train_model__mutmut_2': x_train_model__mutmut_2, 
    'x_train_model__mutmut_3': x_train_model__mutmut_3, 
    'x_train_model__mutmut_4': x_train_model__mutmut_4, 
    'x_train_model__mutmut_5': x_train_model__mutmut_5, 
    'x_train_model__mutmut_6': x_train_model__mutmut_6, 
    'x_train_model__mutmut_7': x_train_model__mutmut_7, 
    'x_train_model__mutmut_8': x_train_model__mutmut_8, 
    'x_train_model__mutmut_9': x_train_model__mutmut_9, 
    'x_train_model__mutmut_10': x_train_model__mutmut_10, 
    'x_train_model__mutmut_11': x_train_model__mutmut_11, 
    'x_train_model__mutmut_12': x_train_model__mutmut_12, 
    'x_train_model__mutmut_13': x_train_model__mutmut_13, 
    'x_train_model__mutmut_14': x_train_model__mutmut_14, 
    'x_train_model__mutmut_15': x_train_model__mutmut_15, 
    'x_train_model__mutmut_16': x_train_model__mutmut_16, 
    'x_train_model__mutmut_17': x_train_model__mutmut_17, 
    'x_train_model__mutmut_18': x_train_model__mutmut_18, 
    'x_train_model__mutmut_19': x_train_model__mutmut_19
}
x_train_model__mutmut_orig.__name__ = 'x_train_model'
