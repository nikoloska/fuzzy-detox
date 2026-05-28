import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# ============================================================
# Universes
# ============================================================

screen_glances_universe = np.arange(0, 151, 1)
idle_checking_universe = np.arange(0, 81, 1)
late_night_use_universe = np.arange(0, 121, 1)
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
idle_checking["high"] = fuzz.trapmf(idle_checking.universe, [40, 58, 80, 85])

# LateNightUse MFs from PDF spec (Bozkurt et al. 2024 — 0/15/30/60 min categories)
late_night_use["low"] = fuzz.trapmf(late_night_use.universe, [0, 0, 15, 30])
late_night_use["medium"] = fuzz.trimf(late_night_use.universe, [15, 30, 60])
late_night_use["high"] = fuzz.trapmf(late_night_use.universe, [31, 60, 120, 120])

social_media["low"] = fuzz.trapmf(social_media.universe, [0, 0, 10, 25])
social_media["medium"] = fuzz.trimf(social_media.universe, [15, 30, 55])
social_media["high"] = fuzz.trapmf(social_media.universe, [40, 70, 100, 100])


# ============================================================
# Output variables
# ============================================================

focus_quality = ctrl.Consequent(score_universe, "FocusQuality")
sleep_quality = ctrl.Consequent(score_universe, "SleepQuality")
digital_overload = ctrl.Consequent(score_universe, "DigitalOverload")

focus_quality.defuzzify_method = "centroid"
sleep_quality.defuzzify_method = "centroid"
digital_overload.defuzzify_method = "centroid"

# ============================================================
# Output membership functions — literature-grounded boundaries
#
# Each output has DISTINCT MF shapes reflecting what the literature
# says about each dimension's sensitivity and distribution.
# Unlike inputs (physical measurements), outputs are on a designed
# 0–10 scale, so boundaries encode domain-specific semantics.
# ============================================================

# ── FocusQuality ─────────────────────────────────────────────
# Reference: Ward et al. (2017) "Brain Drain" — even the mere
# presence of a smartphone reduces available cognitive capacity.
# Newport (2016) "Deep Work" — sustained focus is rare and fragile;
# the "high" zone is deliberately narrow (hard to achieve).
# Mark et al. (2008) — >23 interruptions/day = severe fragmentation.
# Design: "high" zone starts at 8.0 (demanding threshold),
#         "very_low" is standard — any significant impairment is serious.
focus_quality["very_low"]    = fuzz.trapmf(focus_quality.universe, [0,   0,   1.5, 3.0])
focus_quality["low"]         = fuzz.trimf (focus_quality.universe, [2.0, 3.5, 5.0])
focus_quality["medium"]      = fuzz.trimf (focus_quality.universe, [4.0, 5.5, 7.0])
focus_quality["medium_high"] = fuzz.trimf (focus_quality.universe, [5.5, 7.5, 9.0])
focus_quality["high"]        = fuzz.trapmf(focus_quality.universe, [8.0, 9.0, 10,  10])
# Note: gap between medium_high peak (7.5) and high start (8.0) is intentional.
# Ward (2017): truly high focus requires near-total absence of digital fragmentation.

# ── SleepQuality ─────────────────────────────────────────────
# Reference: Combertaldi et al. (2021) — pre-sleep screen use
# reduces slow-wave sleep (SWS) even with short exposure.
# Rasch & Born (2013) — SWS disruption causes next-day cognitive
# and emotional impairment; the degradation is steep.
# Design: "very_low" zone is WIDER ([0,0,2.5,4.5]) than FocusQuality
#         because sleep quality degrades faster with any disruption.
#         "high" zone is NARROWER (starts at 8.5) — truly good sleep
#         requires complete absence of late-night stimulation.
sleep_quality["very_low"]    = fuzz.trapmf(sleep_quality.universe, [0,   0,   2.5, 4.5])
sleep_quality["low"]         = fuzz.trimf (sleep_quality.universe, [3.5, 5.0, 6.5])
sleep_quality["medium"]      = fuzz.trimf (sleep_quality.universe, [5.5, 7.0, 8.0])
sleep_quality["medium_high"] = fuzz.trimf (sleep_quality.universe, [7.0, 8.0, 9.0])
sleep_quality["high"]        = fuzz.trapmf(sleep_quality.universe, [8.5, 9.5, 10,  10])
# Note: "very_low" extends to 4.5 — Combertaldi: even moderate late-night
# use measurably disrupts SWS architecture, making poor sleep common.

