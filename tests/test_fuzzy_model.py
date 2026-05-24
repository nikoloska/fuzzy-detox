"""
Unit tests for fuzzy_engine_v4 — Mamdani FIS with 4-level hierarchy.
Run with: pytest tests/test_fuzzy_model.py -v
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from fuzzy_engine_v4 import evaluate_fuzzy_system


# ─── Fixtures ────────────────────────────────────────────────

@pytest.fixture
def balanced_user():
    return evaluate_fuzzy_system(10, 5, 10, 8)

@pytest.fixture
def night_owl():
    return evaluate_fuzzy_system(110, 55, 160, 85)

@pytest.fixture
def borderline():
    return evaluate_fuzzy_system(50, 28, 55, 40)


# ─── Class 1: Output structure ───────────────────────────────

class TestOutputStructure:
    def test_returns_dict(self, balanced_user):
        assert isinstance(balanced_user, dict)

    def test_has_inputs_key(self, balanced_user):
        assert "inputs" in balanced_user

    def test_has_outputs_key(self, balanced_user):
        assert "outputs" in balanced_user

    def test_has_labels_key(self, balanced_user):
        assert "labels" in balanced_user

    def test_has_recommendation(self, balanced_user):
        assert "recommendation" in balanced_user
        assert isinstance(balanced_user["recommendation"], str)

    def test_outputs_has_four_variables(self, balanced_user):
        keys = balanced_user["outputs"].keys()
        assert set(keys) == {"FocusQuality", "SleepQuality", "DigitalOverload", "HabitBalance"}


# ─── Class 2: Output ranges ──────────────────────────────────

class TestOutputRanges:
    @pytest.mark.parametrize("inputs", [
        (10, 5, 10, 8),
        (110, 55, 160, 85),
        (50, 28, 55, 40),
        (0, 0, 0, 0),
        (150, 80, 180, 100),
    ])
    def test_habit_balance_in_range(self, inputs):
        r = evaluate_fuzzy_system(*inputs)
        hb = r["outputs"]["HabitBalance"]
        assert 0 <= hb <= 10, f"HabitBalance {hb} out of range for inputs {inputs}"

    @pytest.mark.parametrize("inputs", [
        (10, 5, 10, 8),
        (110, 55, 160, 85),
    ])
    def test_all_outputs_in_range(self, inputs):
        r = evaluate_fuzzy_system(*inputs)
        for key, val in r["outputs"].items():
            assert 0 <= val <= 10, f"{key}={val} out of range"


# ─── Class 3: Profile ordering (monotonicity) ─────────────────

class TestProfileOrdering:
    def test_balanced_higher_than_night_owl(self, balanced_user, night_owl):
        assert balanced_user["outputs"]["HabitBalance"] > night_owl["outputs"]["HabitBalance"]

    def test_balanced_has_high_focus(self, balanced_user):
        assert balanced_user["outputs"]["FocusQuality"] >= 6.0

    def test_night_owl_has_low_sleep(self, night_owl):
        assert night_owl["outputs"]["SleepQuality"] <= 4.5

    def test_night_owl_has_high_overload(self, night_owl):
        assert night_owl["outputs"]["DigitalOverload"] >= 6.0

    def test_balanced_habitbalance_above_6(self, balanced_user):
        assert balanced_user["outputs"]["HabitBalance"] >= 6.0

    def test_night_owl_habitbalance_below_4(self, night_owl):
        assert night_owl["outputs"]["HabitBalance"] <= 4.0


# ─── Class 4: Fuzzy smoothness (no abrupt jumps) ─────────────

class TestFuzzySmoothness:
    def test_no_abrupt_jump_at_threshold(self):
        """One extra screen glance must not change HabitBalance by more than 1.0."""
        r1 = evaluate_fuzzy_system(49, 20, 30, 30)
        r2 = evaluate_fuzzy_system(51, 20, 30, 30)
        diff = abs(r1["outputs"]["HabitBalance"] - r2["outputs"]["HabitBalance"])
        assert diff < 1.0, f"Abrupt jump detected: {diff:.2f} for 2-unit input change"

    def test_monotonic_decrease_with_glances(self):
        """Increasing ScreenGlances should not increase HabitBalance."""
        scores = [
            evaluate_fuzzy_system(g, 20, 30, 30)["outputs"]["HabitBalance"]
            for g in [20, 50, 90, 130]
        ]
        for i in range(len(scores) - 1):
            assert scores[i] >= scores[i+1] - 0.5, \
                f"HabitBalance increased from {scores[i]:.2f} to {scores[i+1]:.2f}"


# ─── Class 5: Labels ─────────────────────────────────────────

class TestLabels:
    def test_balanced_user_label(self, balanced_user):
        assert balanced_user["labels"]["HabitBalance"] == "High"

    def test_night_owl_label(self, night_owl):
        assert night_owl["labels"]["HabitBalance"] == "Low"

    def test_borderline_label(self, borderline):
        assert borderline["labels"]["HabitBalance"] == "Medium"

    def test_labels_are_valid_strings(self, balanced_user):
        valid = {"Low", "Medium", "High"}
        for key, label in balanced_user["labels"].items():
            assert label in valid, f"{key} label '{label}' not in {valid}"


# ─── Class 6: Input clamping ─────────────────────────────────

class TestInputClamping:
    def test_negative_inputs_clamped(self):
        r = evaluate_fuzzy_system(-10, -5, -20, -50)
        assert r["outputs"]["HabitBalance"] is not None

    def test_overflow_inputs_clamped(self):
        r = evaluate_fuzzy_system(999, 999, 999, 999)
        for val in r["outputs"].values():
            assert 0 <= val <= 10
