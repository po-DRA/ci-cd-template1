"""Unit tests for classify_risk() — a pure, isolated function.

TEACHING NOTES
==============
A *unit test* tests one small piece of logic in isolation, with no external
dependencies (no files, no database, no trained model).

classify_risk() is a perfect candidate:
  - It is a pure function: same input always gives the same output.
  - It has no side effects.
  - It is fast (no I/O, no ML computation).

Exercise: run these tests, then deliberately break classify_risk() by changing
the comparison operator or the threshold, and watch them fail.

    pixi run test tests/test_unit.py      # run only this file
    pixi run test tests/test_unit.py -v   # verbose output

To break the function, try changing model.py:
    return "HIGH RISK" if probability > RISK_THRESHOLD else "LOW RISK"
                                         ^ was >=
Then re-run the tests and observe which one fails and why.
"""

import pytest

from ci_cd_template.model import RISK_THRESHOLD, classify_risk

# ── Happy-path tests ──────────────────────────────────────────────────────────


def test_high_probability_is_high_risk():
    """A clearly elevated probability should be labelled HIGH RISK."""
    assert classify_risk(0.9) == "HIGH RISK"


def test_low_probability_is_low_risk():
    """A clearly low probability should be labelled LOW RISK."""
    assert classify_risk(0.1) == "LOW RISK"


def test_zero_probability_is_low_risk():
    """Probability of 0 (no risk at all) should be LOW RISK."""
    assert classify_risk(0.0) == "LOW RISK"


def test_full_probability_is_high_risk():
    """Probability of 1 (certain disease) should be HIGH RISK."""
    assert classify_risk(1.0) == "HIGH RISK"


# ── Boundary tests ────────────────────────────────────────────────────────────
# Boundary testing checks the exact value where behaviour switches.
# These are the most commonly missed cases in manual testing.


def test_at_threshold_is_high_risk():
    """Probability exactly at RISK_THRESHOLD should be HIGH RISK (>= boundary)."""
    assert classify_risk(RISK_THRESHOLD) == "HIGH RISK"


def test_just_below_threshold_is_low_risk():
    """A probability just below RISK_THRESHOLD should be LOW RISK."""
    just_below = RISK_THRESHOLD - 0.001
    assert classify_risk(just_below) == "LOW RISK"


def test_just_above_threshold_is_high_risk():
    """A probability just above RISK_THRESHOLD should be HIGH RISK."""
    just_above = RISK_THRESHOLD + 0.001
    assert classify_risk(just_above) == "HIGH RISK"


# ── Error-handling tests ───────────────────────────────────────────────────────
# Test that the function rejects invalid inputs rather than silently misbehaving.


def test_negative_probability_raises():
    """Negative probabilities are invalid and should raise ValueError."""
    with pytest.raises(ValueError, match="probability must be in"):
        classify_risk(-0.1)


def test_probability_above_one_raises():
    """Probabilities > 1 are invalid and should raise ValueError."""
    with pytest.raises(ValueError, match="probability must be in"):
        classify_risk(1.5)