# ── DigitalOverload ───────────────────────────────────────────
# Reference: Sweller (1994) Cognitive Load Theory — working memory
# has a hard capacity limit; overload accumulates incrementally.
# Kushlev & Dunn (2015) — notification frequency crosses a stress
# threshold at moderate levels of checking behaviour.
# Design: "very_low" zone is NARROWER ([0,0,1.0,2.5]) than the others
#         because true low-overload is rare in modern phone use.
#         "high" zone starts earlier (7.0) — CLT saturation happens
#         before the extreme end of the scale.
digital_overload["very_low"]    = fuzz.trapmf(digital_overload.universe, [0,   0,   1.0, 2.5])
digital_overload["low"]         = fuzz.trimf (digital_overload.universe, [1.5, 3.0, 4.5])
digital_overload["medium"]      = fuzz.trimf (digital_overload.universe, [3.5, 5.0, 6.5])
digital_overload["medium_high"] = fuzz.trimf (digital_overload.universe, [5.5, 7.0, 8.0])
digital_overload["high"]        = fuzz.trapmf(digital_overload.universe, [7.0, 8.5, 10,  10])
# Note: "very_low" only spans [0,2.5] — Newport (2016): achieving
# truly minimal cognitive load requires deliberate digital minimalism,
# not just moderate use. Most users will be in "low" or "medium" range.


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
    # Very good sleep — all inputs minimal [Combertaldi 2021; Rasch & Born 2013]
    ctrl.Rule(late_night_use["low"] & screen_glances["low"] & idle_checking["low"],
              sleep_quality["high"]),
    ctrl.Rule(late_night_use["low"] & social_media["low"],
              sleep_quality["high"]),

    # Good sleep — mostly low late-night [Brautsch 2023]
    ctrl.Rule(late_night_use["low"] & screen_glances["medium"],
              sleep_quality["medium_high"]),
    ctrl.Rule(late_night_use["low"] & social_media["medium"],
              sleep_quality["medium_high"]),

    # Moderate sleep — mixed inputs [Siebers 2024]
    ctrl.Rule(late_night_use["medium"] & screen_glances["medium"],
              sleep_quality["medium"]),
    ctrl.Rule(late_night_use["medium"] & social_media["medium"],
              sleep_quality["medium"]),
    ctrl.Rule(late_night_use["medium"] & screen_glances["low"],
              sleep_quality["medium"]),

    # Poor sleep — high late night or social media [Combertaldi 2021]
    ctrl.Rule(late_night_use["high"] & social_media["medium"],
              sleep_quality["low"]),
    ctrl.Rule(late_night_use["medium"] & social_media["high"],
              sleep_quality["low"]),
    ctrl.Rule(screen_glances["low"] & late_night_use["high"],
              sleep_quality["low"]),

    # Very poor sleep — high late night + high stimulation [Rasch & Born 2013]
    ctrl.Rule(late_night_use["high"] & social_media["high"],
              sleep_quality["very_low"]),
    ctrl.Rule(late_night_use["high"] & screen_glances["high"],
              sleep_quality["very_low"]),
    ctrl.Rule(late_night_use["high"] & idle_checking["high"],
              sleep_quality["very_low"]),
]

