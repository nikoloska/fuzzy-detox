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

# ------------------------------------------------------------
# IMPROVEMENT — Adjust LateNightUse "high" membership function
# ------------------------------------------------------------
late_night_use["low"] = fuzz.trapmf(late_night_use.universe, [0, 0, 10, 25])
late_night_use["medium"] = fuzz.trimf(late_night_use.universe, [15, 55, 95])
late_night_use["high"] = fuzz.trapmf(late_night_use.universe, [80, 105, 180, 180])

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
# Rule base
# ============================================================

focus_rules = [
    # Strong negative focus patterns
    ctrl.Rule(screen_glances["high"], focus_quality["low"]),
    ctrl.Rule(late_night_use["high"], focus_quality["low"]),
    ctrl.Rule(social_media["high"], focus_quality["low"]),

    # ------------------------------------------------------------
    # IMPROVEMENT — Separate IdleChecking weight / soften standalone rule
    # ------------------------------------------------------------
    ctrl.Rule(idle_checking["high"], focus_quality["low"]),                        # standalone: low
    ctrl.Rule(idle_checking["high"] & screen_glances["high"], focus_quality["very_low"]),  # combined: very_low

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

    # ------------------------------------------------------------
    # IMPROVEMENT — Tighten rule base: social media high but other inputs moderate/low
    # ------------------------------------------------------------
    # New rule: SocialMedia alone high but glances & late-night low → Medium (not High)
    ctrl.Rule(
        social_media["high"] & screen_glances["low"] & late_night_use["low"],
        digital_overload["medium"]
    ),

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
# 4th FIS — HabitBalance (Hierarchical Mamdani)
# Inputs: FocusQuality, SleepQuality, DigitalOverload (0–10 each)
# Output: HabitBalance (0–10)
#
# Design rationale:
# The three subsystems capture behavioural nuances fuzzy. Their
# defuzzified outputs are re-injected as inputs into a 4th FIS so
# that the final HabitBalance score is also produced by Mamdani
# inference — not by a crisp weighted formula. This hierarchical
# structure is a recognised fuzzy system design pattern that
# preserves fuzziness end-to-end (Mendel, 2001; Zadeh, 1975).
# ============================================================

intermediate_universe = np.arange(0, 10.1, 0.1)

# --- Intermediate input variables ---
fq_in = ctrl.Antecedent(intermediate_universe, "FocusQuality_in")
sq_in = ctrl.Antecedent(intermediate_universe, "SleepQuality_in")
do_in = ctrl.Antecedent(intermediate_universe, "DigitalOverload_in")

for antecedent in [fq_in, sq_in]:
    antecedent["low"]    = fuzz.trapmf(antecedent.universe, [0,   0,   2.5, 4.5])
    antecedent["medium"] = fuzz.trimf (antecedent.universe, [3.0, 5.0, 7.5])
    antecedent["high"]   = fuzz.trapmf(antecedent.universe, [6.0, 8.0, 10,  10])

# DigitalOverload: same shape — but semantically inverted in the rules
# (high overload → bad habit balance)
do_in["low"]    = fuzz.trapmf(do_in.universe, [0,   0,   2.5, 4.5])
do_in["medium"] = fuzz.trimf (do_in.universe, [3.0, 5.0, 7.5])
do_in["high"]   = fuzz.trapmf(do_in.universe, [6.0, 8.0, 10,  10])

# --- Output variable ---
habit_balance_out = ctrl.Consequent(intermediate_universe, "HabitBalance")
habit_balance_out.defuzzify_method = "centroid"

habit_balance_out["very_low"] = fuzz.trapmf(habit_balance_out.universe, [0,   0,   1.5, 3.0])
habit_balance_out["low"]      = fuzz.trimf (habit_balance_out.universe, [2.0, 3.5, 5.0])
habit_balance_out["medium"]   = fuzz.trimf (habit_balance_out.universe, [4.0, 5.5, 7.0])
habit_balance_out["high"]     = fuzz.trimf (habit_balance_out.universe, [6.0, 7.5, 9.0])
habit_balance_out["very_high"]= fuzz.trapmf(habit_balance_out.universe, [8.0, 9.0, 10,  10])

# --- Rule base for 4th FIS ---
# Covers the 27 logical combinations systematically.
# Principle: focus and sleep drive balance up; overload drives it down.
habit_rules = [
    # === Best case: high focus + high sleep ===
    ctrl.Rule(fq_in["high"]   & sq_in["high"]   & do_in["low"],    habit_balance_out["very_high"]),
    ctrl.Rule(fq_in["high"]   & sq_in["high"]   & do_in["medium"], habit_balance_out["high"]),
    ctrl.Rule(fq_in["high"]   & sq_in["high"]   & do_in["high"],   habit_balance_out["medium"]),

    # === High focus + medium sleep ===
    ctrl.Rule(fq_in["high"]   & sq_in["medium"] & do_in["low"],    habit_balance_out["high"]),
    ctrl.Rule(fq_in["high"]   & sq_in["medium"] & do_in["medium"], habit_balance_out["medium"]),
    ctrl.Rule(fq_in["high"]   & sq_in["medium"] & do_in["high"],   habit_balance_out["low"]),

    # === High focus + low sleep ===
    ctrl.Rule(fq_in["high"]   & sq_in["low"]    & do_in["low"],    habit_balance_out["medium"]),
    ctrl.Rule(fq_in["high"]   & sq_in["low"]    & do_in["medium"], habit_balance_out["low"]),
    ctrl.Rule(fq_in["high"]   & sq_in["low"]    & do_in["high"],   habit_balance_out["very_low"]),

    # === Medium focus + high sleep ===
    ctrl.Rule(fq_in["medium"] & sq_in["high"]   & do_in["low"],    habit_balance_out["high"]),
    ctrl.Rule(fq_in["medium"] & sq_in["high"]   & do_in["medium"], habit_balance_out["medium"]),
    ctrl.Rule(fq_in["medium"] & sq_in["high"]   & do_in["high"],   habit_balance_out["low"]),

    # === Medium focus + medium sleep ===
    ctrl.Rule(fq_in["medium"] & sq_in["medium"] & do_in["low"],    habit_balance_out["medium"]),
    ctrl.Rule(fq_in["medium"] & sq_in["medium"] & do_in["medium"], habit_balance_out["medium"]),
    ctrl.Rule(fq_in["medium"] & sq_in["medium"] & do_in["high"],   habit_balance_out["low"]),

    # === Medium focus + low sleep ===
    ctrl.Rule(fq_in["medium"] & sq_in["low"]    & do_in["low"],    habit_balance_out["low"]),
    ctrl.Rule(fq_in["medium"] & sq_in["low"]    & do_in["medium"], habit_balance_out["low"]),
    ctrl.Rule(fq_in["medium"] & sq_in["low"]    & do_in["high"],   habit_balance_out["very_low"]),

    # === Low focus + high sleep ===
    ctrl.Rule(fq_in["low"]    & sq_in["high"]   & do_in["low"],    habit_balance_out["medium"]),
    ctrl.Rule(fq_in["low"]    & sq_in["high"]   & do_in["medium"], habit_balance_out["low"]),
    ctrl.Rule(fq_in["low"]    & sq_in["high"]   & do_in["high"],   habit_balance_out["very_low"]),

    # === Low focus + medium sleep ===
    ctrl.Rule(fq_in["low"]    & sq_in["medium"] & do_in["low"],    habit_balance_out["low"]),
    ctrl.Rule(fq_in["low"]    & sq_in["medium"] & do_in["medium"], habit_balance_out["low"]),
    ctrl.Rule(fq_in["low"]    & sq_in["medium"] & do_in["high"],   habit_balance_out["very_low"]),

    # === Worst case: low focus + low sleep ===
    ctrl.Rule(fq_in["low"]    & sq_in["low"]    & do_in["low"],    habit_balance_out["low"]),
    ctrl.Rule(fq_in["low"]    & sq_in["low"]    & do_in["medium"], habit_balance_out["very_low"]),
    ctrl.Rule(fq_in["low"]    & sq_in["low"]    & do_in["high"],   habit_balance_out["very_low"]),
]

habit_system = ctrl.ControlSystem(habit_rules)


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

def _habit_balance_label(score: float) -> str:
    if score < 3.0:
        return "Very Low"
    if score < 5.0:
        return "Low"
    if score < 7.0:
        return "Medium"
    if score < 8.5:
        return "High"
    return "Very High"

def _add_recommendation(
        recommendations: list,
        rec_id: str,
        priority: int,
        source: str,
        trigger: str,
        principle: str,
        action: str,
        insight: str,
) -> None:
    """Adds one recommendation if it was not already added."""
    if any(rec["id"] == rec_id for rec in recommendations):
        return

    recommendations.append({
        "id": rec_id,
        "priority": priority,
        "source": source,
        "trigger": trigger,
        "principle": principle,
        "action": action,
        "insight": insight,
    })


def _literature_recommendations(
        screen_glances: float,
        idle_checking: float,
        late_night_use: float,
        social_media: float,
        focus: float,
        sleep: float,
        overload: float,
        habit: float,
) -> list:
    """
    Literature-informed recommendation mapping.

    The fuzzy system remains the decision engine.
    This layer maps fuzzy outputs and raw inputs to practical behavioral principles.

    """

    recommendations = []

    # Source: Exelmans, Liese & Van den Bulck, Jan, 2016. "Bedtime mobile phone use and sleep in adults,"
    # Social Science & Medicine, Elsevier, vol. 148(C), pages 93-101.)
    # and
    # Digital Wellness Institute (2024), "Healthy Tech Habits":
    # no screens 30-60 minutes before bed; charge phone outside bedroom.
    # Also aligned with James Clear, Atomic Habits: environment design.
    if late_night_use >= 80 or sleep < 4.5:
        _add_recommendation(
            recommendations,
            rec_id="late_night_sleep_boundary",
            priority=1,
            source="Exelmans & Van den Bulck; Digital Wellness Institute; Atomic Habits",
            trigger=f"Late Night Use is {late_night_use:.0f} minutes and Sleep Quality is {sleep:.2f}/10.",
            principle="Reduce bedtime screen exposure through environment design.",
            action="Charge your phone outside the bedroom and stop screens 30 minutes earlier.",
            insight="Your sleep score is strongly shaped by evening phone boundaries."
        )

    # Source: Cal Newport, Digital Minimalism:
    # remove low-value optional digital use and replace it with meaningful offline activity.
    # Digital Wellness Institute (2024): replace social media time with meaningful activities.
    if late_night_use >= 60 and social_media >= 55:
        _add_recommendation(
            recommendations,
            rec_id="late_night_social_replacement",
            priority=2,
            source="Digital Minimalism; Digital Wellness Institute",
            trigger=f"Late Night Use is {late_night_use:.0f} minutes and Social Media Usage is {social_media:.0f}%.",
            principle="Replace low-value late-night scrolling with intentional offline recovery.",
            action="Replace late-night social scrolling with one planned offline wind-down activity.",
            insight="Late social media combines stimulation, habit, and poor timing."
        )

    # Source: Cal Newport, Deep Work:
    # protect focused work from attention fragmentation.
    # Nir Eyal, Indistractable: schedule intentional checking instead of reactive checking.
    if screen_glances >= 65 or focus < 4.5:
        _add_recommendation(
            recommendations,
            rec_id="screen_glance_checking_windows",
            priority=3,
            source="Deep Work; Indistractable",
            trigger=f"Screen Glances are {screen_glances:.0f} per day and Focus Quality is {focus:.2f}/10.",
            principle="Reduce attention fragmentation with planned phone-checking windows.",
            action="Use three fixed phone-check windows to protect focus from repeated unlocks.",
            insight="Frequent glances can fragment attention even when total screen time feels normal."
        )

    # Source: Cal Newport, Deep Work and Digital Wellness Institute (2024):
    # turn off notifications and practice one-tasking to reduce interruptions.
    if screen_glances >= 65 and idle_checking >= 40:
        _add_recommendation(
            recommendations,
            rec_id="notifications_and_idle_checking",
            priority=4,
            source="Deep Work; Digital Wellness Institute",
            trigger=f"Screen Glances are {screen_glances:.0f} and Idle Checking is {idle_checking:.0f}.",
            principle="Reduce external triggers and repeated checking loops.",
            action="Turn off non-essential notifications and check messages only during planned windows.",
            insight="Your issue is not only usage, but repeated attention switching."
        )

    # Source: BJ Fogg, Tiny Habits and James Clear, Atomic Habits:
    # make the replacement behavior very small and easy to repeat.
    if idle_checking >= 40:
        _add_recommendation(
            recommendations,
            rec_id="idle_checking_tiny_replacement",
            priority=5,
            source="Tiny Habits; Atomic Habits",
            trigger=f"Idle Checking is {idle_checking:.0f} short checks per day.",
            principle="Replace automatic checking with a tiny alternative behavior.",
            action="When you reach for the phone, take one breath before unlocking.",
            insight="A tiny pause makes automatic checking visible before it becomes scrolling."
        )

    # Source: Cal Newport, Digital Minimalism:
    # take a temporary break from optional technologies to clarify their value.
    # Digital Wellness Institute (2024): a week-long social media fast can reset habits.
    if social_media >= 75:
        _add_recommendation(
            recommendations,
            rec_id="social_media_fast",
            priority=6,
            source="Digital Minimalism; Digital Wellness Institute",
            trigger=f"Social Media Usage is {social_media:.0f}% of total screen time.",
            principle="Use a short social media fast to reset optional digital habits.",
            action="Try a seven-day social media fast and remove the apps temporarily.",
            insight="Removing access works better than relying on willpower alone."
        )

    # Source: Cal Newport, Digital Minimalism:
    # use technology intentionally, not automatically.
    # Digital Wellness Institute (2024): set app time limits and use timers.
    if social_media >= 55:
        _add_recommendation(
            recommendations,
            rec_id="intentional_social_media_slot",
            priority=7,
            source="Digital Minimalism; Digital Wellness Institute",
            trigger=f"Social Media Usage is {social_media:.0f}% of total screen time.",
            principle="Shift social media from automatic use to intentional sessions.",
            action="Set one daily social media slot and close the app when it ends.",
            insight="A defined slot turns social media from background noise into a choice."
        )

    # Source: Digital Wellness Institute (2024):
    # app blockers can blacklist distracting apps during specific times.
    # Nir Eyal, Indistractable: reduce external triggers before distraction happens.
    if overload >= 7.0:
        _add_recommendation(
            recommendations,
            rec_id="high_overload_app_blocker",
            priority=8,
            source="Digital Wellness Institute; Indistractable",
            trigger=f"Digital Overload is {overload:.2f}/10.",
            principle="Use friction to prevent high-overload digital patterns.",
            action="Block distracting apps during focus time and after your planned evening cutoff.",
            insight="High overload often needs friction, not just motivation."
        )

    # Source: Digital Wellness Institute (2024):
    # turn off notifications and set do-not-disturb times.
    # James Clear, Atomic Habits: make good behavior easier by changing the environment.
    if overload >= 6.5 and idle_checking >= 30:
        _add_recommendation(
            recommendations,
            rec_id="do_not_disturb_boundary",
            priority=9,
            source="Digital Wellness Institute; Atomic Habits",
            trigger=f"Digital Overload is {overload:.2f}/10 and Idle Checking is {idle_checking:.0f}.",
            principle="Create a low-friction boundary against repeated interruptions.",
            action="Enable do-not-disturb during meals, workouts, and your first work hour.",
            insight="Boundaries work best when they are automatic, visible, and repeated."
        )

    # Source: Digital Wellness Institute (2024):
    # practice one-tasking and avoid toggling between tasks.
    # Cal Newport, Deep Work: preserve uninterrupted attention.
    if focus < 5.5 and screen_glances >= 40 and screen_glances < 65:
        _add_recommendation(
            recommendations,
            rec_id="medium_glance_one_tasking",
            priority=10,
            source="Digital Wellness Institute; Deep Work",
            trigger=f"Screen Glances are {screen_glances:.0f} and Focus Quality is {focus:.2f}/10.",
            principle="Protect moderate focus by reducing task switching.",
            action="Choose one screen task at a time and finish before switching.",
            insight="Moderate checking can still weaken focus when it creates task-hopping."
        )

    # Source: Digital Wellness Institute (2024):
    # avoid passive scrolling and choose activities that add value.
    # Cal Newport, Digital Minimalism: prioritize high-value technology use.
    if social_media >= 55 and screen_glances <= 40 and late_night_use <= 25:
        _add_recommendation(
            recommendations,
            rec_id="high_social_but_controlled_timing",
            priority=11,
            source="Digital Minimalism; Digital Wellness Institute",
            trigger=f"Social Media Usage is {social_media:.0f}%, but glances and late-night use are low.",
            principle="Keep social media intentional when timing and checking are already controlled.",
            action="Keep social media to one intentional session, not scattered passive scrolling.",
            insight="Your timing is controlled; the next improvement is content quality."
        )

    # Source: James Clear, Atomic Habits:
    # use visual cues and environment design to interrupt unwanted habits.
    if screen_glances >= 100:
        _add_recommendation(
            recommendations,
            rec_id="very_high_glance_phone_parking",
            priority=12,
            source="Atomic Habits",
            trigger=f"Screen Glances are very high at {screen_glances:.0f} per day.",
            principle="Make the unwanted habit harder by changing phone placement.",
            action="Park your phone away from your desk during one focused work block.",
            insight="Distance adds friction, and friction weakens automatic checking loops."
        )

    # Source: BJ Fogg, Tiny Habits:
    # reduce behavior in very small, realistic steps.
    if 25 < late_night_use < 80:
        _add_recommendation(
            recommendations,
            rec_id="medium_late_night_gradual_reduction",
            priority=13,
            source="Tiny Habits",
            trigger=f"Late Night Use is moderate at {late_night_use:.0f} minutes.",
            principle="Use a small reduction instead of a strict ban.",
            action="Reduce late-night use by ten minutes for the next seven evenings.",
            insight="Small reductions are easier to repeat than sudden digital curfews."
        )

    # Source: Cal Newport, Digital Minimalism:
    # replace low-value online time with meaningful offline activity.
    # Digital Wellness Institute (2024): reading, exercising, nature, and screen-free activities.
    if habit < 6.5 and overload >= 5.0:
        _add_recommendation(
            recommendations,
            rec_id="offline_replacement_activity",
            priority=14,
            source="Digital Minimalism; Digital Wellness Institute",
            trigger=f"Habit Balance is {habit:.2f}/10 and Digital Overload is {overload:.2f}/10.",
            principle="Replace digital stimulation with a meaningful offline activity.",
            action="Swap one scrolling session for reading, walking, or a screen-free hobby.",
            insight="Replacement works better than empty restriction because it fills the habit gap."
        )

    # Source: James Clear, Atomic Habits:
    # preserve good systems and repeat small protective routines.
    if habit >= 7.0:
        _add_recommendation(
            recommendations,
            rec_id="balanced_pattern_protective_routine",
            priority=15,
            source="Atomic Habits",
            trigger=f"Habit Balance is strong at {habit:.2f}/10.",
            principle="Maintain the current habit system with one small protective routine.",
            action="Keep one daily phone-free moment to protect your current balance.",
            insight="Balanced habits still need small boundaries to stay stable."
        )

    # Fallback 1
    # Source: Digital Wellness Institute (2024): tech-free times and zones.
    if len(recommendations) < 3:
        _add_recommendation(
            recommendations,
            rec_id="fallback_tech_free_moment",
            priority=90,
            source="Digital Wellness Institute",
            trigger="General digital wellness support.",
            principle="Add one simple tech-free moment to the day.",
            action="Keep one daily meal or walk completely phone-free this week.",
            insight="Small tech-free moments make digital boundaries easier to notice."
        )

    # Fallback 2
    # Source: Digital Wellness Institute (2024): turn off notifications and check apps intentionally.
    if len(recommendations) < 3:
        _add_recommendation(
            recommendations,
            rec_id="fallback_notification_check",
            priority=91,
            source="Digital Wellness Institute",
            trigger="General focus support.",
            principle="Reduce interruptions by making notification checking intentional.",
            action="Mute one distracting app and check it only at a chosen time.",
            insight="One muted app can reduce many tiny interruptions."
        )

    # Fallback 3
    # Source: James Clear, Atomic Habits:
    # make the desired behavior obvious through a visible cue.
    if len(recommendations) < 3:
        _add_recommendation(
            recommendations,
            rec_id="fallback_visible_boundary",
            priority=92,
            source="Atomic Habits",
            trigger="General habit stability.",
            principle="Use a visible cue to support the desired habit.",
            action="Place a small reminder where you usually unlock your phone.",
            insight="Visible cues help interrupt automatic behavior before it runs."
        )

    return sorted(recommendations, key=lambda rec: rec["priority"])[:3]

def _recommendation(recommendations: list) -> str:
    if not recommendations:
        return "Your digital rhythm looks moderate. Small habit changes could improve balance."

    return recommendations[0]["action"]

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

    # ── 4th Mamdani FIS: HabitBalance ──────────────────────────────
    # The three intermediate crisp values are re-injected as inputs
    # into a dedicated FIS, keeping the full inference chain fuzzy.
    habit_sim = ctrl.ControlSystemSimulation(habit_system)
    habit_sim.input["FocusQuality_in"]    = _clamp(focus,   0, 10)
    habit_sim.input["SleepQuality_in"]    = _clamp(sleep,   0, 10)
    habit_sim.input["DigitalOverload_in"] = _clamp(overload, 0, 10)
    habit_sim.compute()
    habit = round(_safe_output(habit_sim, "HabitBalance"), 2)

    recommendations = _literature_recommendations(
        screen_glances=screen_glances_value,
        idle_checking=idle_checking_value,
        late_night_use=late_night_use_value,
        social_media=social_media_value,
        focus=focus,
        sleep=sleep,
        overload=overload,
        habit=habit,
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
            "HabitBalance": _habit_balance_label(habit),
        },
        "recommendation": _recommendation(recommendations),
        "recommendations": recommendations,
    }