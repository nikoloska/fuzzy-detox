import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ============================================================
# Universes
# ============================================================

screen_glances_universe = np.arange(0, 151, 1)
idle_checking_universe = np.arange(0, 81, 1)
late_night_use_universe = np.arange(0, 181, 1)
social_media_universe = np.arange(0, 101, 1)
score_universe = np.arange(0, 10.1, 0.1)


# ============================================================
# Input variables
# ============================================================

screen_glances = ctrl.Antecedent(screen_glances_universe, "ScreenGlances")
idle_checking = ctrl.Antecedent(idle_checking_universe, "IdleChecking")
late_night_use = ctrl.Antecedent(late_night_use_universe, "LateNightUse")
social_media = ctrl.Antecedent(social_media_universe, "SocialMediaUsage")

screen_glances["low"] = fuzz.trapmf(screen_glances.universe, [0, 0, 20, 40])
screen_glances["medium"] = fuzz.trimf(screen_glances.universe, [20, 50, 90])
screen_glances["high"] = fuzz.trapmf(screen_glances.universe, [65, 90, 150, 150])

idle_checking["low"] = fuzz.trapmf(idle_checking.universe, [0, 0, 10, 20])
idle_checking["medium"] = fuzz.trimf(idle_checking.universe, [10, 30, 55])
idle_checking["high"] = fuzz.trapmf(idle_checking.universe, [40, 58, 80, 80])

late_night_use["low"] = fuzz.trapmf(late_night_use.universe, [0, 0, 10, 25])
late_night_use["medium"] = fuzz.trimf(late_night_use.universe, [15, 45, 85])
late_night_use["high"] = fuzz.trapmf(late_night_use.universe, [65, 90, 180, 180])

social_media["low"] = fuzz.trapmf(social_media.universe, [0, 0, 15, 30])
social_media["medium"] = fuzz.trimf(social_media.universe, [15, 40, 70])
social_media["high"] = fuzz.trapmf(social_media.universe, [55, 75, 100, 100])


# ============================================================
# Output variables
# ============================================================

focus_quality = ctrl.Consequent(score_universe, "FocusQuality")
sleep_quality = ctrl.Consequent(score_universe, "SleepQuality")
digital_overload = ctrl.Consequent(score_universe, "DigitalOverload")

focus_quality.defuzzify_method = "centroid"
sleep_quality.defuzzify_method = "centroid"
digital_overload.defuzzify_method = "centroid"

focus_quality["very_low"] = fuzz.trapmf(focus_quality.universe, [0, 0, 1.5, 3.0])
focus_quality["low"] = fuzz.trimf(focus_quality.universe, [2.0, 3.5, 5.0])
focus_quality["medium"] = fuzz.trimf(focus_quality.universe, [4.0, 5.5, 7.0])
focus_quality["medium_high"] = fuzz.trimf(focus_quality.universe, [5.5, 7.0, 8.5])
focus_quality["high"] = fuzz.trapmf(focus_quality.universe, [7.0, 8.5, 10, 10])

sleep_quality["low"] = fuzz.trapmf(sleep_quality.universe, [0, 0, 2.5, 4.5])
sleep_quality["medium"] = fuzz.trimf(sleep_quality.universe, [3.0, 5.0, 7.5])
sleep_quality["high"] = fuzz.trapmf(sleep_quality.universe, [6.0, 8.0, 10, 10])

digital_overload["low"] = fuzz.trapmf(digital_overload.universe, [0, 0, 2.5, 4.5])
digital_overload["medium"] = fuzz.trimf(digital_overload.universe, [3.0, 5.0, 7.5])
digital_overload["high"] = fuzz.trapmf(digital_overload.universe, [6.0, 8.0, 10, 10])


# ============================================================
# Rule bases
# ============================================================

focus_rules = [
    # Strong negative focus patterns
    ctrl.Rule(screen_glances["high"], focus_quality["low"]),
    ctrl.Rule(late_night_use["high"], focus_quality["low"]),
    ctrl.Rule(idle_checking["high"], focus_quality["very_low"]),
    ctrl.Rule(social_media["high"], focus_quality["low"]),

    # Strong positive focus patterns
    ctrl.Rule(screen_glances["low"] & social_media["low"], focus_quality["high"]),
    ctrl.Rule(
        screen_glances["low"] & idle_checking["low"] & late_night_use["low"],
        focus_quality["high"]
    ),

    # Moderate / realistic everyday patterns
    ctrl.Rule(screen_glances["medium"] & late_night_use["low"], focus_quality["medium_high"]),
    ctrl.Rule(screen_glances["medium"] & social_media["medium"], focus_quality["medium"]),
    ctrl.Rule(screen_glances["medium"] & late_night_use["medium"], focus_quality["medium"]),
    ctrl.Rule(idle_checking["medium"] & social_media["medium"], focus_quality["medium"]),
    ctrl.Rule(late_night_use["medium"] & social_media["medium"], focus_quality["medium"]),

    # Mixed cases
    ctrl.Rule(screen_glances["low"] & social_media["medium"], focus_quality["medium_high"]),
    ctrl.Rule(screen_glances["medium"] & social_media["low"], focus_quality["medium_high"]),
    ctrl.Rule(idle_checking["low"] & late_night_use["medium"], focus_quality["medium"]),
]

