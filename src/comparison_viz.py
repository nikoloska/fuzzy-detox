"""
comparison_viz.py — Fuzzy vs Crisp visual comparison
The key argument: crisp systems jump abruptly at thresholds.
Fuzzy systems transition smoothly — this is why fuzzy logic matters.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

from fuzzy_engine import evaluate_fuzzy_system
from crisp_engine    import evaluate_crisp_system

# ── palette ────────────────────────────────────────────────
BG     = "#020408"
PANEL  = "#0d1117"
BORDER = "#1e2d3d"
FUZZY  = "#00d4ff"   # cyan
CRISP  = "#f87171"   # red
TEXT   = "#94a3b8"
TITLE  = "#e2e8f0"
THRESH = "#fbbf24"   # amber for threshold lines

matplotlib.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor":   PANEL,
    "axes.edgecolor":   BORDER,
    "axes.labelcolor":  TEXT,
    "xtick.color":      TEXT,
    "ytick.color":      TEXT,
    "text.color":       TITLE,
    "grid.color":       BORDER,
    "grid.linewidth":   0.5,
    "font.family":      "monospace",
    "font.size":        8,
})


def _ax_style(ax, title, xlabel, ylabel="Score (0–10)"):
    ax.set_title(title, fontsize=9, color=TITLE, pad=5, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=7, color=TEXT, labelpad=3)
    ax.set_ylabel(ylabel, fontsize=7, color=TEXT, labelpad=3)
    ax.set_ylim(-0.3, 10.5)
    ax.grid(True, alpha=0.25, axis="y")
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["left","bottom"]].set_color(BORDER)


def make_sweep_figure():
    """
    Main argument: sweep ScreenGlances 0→150, keep others fixed at medium.
    Shows smooth fuzzy curve vs abrupt crisp step function.
    All 4 outputs side by side.
    """
    sg_range = np.arange(0, 151, 1)
    IC_FIXED, LN_FIXED, SM_FIXED = 25, 40, 40   # medium values

    fuzzy_scores = {k: [] for k in ["FocusQuality","SleepQuality","DigitalOverload","HabitBalance"]}
    crisp_scores = {k: [] for k in ["FocusQuality","SleepQuality","DigitalOverload","HabitBalance"]}

    for sg in sg_range:
        fr = evaluate_fuzzy_system(sg, IC_FIXED, LN_FIXED, SM_FIXED)["outputs"]
        cr = evaluate_crisp_system(sg, IC_FIXED, LN_FIXED, SM_FIXED)["outputs"]
        for k in fuzzy_scores:
            fuzzy_scores[k].append(fr[k])
            crisp_scores[k].append(cr[k])

    fig = plt.figure(figsize=(13, 8), facecolor=BG)
    fig.suptitle(
        "Fuzzy vs Crisp — ScreenGlances swept 0→150  (IdleChecking=25, LateNightUse=40, SocialMedia=40%)\n"
        "Key insight: crisp scores jump abruptly at thresholds; fuzzy scores transition smoothly",
        fontsize=9, color=TITLE, y=0.98, fontweight="bold"
    )

    gs = GridSpec(2, 2, figure=fig, hspace=0.52, wspace=0.38,
                  left=0.08, right=0.97, top=0.90, bottom=0.08)

    outputs = [
        ("FocusQuality",    "FocusQuality",    gs[0,0]),
        ("SleepQuality",    "SleepQuality",    gs[0,1]),
        ("DigitalOverload", "DigitalOverload",  gs[1,0]),
        ("HabitBalance",    "HabitBalance ★",  gs[1,1]),
    ]

    # crisp thresholds for ScreenGlances
    THRESH_LOW  = 40
    THRESH_HIGH = 65

    for key, label, pos in outputs:
        ax = fig.add_subplot(pos)
        ax.plot(sg_range, fuzzy_scores[key], color=FUZZY, lw=2.0,
                label="Fuzzy (Mamdani)", zorder=3)
        ax.step(sg_range, crisp_scores[key], color=CRISP, lw=1.5,
                label="Crisp (if-else)", where="post", zorder=2, alpha=0.85)

        # threshold lines
        ax.axvline(THRESH_LOW,  color=THRESH, lw=0.9, ls="--", alpha=0.6)
        ax.axvline(THRESH_HIGH, color=THRESH, lw=0.9, ls="--", alpha=0.6)
        ax.text(THRESH_LOW+1,  0.4, "Low→Med", fontsize=6, color=THRESH, alpha=0.8)
        ax.text(THRESH_HIGH+1, 0.4, "Med→High", fontsize=6, color=THRESH, alpha=0.8)

        # annotate the jump for crisp on HabitBalance
        if key == "HabitBalance":
            idx = THRESH_HIGH
            jump = abs(crisp_scores[key][idx] - crisp_scores[key][idx-1])
            if jump > 0.3:
                ax.annotate(f"Jump: {jump:.1f}pts",
                    xy=(THRESH_HIGH, crisp_scores[key][THRESH_HIGH]),
                    xytext=(THRESH_HIGH+12, crisp_scores[key][THRESH_HIGH]+1.2),
                    fontsize=7, color=CRISP,
                    arrowprops=dict(arrowstyle="->", color=CRISP, lw=0.8))

        _ax_style(ax, label, "ScreenGlances (glances/day)")
        ax.legend(fontsize=6, loc="upper right" if key != "DigitalOverload" else "lower right",
                  framealpha=0.2, labelcolor=TEXT, edgecolor=BORDER)

    return fig


def make_threshold_demo_figure():
    """
    Zoom into the critical threshold zone (35–70 glances).
    Shows exactly what happens when you cross 40 and 65 glances.
    Perfect slide for the presentation.
    """
    sg_range = np.arange(35, 71, 1)
    IC, LN, SM = 25, 40, 40

    fuzzy_hb, crisp_hb = [], []
    for sg in sg_range:
        fuzzy_hb.append(evaluate_fuzzy_system(sg, IC, LN, SM)["outputs"]["HabitBalance"])
        crisp_hb.append(evaluate_crisp_system(sg, IC, LN, SM)["outputs"]["HabitBalance"])

    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=BG)
    ax.set_facecolor(PANEL)

    ax.plot(sg_range, fuzzy_hb, color=FUZZY, lw=2.5, label="Fuzzy — smooth transition", zorder=3)
    ax.step(sg_range, crisp_hb, color=CRISP, lw=2.0, label="Crisp — abrupt jump", where="post", zorder=2)

    # shade the jump zone
    ax.axvspan(38, 42, alpha=0.08, color=CRISP)
    ax.axvline(40, color=THRESH, lw=1.2, ls="--", alpha=0.8, label="Crisp threshold (40 glances)")

    # annotate
    ax.annotate("39 glances\nFuzzy: 6.4 | Crisp: 7.0",
        xy=(39, evaluate_fuzzy_system(39, IC, LN, SM)["outputs"]["HabitBalance"]),
        xytext=(43, 7.8), fontsize=7.5, color=FUZZY,
        arrowprops=dict(arrowstyle="->", color=FUZZY, lw=0.9))
    ax.annotate("41 glances\nFuzzy: 6.2 | Crisp: 5.5",
        xy=(41, evaluate_crisp_system(41, IC, LN, SM)["outputs"]["HabitBalance"]),
        xytext=(43, 4.8), fontsize=7.5, color=CRISP,
        arrowprops=dict(arrowstyle="->", color=CRISP, lw=0.9))

    ax.text(38.5, 3.2,
        "2 glances more\nCrisp: −1.5 pts\nFuzzy: −0.2 pts",
        fontsize=7.5, color=THRESH, ha="center",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=PANEL, edgecolor=THRESH, alpha=0.9))

    _ax_style(ax, "The threshold problem — zoom on ScreenGlances 35→70",
              "ScreenGlances (glances/day)")
    ax.set_xlim(35, 70)
    ax.legend(fontsize=7.5, loc="upper right", framealpha=0.25,
              labelcolor=TEXT, edgecolor=BORDER)
    fig.tight_layout(pad=1.0)
    return fig


def make_profile_comparison_figure():
    """
    Compare 5 predefined user profiles on all outputs.
    Grouped bar chart: fuzzy vs crisp per profile.
    """
    profiles = [
        ("Balanced",      15,  5,  10, 10),
        ("Night Owl",     70, 30, 140, 75),
        ("Doomscroller",  95, 55,  50, 88),
        ("Focused Worker",28,  8,  30, 15),
        ("Borderline",    50, 25,  50, 42),
    ]

    keys = ["FocusQuality","SleepQuality","DigitalOverload","HabitBalance"]
    labels_short = ["Focus","Sleep","Overload","Balance"]

    fig, axes = plt.subplots(1, len(profiles), figsize=(14, 4.5), facecolor=BG)
    fig.suptitle("5 user profiles — Fuzzy vs Crisp across all 4 outputs",
                 fontsize=9, color=TITLE, y=1.00, fontweight="bold")

    x = np.arange(len(keys))
    w = 0.38

    for i, (name, sg, ic, ln, sm) in enumerate(profiles):
        ax = axes[i]
        ax.set_facecolor(PANEL)

        fv = [evaluate_fuzzy_system(sg, ic, ln, sm)["outputs"][k] for k in keys]
        cv = [evaluate_crisp_system(sg, ic, ln, sm)["outputs"][k] for k in keys]

        ax.bar(x - w/2, fv, w, color=FUZZY, alpha=0.85, label="Fuzzy",
               edgecolor=BORDER, linewidth=0.5)
        ax.bar(x + w/2, cv, w, color=CRISP, alpha=0.75, label="Crisp",
               edgecolor=BORDER, linewidth=0.5)

        for j, (f, c) in enumerate(zip(fv, cv)):
            diff = f - c
            col = "#34d399" if abs(diff) < 0.5 else THRESH
            ax.text(j, max(f, c) + 0.3, f"{diff:+.1f}", ha="center",
                    fontsize=6.5, color=col, fontweight="bold")

        ax.set_title(name, fontsize=8, color=TITLE, pad=4, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(labels_short, fontsize=6.5, color=TEXT)
        ax.set_ylim(0, 11.5)
        ax.set_yticks([0, 5, 10])
        ax.spines[["top","right"]].set_visible(False)
        ax.spines[["left","bottom"]].set_color(BORDER)
        ax.tick_params(colors=TEXT)
        ax.grid(True, axis="y", alpha=0.2)
        if i == 0:
            ax.set_ylabel("Score (0–10)", fontsize=7, color=TEXT)
            ax.legend(fontsize=6, framealpha=0.2, labelcolor=TEXT, edgecolor=BORDER)

    fig.tight_layout(pad=0.6)
    return fig


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__), "..", "docs")
    os.makedirs(out, exist_ok=True)

    print("Generating sweep figure...")
    fig = make_sweep_figure()
    fig.savefig(f"{out}/comparison_sweep.png", dpi=150, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)

    print("Generating threshold demo...")
    fig = make_threshold_demo_figure()
    fig.savefig(f"{out}/comparison_threshold.png", dpi=150, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)

    print("Generating profile comparison...")
    fig = make_profile_comparison_figure()
    fig.savefig(f"{out}/comparison_profiles.png", dpi=150, bbox_inches="tight",
                facecolor=BG)
    plt.close(fig)

    print("Done — 3 figures saved to docs/")
