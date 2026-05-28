"""
crisp_engine.py
===============
A rule-based (crisp / if-else) baseline that mirrors the exact same
public interface as fuzzy_engine.py:

    evaluate_crisp_system(screen_glances, idle_checking,
                          late_night_use, social_media) -> dict

Current crisp thresholds:
  ScreenGlances : Low <= 32.00,  Medium 32.00–74.62,  High >= 74.62
  IdleChecking  : Low <= 16.67,  Medium 16.67–46.28,  High >= 46.28
  LateNightUse  : Low <= 22.50,  Medium 22.50–45.25,  High >= 45.25
  SocialMedia   : Low <= 20.00,  Medium 20.00–48.18,  High >= 48.18

This design intentionally makes the crisp baseline boundary-sensitive:
a tiny change around a threshold can switch the class completely, while
the fuzzy system changes gradually through overlapping memberships.
"""

# ─── HELPERS ────────────────────────────────────────────────────────────────

def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(float(value), maximum))


def _classify(value, low_max, high_min):
    """Return 'low', 'medium', or 'high' for a crisp value."""
    if value <= low_max:
        return "low"
    if value >= high_min:
        return "high"
    return "medium"


def _positive_label(score: float) -> str:
    if score < 3.5:
        return "Low"
    if score < 6.5:
        return "Medium"
    return "High"


def _overload_label(score: float) -> str:
    return _positive_label(score)


# ─── CRISP SCORE TABLES ──────────────────────────────────────────────────────
# Each output is a fixed score (0–10) based on crisp class combinations.
# Where multiple rules could fire, the most specific (most inputs specified)
# takes priority.

# FocusQuality scores  (sg_class, ic_class) → score
_FOCUS_RULES = {
    ("low",  "low"):    8.5,
    ("low",  "medium"): 7.0,
    ("low",  "high"):   4.0,
    ("medium","low"):   7.0,
    ("medium","medium"):5.5,
    ("medium","high"):  3.0,
    ("high", "low"):    4.0,
    ("high", "medium"): 2.5,
    ("high", "high"):   1.5,
}

# SleepQuality scores  (ln_class, sg_class) → score
_SLEEP_RULES = {
    ("low",  "low"):    8.5,
    ("low",  "medium"): 7.5,
    ("low",  "high"):   6.0,
    ("medium","low"):   6.0,
    ("medium","medium"):5.0,
    ("medium","high"):  3.5,
    ("high", "low"):    3.0,
    ("high", "medium"): 2.0,
    ("high", "high"):   1.5,
}

# DigitalOverload scores  (sg_class, sm_class) → score
_OVERLOAD_RULES = {
    ("low",  "low"):    1.5,
    ("low",  "medium"): 3.5,
    ("low",  "high"):   5.5,
    ("medium","low"):   3.5,
    ("medium","medium"):5.5,
    ("medium","high"):  7.0,
    ("high", "low"):    5.5,
    ("high", "medium"): 7.5,
    ("high", "high"):   9.0,
}

# ─── THRESHOLDS (derived from fuzzy MF crossover points) ────────────────────
_SG_LOW_MAX  = 32.00;  _SG_HIGH_MIN  = 74.62
_IC_LOW_MAX  = 16.67;  _IC_HIGH_MIN  = 46.28
_LN_LOW_MAX  = 22.50;  _LN_HIGH_MIN  = 45.25
_SM_LOW_MAX  = 20.00;  _SM_HIGH_MIN  = 48.18


def _recommendation(focus: float, sleep: float,
                    overload: float, habit: float) -> str:
    if habit >= 7.0:
        return "Your digital rhythm looks balanced. Keep the current pattern stable."
    if overload >= 7.0:
        return "Digital overload is high. Reduce social-media-heavy sessions and idle checking."
    if sleep < 4.5:
        return "Sleep quality is weak. Reduce late-night use after 22:00."
    if focus < 4.5:
        return "Focus quality is weak. Reduce screen glances and habitual idle checks."
    return "The pattern is moderate. Small reductions in checking behaviour could improve balance."


# ─── PUBLIC API ──────────────────────────────────────────────────────────────

def evaluate_crisp_system(
        screen_glances_value: float,
        idle_checking_value:  float,
        late_night_use_value: float,
        social_media_value:   float,
) -> dict:
    """
    Evaluate digital habits using crisp if-else logic.

    Parameters
    ----------
    screen_glances_value : float  0–150
    idle_checking_value  : float  0–80
    late_night_use_value : float  0–180
    social_media_value   : float  0–100

    Returns
    -------
    dict with keys:
        inputs, outputs, labels, recommendation, classes
    """
    sg = _clamp(screen_glances_value, 0, 150)
    ic = _clamp(idle_checking_value,  0, 80)
    ln = _clamp(late_night_use_value, 0, 120)
    sm = _clamp(social_media_value,   0, 100)

    # Classify each input
    sg_cls = _classify(sg, _SG_LOW_MAX, _SG_HIGH_MIN)
    ic_cls = _classify(ic, _IC_LOW_MAX, _IC_HIGH_MIN)
    ln_cls = _classify(ln, _LN_LOW_MAX, _LN_HIGH_MIN)
    sm_cls = _classify(sm, _SM_LOW_MAX, _SM_HIGH_MIN)

    # Look up crisp scores
    focus    = round(_FOCUS_RULES[(sg_cls, ic_cls)],    2)
    sleep    = round(_SLEEP_RULES[(ln_cls, sg_cls)],    2)
    overload = round(_OVERLOAD_RULES[(sg_cls, sm_cls)], 2)

    habit = round(
        0.4 * focus + 0.4 * sleep + 0.2 * (10 - overload),
        2
    )

    return {
        "inputs": {
            "ScreenGlances":    sg,
            "IdleChecking":     ic,
            "LateNightUse":     ln,
            "SocialMediaUsage": sm,
        },
        "classes": {
            "ScreenGlances":    sg_cls,
            "IdleChecking":     ic_cls,
            "LateNightUse":     ln_cls,
            "SocialMediaUsage": sm_cls,
        },
        "outputs": {
            "FocusQuality":    focus,
            "SleepQuality":    sleep,
            "DigitalOverload": overload,
            "HabitBalance":    habit,
        },
        "labels": {
            "FocusQuality":    _positive_label(focus),
            "SleepQuality":    _positive_label(sleep),
            "DigitalOverload": _overload_label(overload),
            "HabitBalance":    _positive_label(habit),
        },
        "recommendation": _recommendation(focus, sleep, overload, habit),
    }


# ─── QUICK SMOKE TEST ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import json

    test_cases = [
        ("Balanced User",        25, 10, 10, 20),
        ("Night Owl",            60, 28,110, 70),
        ("Distracted Achiever",  98, 50, 45, 68),
        ("Focused Worker",       30,  8, 35, 18),
        ("Borderline SG=50",     50, 20, 30, 40),
    ]

    print(f"{'Profile':<25} {'HabitBalance':>13} {'Focus':>7} {'Sleep':>7} {'Overload':>9}")
    print("-" * 65)
    for name, sg, ic, ln, sm in test_cases:
        r = evaluate_crisp_system(sg, ic, ln, sm)
        o = r["outputs"]
        print(f"{name:<25} {o['HabitBalance']:>13.2f} {o['FocusQuality']:>7.2f} "
              f"{o['SleepQuality']:>7.2f} {o['DigitalOverload']:>9.2f}")