sleep_rules = [
    ctrl.Rule(late_night_use["low"] & screen_glances["low"] & idle_checking["low"], sleep_quality["high"]),
    ctrl.Rule(late_night_use["medium"] & screen_glances["medium"], sleep_quality["medium"]),
    ctrl.Rule(late_night_use["high"] & social_media["high"], sleep_quality["low"]),
    ctrl.Rule(late_night_use["high"] & screen_glances["high"], sleep_quality["low"]),
    ctrl.Rule(late_night_use["high"] & idle_checking["high"], sleep_quality["low"]),
    ctrl.Rule(late_night_use["medium"] & social_media["high"], sleep_quality["medium"]),
    ctrl.Rule(screen_glances["low"] & late_night_use["high"], sleep_quality["low"]),
]

digital_overload_rules = [
    ctrl.Rule(screen_glances["high"] & social_media["high"], digital_overload["high"]),
    ctrl.Rule(idle_checking["high"] & social_media["high"], digital_overload["high"]),
    ctrl.Rule(late_night_use["high"] & social_media["high"], digital_overload["high"]),
    ctrl.Rule(screen_glances["high"] & idle_checking["high"] & late_night_use["high"], digital_overload["high"]),

    ctrl.Rule(late_night_use["high"] & social_media["low"], digital_overload["medium"]),
    ctrl.Rule(screen_glances["high"] & social_media["low"], digital_overload["medium"]),
    ctrl.Rule(idle_checking["high"] & social_media["low"], digital_overload["medium"]),
    ctrl.Rule(screen_glances["medium"] & social_media["medium"], digital_overload["medium"]),
    ctrl.Rule(screen_glances["low"] & social_media["high"], digital_overload["medium"]),

    ctrl.Rule(screen_glances["low"] & social_media["low"], digital_overload["low"]),
    ctrl.Rule(screen_glances["low"] & idle_checking["low"] & late_night_use["low"], digital_overload["low"]),
]

focus_system = ctrl.ControlSystem(focus_rules)
sleep_system = ctrl.ControlSystem(sleep_rules)
digital_overload_system = ctrl.ControlSystem(digital_overload_rules)


# ============================================================
# Public evaluation function
# ============================================================

def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(float(value), maximum))


def _positive_label(score: float) -> str:
    if score < 3.5:
        return "Low"
    if score < 6.5:
        return "Medium"
    return "High"


def _overload_label(score: float) -> str:
    if score < 3.5:
        return "Low"
    if score < 6.5:
        return "Medium"
    return "High"


def _recommendation(focus: float, sleep: float, overload: float, habit: float) -> str:
    if habit >= 7.0:
        return "Your digital rhythm looks balanced. Keep the current pattern stable."
    if overload >= 7.0:
        return "Digital overload is high. Reduce social-media-heavy sessions and idle checking."
    if sleep < 4.5:
        return "Sleep quality is weak. Reduce late-night use after 22:00."
    if focus < 4.5:
        return "Focus quality is weak. Reduce screen glances and habitual idle checks."
    return "The pattern is moderate. Small reductions in checking behavior could improve balance."

def _safe_output(sim, output_name: str, default: float = 5.0) -> float:
    if output_name not in sim.output:
        return default
    return float(sim.output[output_name])

def evaluate_fuzzy_system(
        screen_glances_value: float,
        idle_checking_value: float,
        late_night_use_value: float,
        social_media_value: float,
) -> dict:
    screen_glances_value = _clamp(screen_glances_value, 0, 150)
    idle_checking_value = _clamp(idle_checking_value, 0, 80)
    late_night_use_value = _clamp(late_night_use_value, 0, 180)
    social_media_value = _clamp(social_media_value, 0, 100)

    focus_sim = ctrl.ControlSystemSimulation(focus_system)
    sleep_sim = ctrl.ControlSystemSimulation(sleep_system)
    overload_sim = ctrl.ControlSystemSimulation(digital_overload_system)

    for sim in [focus_sim, sleep_sim, overload_sim]:
        sim.input["ScreenGlances"] = screen_glances_value
        sim.input["IdleChecking"] = idle_checking_value
        sim.input["LateNightUse"] = late_night_use_value
        sim.input["SocialMediaUsage"] = social_media_value
        sim.compute()

    focus = round(_safe_output(focus_sim, "FocusQuality"), 2)
    sleep = round(_safe_output(sleep_sim, "SleepQuality"), 2)
    overload = round(_safe_output(overload_sim, "DigitalOverload"), 2)

    habit = round(
        0.4 * focus + 0.4 * sleep + 0.2 * (10 - overload),
        2
    )

    return {
        "inputs": {
            "ScreenGlances": screen_glances_value,
            "IdleChecking": idle_checking_value,
            "LateNightUse": late_night_use_value,
            "SocialMediaUsage": social_media_value,
        },
        "outputs": {
            "FocusQuality": focus,
            "SleepQuality": sleep,
            "DigitalOverload": overload,
            "HabitBalance": habit,
        },
        "labels": {
            "FocusQuality": _positive_label(focus),
            "SleepQuality": _positive_label(sleep),
            "DigitalOverload": _overload_label(overload),
            "HabitBalance": _positive_label(habit),
        },
        "recommendation": _recommendation(focus, sleep, overload, habit),
    }




