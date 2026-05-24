"""
mf_viz.py — Membership Function Visualisation for fuzzy-detox
Generates matplotlib figures showing MFs + current input/output values.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import skfuzzy as fuzz

# ── palette (matches app dark theme) ────────────────────────
BG      = "#020408"
PANEL   = "#0d1117"
BORDER  = "#1e2d3d"
LOW_C   = "#34d399"   # green
MED_C   = "#fbbf24"   # amber
HIGH_C  = "#f87171"   # red
VLOW_C  = "#818cf8"   # purple (for very_low / very_high)
MARKER  = "#00d4ff"   # cyan — current value line
TEXT    = "#94a3b8"
TITLE   = "#e2e8f0"

matplotlib.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    BORDER,
    "axes.labelcolor":   TEXT,
    "xtick.color":       TEXT,
    "ytick.color":       TEXT,
    "text.color":        TITLE,
    "grid.color":        BORDER,
    "grid.linewidth":    0.5,
    "font.family":       "monospace",
    "font.size":         8,
})


def _ax_mf(ax, universe, mfs: dict, current_val: float | None = None,
           xlabel: str = "", title: str = ""):
    """Draw one MF panel."""
    color_map = {
        "very_low":   VLOW_C,
        "low":        LOW_C,
        "medium":     MED_C,
        "medium_high":"#34d399",
        "high":       HIGH_C,
        "very_high":  "#00d4ff",
    }
    for label, mf_vals in mfs.items():
        color = color_map.get(label, "#a78bfa")
        ax.plot(universe, mf_vals, color=color, lw=1.6, label=label)
        # shaded fill under curve
        ax.fill_between(universe, mf_vals, alpha=0.07, color=color)

    if current_val is not None:
        ax.axvline(current_val, color=MARKER, lw=1.5, ls="--", alpha=0.85)
        # membership degree annotation
        ax.text(current_val, 1.04, f"{current_val:.1f}",
                ha="center", va="bottom", color=MARKER,
                fontsize=7, fontweight="bold")

    ax.set_xlim(universe[0], universe[-1])
    ax.set_ylim(-0.05, 1.15)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(["0", "0.5", "1"], fontsize=6)
    ax.set_xlabel(xlabel, fontsize=7, color=TEXT, labelpad=3)
    ax.set_title(title, fontsize=8, color=TITLE, pad=4, fontweight="bold")
    ax.grid(True, axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(BORDER)
    ax.legend(fontsize=6, loc="upper right", framealpha=0.2,
              labelcolor=TEXT, edgecolor=BORDER)


def make_input_mf_figure(sg: float, ic: float, ln: float, sm: float):
    """Figure: 4 input MFs with current values marked."""
    fig = plt.figure(figsize=(11, 5.5), facecolor=BG)
    fig.suptitle("Input Membership Functions — current values marked (──)",
                 fontsize=9, color=TITLE, y=0.98, fontweight="bold")

    gs = GridSpec(2, 2, figure=fig, hspace=0.55, wspace=0.38,
                  left=0.07, right=0.97, top=0.90, bottom=0.08)

    # ScreenGlances 0–150
    u_sg = np.arange(0, 151, 1)
    mfs_sg = {
        "low":    fuzz.trapmf(u_sg, [0,  0,  20, 40]),
        "medium": fuzz.trimf (u_sg, [20, 50, 90]),
        "high":   fuzz.trapmf(u_sg, [65, 90, 150, 150]),
    }
    ax = fig.add_subplot(gs[0, 0])
    _ax_mf(ax, u_sg, mfs_sg, sg, "glances / day", "ScreenGlances")

    # IdleChecking 0–80
    u_ic = np.arange(0, 81, 1)
    mfs_ic = {
        "low":    fuzz.trapmf(u_ic, [0,  0,  10, 25]),
        "medium": fuzz.trimf (u_ic, [18, 35, 52]),
        "high":   fuzz.trapmf(u_ic, [42, 58, 80, 85]),
    }
    ax = fig.add_subplot(gs[0, 1])
    _ax_mf(ax, u_ic, mfs_ic, ic, "idle checks / day", "IdleChecking")

    # LateNightUse 0–120
    u_ln = np.arange(0, 121, 1)
    mfs_ln = {
        "low":    fuzz.trapmf(u_ln, [0,   0,   15,  30]),
        "medium": fuzz.trimf (u_ln, [15,  30,  60]),
        "high":   fuzz.trapmf(u_ln, [31,  60, 120, 120]),
    }
    ax = fig.add_subplot(gs[1, 0])
    _ax_mf(ax, u_ln, mfs_ln, ln, "min after 22:00", "LateNightUse")

    # SocialMediaUsage 0–100
    u_sm = np.arange(0, 101, 1)
    mfs_sm = {
        "low":    fuzz.trapmf(u_sm, [0,  0,  10, 25]),
        "medium": fuzz.trimf (u_sm, [15, 30, 55]),
        "high":   fuzz.trapmf(u_sm, [40, 70, 100, 100]),
    }
    ax = fig.add_subplot(gs[1, 1])
    _ax_mf(ax, u_sm, mfs_sm, sm, "% of screen time", "SocialMediaUsage")

    return fig


def make_output_mf_figure(focus: float, sleep: float, overload: float, habit: float):
    """
    Output MF figure — imports MFs directly from fuzzy_engine_v4.
    This guarantees pixel-perfect consistency: if the engine MFs change,
    the visualisation updates automatically with zero drift.
    """
    from fuzzy_engine import (
        focus_quality, sleep_quality, digital_overload, habit_balance_out
    )

    fig = plt.figure(figsize=(11, 5.5), facecolor=BG)
    fig.suptitle("Output Membership Functions — defuzzified values marked (──)",
                 fontsize=9, color=TITLE, y=0.98, fontweight="bold")

    gs = GridSpec(2, 2, figure=fig, hspace=0.55, wspace=0.38,
                  left=0.07, right=0.97, top=0.90, bottom=0.08)

    def var_to_mfs(var):
        """Extract {term: mf_array} dict from a skfuzzy Consequent."""
        return {name: term.mf for name, term in var.terms.items()}

    u = var_to_mfs(focus_quality)  # use engine universe
    universe = focus_quality.universe

    ax = fig.add_subplot(gs[0, 0])
    _ax_mf(ax, universe, var_to_mfs(focus_quality),    focus,   "score (0–10)", "FocusQuality")

    ax = fig.add_subplot(gs[0, 1])
    _ax_mf(ax, universe, var_to_mfs(sleep_quality),    sleep,   "score (0–10)", "SleepQuality")

    ax = fig.add_subplot(gs[1, 0])
    _ax_mf(ax, universe, var_to_mfs(digital_overload), overload,"score (0–10)", "DigitalOverload")

    ax = fig.add_subplot(gs[1, 1])
    _ax_mf(ax, universe, var_to_mfs(habit_balance_out),habit,   "score (0–10)",
           "HabitBalance  ← 4th Mamdani FIS")

    return fig


def make_hierarchy_figure(focus: float, sleep: float,
                          overload: float, habit: float):
    """Mini bar chart showing the 4 output values side by side."""
    fig, ax = plt.subplots(figsize=(7, 2.6), facecolor=BG)
    ax.set_facecolor(PANEL)

    labels = ["FocusQuality", "SleepQuality", "DigitalOverload", "HabitBalance ★"]
    values = [focus, sleep, overload, habit]
    from fuzzy_engine import _label_from_mf, focus_quality, digital_overload as do_var
    def _bar_color(val, invert=False):
        lbl = _label_from_mf(val, focus_quality)
        tier = {"High":"good","Medium High":"good","Medium":"med",
                "Low":"poor","Very Low":"poor"}.get(lbl,"med")
        if invert:
            tier = {"good":"poor","med":"med","poor":"good"}[tier]
        return {
            "good": LOW_C,
            "med":  MED_C,
            "poor": HIGH_C,
        }[tier]

    colors = [
        _bar_color(focus),
        _bar_color(sleep),
        _bar_color(overload, invert=True),
        _bar_color(habit),
    ]

    bars = ax.barh(labels, values, color=colors, height=0.45,
                   edgecolor=BORDER, linewidth=0.6)

    for bar, val in zip(bars, values):
        ax.text(val + 0.15, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", ha="left",
                fontsize=8, color=TITLE, fontweight="bold")

    ax.set_xlim(0, 11.5)
    ax.set_xlabel("Score (0–10)", fontsize=7, color=TEXT)
    ax.set_title("Hierarchical FIS — all outputs at a glance",
                 fontsize=8, color=TITLE, pad=5, fontweight="bold")
    ax.axvline(5, color=BORDER, lw=0.8, ls=":")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(BORDER)
    ax.tick_params(colors=TEXT, labelsize=7)
    fig.tight_layout(pad=0.8)
    return fig