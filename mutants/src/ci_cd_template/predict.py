from pathlib import Path

import joblib
import pandas as pd

from ci_cd_template.model import FEATURES, classify_risk

# Default path to the saved model, relative to the project root
MODEL_PATH = Path(__file__).parent.parent.parent / "model" / "model.joblib"
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


def predict(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    args = [patient, model_path]# type: ignore
    kwargs = {}# type: ignore
    return _mutmut_trampoline(x_predict__mutmut_orig, x_predict__mutmut_mutants, args, kwargs, None)


def x_predict__mutmut_orig(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_1(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = None
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_2(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(None)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_3(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = None
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_4(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame(None)[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_5(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = None
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_6(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(None)
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_7(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(None)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_8(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[1])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_9(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = None
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_10(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(None)
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_11(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(None)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_12(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[1][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_13(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][2])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_14(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "XXcardioXX": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_15(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "CARDIO": label,
        "probability": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_16(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "XXprobabilityXX": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_17(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "PROBABILITY": probability,
        "risk_label": classify_risk(probability),
    }


def x_predict__mutmut_18(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "XXrisk_labelXX": classify_risk(probability),
    }


def x_predict__mutmut_19(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "RISK_LABEL": classify_risk(probability),
    }


def x_predict__mutmut_20(patient: dict, model_path: Path = MODEL_PATH) -> dict:
    """Load the trained model and predict cardiovascular risk for one patient.

    Args:
        patient: Dictionary with keys matching FEATURES (see model.FEATURES).
                 Example::

                     {
                         "age": 21900,        # days (~60 years)
                         "height": 165,       # cm
                         "weight": 85.0,      # kg
                         "gender": 1,         # 1 or 2
                         "ap_hi": 160,        # systolic BP
                         "ap_lo": 100,        # diastolic BP
                         "cholesterol": 3,    # 1-3
                         "gluc": 2,           # 1-3
                         "smoke": 1,          # 0/1
                         "alco": 0,           # 0/1
                         "active": 0,         # 0/1
                     }

        model_path: Path to the saved joblib model file.

    Returns:
        Dictionary with:
            - "cardio": 0 (no disease) or 1 (disease present)
            - "probability": float probability of cardiovascular disease (0-1)
            - "risk_label": human-readable string from classify_risk()
    """
    model = joblib.load(model_path)
    df = pd.DataFrame([patient])[FEATURES]
    label = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])
    return {
        "cardio": label,
        "probability": probability,
        "risk_label": classify_risk(None),
    }

x_predict__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
'x_predict__mutmut_1': x_predict__mutmut_1, 
    'x_predict__mutmut_2': x_predict__mutmut_2, 
    'x_predict__mutmut_3': x_predict__mutmut_3, 
    'x_predict__mutmut_4': x_predict__mutmut_4, 
    'x_predict__mutmut_5': x_predict__mutmut_5, 
    'x_predict__mutmut_6': x_predict__mutmut_6, 
    'x_predict__mutmut_7': x_predict__mutmut_7, 
    'x_predict__mutmut_8': x_predict__mutmut_8, 
    'x_predict__mutmut_9': x_predict__mutmut_9, 
    'x_predict__mutmut_10': x_predict__mutmut_10, 
    'x_predict__mutmut_11': x_predict__mutmut_11, 
    'x_predict__mutmut_12': x_predict__mutmut_12, 
    'x_predict__mutmut_13': x_predict__mutmut_13, 
    'x_predict__mutmut_14': x_predict__mutmut_14, 
    'x_predict__mutmut_15': x_predict__mutmut_15, 
    'x_predict__mutmut_16': x_predict__mutmut_16, 
    'x_predict__mutmut_17': x_predict__mutmut_17, 
    'x_predict__mutmut_18': x_predict__mutmut_18, 
    'x_predict__mutmut_19': x_predict__mutmut_19, 
    'x_predict__mutmut_20': x_predict__mutmut_20
}
x_predict__mutmut_orig.__name__ = 'x_predict'