digital_overload_rules = [
    # Very high overload — multiple high inputs simultaneously [Sweller 1994; Kushlev 2015]
    ctrl.Rule(screen_glances["high"] & idle_checking["high"] & late_night_use["high"],
              digital_overload["high"]),
    ctrl.Rule(screen_glances["high"] & social_media["high"],
              digital_overload["high"]),
    ctrl.Rule(idle_checking["high"] & social_media["high"],
              digital_overload["high"]),
    ctrl.Rule(late_night_use["high"] & social_media["high"],
              digital_overload["high"]),

    # High overload — dominant single driver [Mark 2008]
    ctrl.Rule(screen_glances["high"] & idle_checking["high"],
              digital_overload["medium_high"]),
    ctrl.Rule(idle_checking["high"] & late_night_use["high"],
              digital_overload["medium_high"]),
    ctrl.Rule(screen_glances["high"] & late_night_use["medium"],
              digital_overload["medium_high"]),

    # Moderate overload — mixed mid inputs [Kushlev 2015]
    ctrl.Rule(social_media["high"] & screen_glances["low"] & late_night_use["low"],
              digital_overload["medium"]),
    ctrl.Rule(late_night_use["high"] & social_media["low"],
              digital_overload["medium"]),
    ctrl.Rule(screen_glances["high"] & social_media["low"],
              digital_overload["medium"]),
    ctrl.Rule(idle_checking["high"] & social_media["low"],
              digital_overload["medium"]),
    ctrl.Rule(screen_glances["medium"] & social_media["medium"],
              digital_overload["medium"]),
    ctrl.Rule(screen_glances["low"] & social_media["high"],
              digital_overload["medium"]),

    # Low overload — mostly low inputs [Newport 2016]
    ctrl.Rule(screen_glances["medium"] & social_media["low"] & late_night_use["low"],
              digital_overload["low"]),
    ctrl.Rule(idle_checking["medium"] & screen_glances["low"],
              digital_overload["low"]),

    # Very low overload — all inputs minimal [Newport 2016; Ward 2017]
    ctrl.Rule(screen_glances["low"] & social_media["low"],
              digital_overload["very_low"]),
    ctrl.Rule(screen_glances["low"] & idle_checking["low"] & late_night_use["low"],
              digital_overload["very_low"]),
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

# 5 terms — same structure as FocusQuality, SleepQuality, DigitalOverload
# Consistent with Maximum Membership Principle across all outputs (Zadeh, 1965)
habit_balance_out["very_low"]   = fuzz.trapmf(habit_balance_out.universe, [0,   0,   1.5, 3.0])
habit_balance_out["low"]        = fuzz.trimf (habit_balance_out.universe, [2.0, 3.5, 5.0])
habit_balance_out["medium"]     = fuzz.trimf (habit_balance_out.universe, [4.0, 5.5, 7.0])
habit_balance_out["medium_high"]= fuzz.trimf (habit_balance_out.universe, [5.5, 7.0, 8.5])
habit_balance_out["high"]       = fuzz.trapmf(habit_balance_out.universe, [7.0, 8.5, 10,  10])

# --- Rule base for 4th FIS ---
# Covers the 27 logical combinations systematically.
# Principle: focus and sleep drive balance up; overload drives it down.
habit_rules = [
    # === Best case: high focus + high sleep ===
    ctrl.Rule(fq_in["high"]   & sq_in["high"]   & do_in["low"],    habit_balance_out["high"]),
    ctrl.Rule(fq_in["high"]   & sq_in["high"]   & do_in["medium"], habit_balance_out["medium_high"]),
    ctrl.Rule(fq_in["high"]   & sq_in["high"]   & do_in["high"],   habit_balance_out["medium"]),

    # === High focus + medium sleep ===
    ctrl.Rule(fq_in["high"]   & sq_in["medium"] & do_in["low"],    habit_balance_out["medium_high"]),
    ctrl.Rule(fq_in["high"]   & sq_in["medium"] & do_in["medium"], habit_balance_out["medium"]),
    ctrl.Rule(fq_in["high"]   & sq_in["medium"] & do_in["high"],   habit_balance_out["low"]),

    # === High focus + low sleep ===
    ctrl.Rule(fq_in["high"]   & sq_in["low"]    & do_in["low"],    habit_balance_out["medium"]),
    ctrl.Rule(fq_in["high"]   & sq_in["low"]    & do_in["medium"], habit_balance_out["low"]),
    ctrl.Rule(fq_in["high"]   & sq_in["low"]    & do_in["high"],   habit_balance_out["very_low"]),

    # === Medium focus + high sleep ===
    ctrl.Rule(fq_in["medium"] & sq_in["high"]   & do_in["low"],    habit_balance_out["medium_high"]),
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


def _label_from_mf(score: float, antecedent_or_consequent) -> str:
    """
    Derive the linguistic label for a crisp score using the Maximum
    Membership Principle: the label whose MF has the highest degree
    of membership at `score` is returned.

    This ensures labels are always consistent with the actual MF
    definitions — no hardcoded thresholds that could drift out of
    sync with the fuzzy sets.

    Reference: Zadeh (1965) — linguistic variables and fuzzy sets.
    """
    best_label = "Medium"
    best_degree = -1.0
    for term_name, term in antecedent_or_consequent.terms.items():
        degree = float(fuzz.interp_membership(
            antecedent_or_consequent.universe,
            term.mf,
            score
        ))
        if degree > best_degree:
            best_degree = degree
            best_label = term_name
    # Capitalise for display ("very_high" → "Very High")
    return best_label.replace("_", " ").title()


def _positive_label(score: float) -> str:
    """Label for FocusQuality  outputs (MF-derived)."""
    return _label_from_mf(score, focus_quality)

def _sleep_label(score: float) -> str:
    """Label for  SleepQuality outputs (MF-derived)."""
    return _label_from_mf(score, sleep_quality)

def _overload_label(score: float) -> str:
    """Label for DigitalOverload output (MF-derived)."""
    return _label_from_mf(score, digital_overload)


def _habit_label(score: float) -> str:
    """Label for HabitBalance output (MF-derived, 5 terms)."""
    return _label_from_mf(score, habit_balance_out)

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


def _mu(var, term: str, value: float) -> float:
    """
    Compute the degree of membership of `value` in `var[term]`.
    Uses skfuzzy's interp_membership for exact MF evaluation.

    This replaces numeric thresholds with MF-derived degrees,
    keeping the recommendation layer fully fuzzy-consistent.
    Reference: Zadeh (1965) — membership function evaluation.

    A degree > 0.5 means `value` is more `term` than not.
    A degree > 0.1 means `term` has meaningful activation.
    """
    return float(fuzz.interp_membership(
        var.universe, var[term].mf, value
    ))


def _literature_recommendations(
        screen_glances: float,
        idle_checking: float,
        late_night_use: float,
        social_media: float,
        focus: float,
        sleep: float,
        overload: float,
        habit: float,
        lbl_focus: str,
        lbl_sleep: str,
        lbl_overload: str,
        lbl_habit: str,
) -> list:

    recommendations = []

    # Fuzzy membership degrees for raw inputs
    # Import module-level Antecedent variables explicitly to avoid
    # name collision with the float parameters of this function.
    import fuzzy_engine as _eng
    mu_ln_high   = _mu(_eng.late_night_use,  "high",   late_night_use)
    mu_ln_medium = _mu(_eng.late_night_use,  "medium", late_night_use)
    mu_sg_high   = _mu(_eng.screen_glances,  "high",   screen_glances)
    mu_sg_medium = _mu(_eng.screen_glances,  "medium", screen_glances)
    mu_ic_high   = _mu(_eng.idle_checking,   "high",   idle_checking)
    mu_sm_high   = _mu(_eng.social_media,    "high",   social_media)
    mu_sm_medium = _mu(_eng.social_media,    "medium", social_media)

    # Output condition helpers (from MF-derived labels — no numbers)
    sleep_poor    = lbl_sleep    in {"Very Low", "Low"}
    sleep_medium  = lbl_sleep    == "Medium"
    focus_poor    = lbl_focus    in {"Very Low", "Low"}
    focus_medium  = lbl_focus    == "Medium"
    overload_high = lbl_overload in {"High", "Medium High"}
    habit_poor    = lbl_habit    in {"Very Low", "Low"}
    habit_medium  = lbl_habit    == "Medium"
    habit_good    = lbl_habit    in {"High", "Medium High"}

    # ── RECOMMENDATIONS ──

    # Source: Exelmans & Van den Bulck (2016); Digital Wellness Institute (2024); Atomic Habits
    if mu_ln_high > 0.3 or sleep_poor:
        reason = (f"Late Night Use activating 'high' (μ={mu_ln_high:.2f})"
                  if mu_ln_high > 0.3
                  else f"Sleep Quality is '{lbl_sleep}'")
        _add_recommendation(
            recommendations,
            rec_id="late_night_sleep_boundary",
            priority=1,
            source="Exelmans & Van den Bulck; Digital Wellness Institute; Atomic Habits",
            trigger=f"{reason} — bedtime boundaries recommended.",
            principle="Reduce bedtime screen exposure through environment design.",
            action="Charge your phone outside the bedroom and stop screens 30 minutes earlier.",
            insight="Your sleep score is strongly shaped by evening phone boundaries."
        )

    # Source: Newport (2021) Digital Minimalism; Digital Wellness Institute (2024)
    if mu_ln_medium > 0.4 and mu_sm_high > 0.3:
        _add_recommendation(
            recommendations,
            rec_id="late_night_social_replacement",
            priority=2,
            source="Digital Minimalism; Digital Wellness Institute",
            trigger=f"Late Night Use is in medium zone (μ={mu_ln_medium:.2f}) and Social Media is high (μ={mu_sm_high:.2f}).",
            principle="Replace low-value late-night scrolling with intentional offline recovery.",
            action="Replace late-night social scrolling with one planned offline wind-down activity.",
            insight="Late social media combines stimulation, habit, and poor timing."
        )

    # Source: Ward et al. (2017); Mark et al. (2008)
    if mu_sg_high > 0.3 or focus_poor:
        _add_recommendation(
            recommendations,
            rec_id="screen_glance_focus_boundary",
            priority=3,
            source="Ward et al.; Mark et al.",
            trigger=f"Screen Glances activating 'high' (μ={mu_sg_high:.2f}) and Focus Quality is '{lbl_focus}'.",
            principle="Reduce fragmented attention by setting physical phone boundaries.",
            action="Keep your phone face-down or in a drawer during focused work blocks.",
            insight="Mere phone presence reduces cognitive capacity even without use."
        )

    # Source: Kushlev & Dunn (2015)
    if mu_sg_high > 0.3 and mu_ic_high > 0.3:
        _add_recommendation(
            recommendations,
            rec_id="idle_checking_batch",
            priority=4,
            source="Kushlev & Dunn",
            trigger=f"Screen Glances (μ_high={mu_sg_high:.2f}) and Idle Checking (μ_high={mu_ic_high:.2f}) both elevated.",
            principle="Batch phone checks to reduce the stress of constant notifications.",
            action="Check your phone only at scheduled times — e.g. every 90 minutes.",
            insight="Batching checks cuts the hidden stress of perpetual availability."
        )

    # Source: Sweller (1994) CLT; Kushlev & Dunn (2015)
    if mu_ic_high > 0.5:
        _add_recommendation(
            recommendations,
            rec_id="idle_checking_notification_audit",
            priority=5,
            source="Cognitive Load Theory; Kushlev & Dunn",
            trigger=f"Idle Checking is predominantly 'high' (μ={mu_ic_high:.2f}).",
            principle="Reduce cognitive load by removing low-value notification sources.",
            action="Turn off notifications for the three least-important apps on your phone.",
            insight="Each notification creates a micro-interruption that fragments thinking."
        )

    # Source: Twenge & Campbell (2018); Przybylski & Weinstein (2017)
    if mu_sm_high > 0.5:
        _add_recommendation(
            recommendations,
            rec_id="social_media_goldilocks",
            priority=6,
            source="Twenge & Campbell; Przybylski & Weinstein",
            trigger=f"Social Media Usage is predominantly 'high' (μ={mu_sm_high:.2f}).",
            principle="Apply the Goldilocks principle — moderate social media use is neutral; high use is harmful.",
            action="Set a daily time limit for your most-used social app.",
            insight="Moderate use has neutral wellbeing effects; high use consistently lowers wellbeing."
        )

    # Source: Twenge & Campbell (2018)
    if mu_sm_medium > 0.5 and mu_sm_high < 0.3:
        _add_recommendation(
            recommendations,
            rec_id="social_media_intentional_use",
            priority=7,
            source="Twenge & Campbell",
            trigger=f"Social Media Usage is in medium zone (μ={mu_sm_medium:.2f}).",
            principle="Keep social media use at a moderate, intentional level.",
            action="Use social media only for a specific purpose — not as default boredom relief.",
            insight="Passive scrolling drives most of the negative wellbeing effect."
        )

    # Source: Newport (2016) Deep Work; Ward et al. (2017)
    if overload_high and focus_poor:
        _add_recommendation(
            recommendations,
            rec_id="overload_focus_protection",
            priority=8,
            source="Deep Work; Ward et al.",
            trigger=f"Digital Overload is '{lbl_overload}' and Focus Quality is '{lbl_focus}'.",
            principle="Protect deep focus periods from digital overload.",
            action="Schedule one 90-minute phone-free block per day for deep work.",
            insight="Deep work requires zero digital interruption — even standby reduces capacity."
        )

    # Source: Sweller (1994); Kushlev & Dunn (2015)
    if overload_high and mu_ic_high > 0.3:
        _add_recommendation(
            recommendations,
            rec_id="overload_notification_reduction",
            priority=9,
            source="Cognitive Load Theory; Kushlev & Dunn",
            trigger=f"Digital Overload is '{lbl_overload}' and Idle Checking elevated (μ={mu_ic_high:.2f}).",
            principle="Reducing passive checking directly lowers cognitive overload.",
            action="Enable Do Not Disturb for 2-hour blocks during your peak focus hours.",
            insight="High overload often needs friction, not just motivation."
        )

    # Source: Rasch & Born (2013); Combertaldi et al. (2021)
    if sleep_poor and mu_sg_medium > 0.3:
        _add_recommendation(
            recommendations,
            rec_id="sleep_glance_pattern",
            priority=10,
            source="Rasch & Born; Combertaldi et al.",
            trigger=f"Sleep Quality is '{lbl_sleep}' and moderate glance pattern (μ={mu_sg_medium:.2f}).",
            principle="Reduce stimulation in the 90 minutes before sleep.",
            action="Switch your phone to grayscale mode after 21:00 to reduce stimulation.",
            insight="Screen light and content stimulation both delay sleep onset."
        )

    # Source: Newport (2021) Digital Minimalism
    if focus_medium and mu_sg_medium > 0.4:
        _add_recommendation(
            recommendations,
            rec_id="focus_improvement_batching",
            priority=11,
            source="Digital Minimalism",
            trigger=f"Focus Quality is '{lbl_focus}' and Screen Glances moderate (μ={mu_sg_medium:.2f}).",
            principle="Small reductions in glances improve focus quality significantly.",
            action="Reduce screen glances by 20% by leaving your phone in another room during work.",
            insight="Phone proximity alone reduces available cognitive resources."
        )

    # Source: Fogg (2019) Tiny Habits
    if mu_ln_medium > 0.5 and mu_ln_high < 0.3:
        _add_recommendation(
            recommendations,
            rec_id="late_night_gradual_reduction",
            priority=12,
            source="Tiny Habits",
            trigger=f"Late Night Use is in medium zone (μ={mu_ln_medium:.2f}).",
            principle="Use a small reduction instead of a strict ban.",
            action="Reduce late-night use by ten minutes for the next seven evenings.",
            insight="Small reductions are easier to repeat than sudden digital curfews."
        )

    # Source: Newport (2021) Digital Minimalism; Digital Wellness Institute (2024)
    if habit_poor and overload_high:
        _add_recommendation(
            recommendations,
            rec_id="offline_replacement_activity",
            priority=13,
            source="Digital Minimalism; Digital Wellness Institute",
            trigger=f"Habit Balance is '{lbl_habit}' and Digital Overload is '{lbl_overload}'.",
            principle="Replace digital stimulation with a meaningful offline activity.",
            action="Swap one scrolling session for reading, walking, or a screen-free hobby.",
            insight="Replacement works better than empty restriction because it fills the habit gap."
        )

    # Source: Clear (2018) Atomic Habits
    if habit_good:
        _add_recommendation(
            recommendations,
            rec_id="balanced_pattern_protective_routine",
            priority=14,
            source="Atomic Habits",
            trigger=f"Habit Balance is '{lbl_habit}' — a healthy digital pattern.",
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
    late_night_use_value = _clamp(late_night_use_value, 0, 120)
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

    focus_lbl   = _positive_label(focus)
    sleep_lbl   = _sleep_label(sleep)
    overload_lbl= _overload_label(overload)
    habit_lbl   = _habit_label(habit)

    recommendations = _literature_recommendations(
        screen_glances=screen_glances_value,
        idle_checking=idle_checking_value,
        late_night_use=late_night_use_value,
        social_media=social_media_value,
        focus=focus,
        sleep=sleep,
        overload=overload,
        habit=habit,
        lbl_focus=focus_lbl,
        lbl_sleep=sleep_lbl,
        lbl_overload=overload_lbl,
        lbl_habit=habit_lbl,
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
            "FocusQuality":    focus_lbl,
            "SleepQuality":    sleep_lbl,
            "DigitalOverload": overload_lbl,
            "HabitBalance":    habit_lbl,
        },
        "recommendation": _recommendation(recommendations),
        "recommendations": recommendations,
    }