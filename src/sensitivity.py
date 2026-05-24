"""
sensitivity.py — Sensitivity analysis for fuzzy-detox
Starting from an ideal baseline, each input is degraded to its maximum
to show which has the greatest impact on HabitBalance.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fuzzy_engine_v4 import evaluate_fuzzy_system

# Ideal baseline: all inputs at low/healthy values
BASELINE = {"ScreenGlances": 10, "IdleChecking": 5,
            "LateNightUse":  10, "SocialMediaUsage": 10}

INPUT_RANGES  = {"ScreenGlances": (0,150), "IdleChecking": (0,80),
                 "LateNightUse":  (0,180), "SocialMediaUsage": (0,100)}
OUTPUTS       = ["FocusQuality","SleepQuality","DigitalOverload","HabitBalance"]
SHORT         = ["ScreenGlances","IdleChecking","LateNightUse","SocialMedia"]
INPUT_NAMES   = list(INPUT_RANGES.keys())


def run_sweep(input_name: str, n_steps: int = 60):
    lo, hi   = INPUT_RANGES[input_name]
    values   = np.linspace(lo, hi, n_steps)
    results  = {k: [] for k in OUTPUTS}
    for v in values:
        inputs = dict(BASELINE)
        inputs[input_name] = float(v)
        out = evaluate_fuzzy_system(
            inputs["ScreenGlances"], inputs["IdleChecking"],
            inputs["LateNightUse"],  inputs["SocialMediaUsage"])["outputs"]
        for k in OUTPUTS:
            results[k].append(out[k])
    return values, results


def sensitivity_range(input_name):
    _, res = run_sweep(input_name)
    return {k: round(max(res[k]) - min(res[k]), 3) for k in OUTPUTS}


def make_sensitivity_figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    BG    = "#ffffff"; PANEL = "#f8fafc"; BORD = "#e2e8f0"
    COLS  = ["#6366f1","#0ea5e9","#f59e0b","#10b981"]
    TEXT  = "#475569"; TITLE = "#1e293b"

    matplotlib.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": PANEL,
        "axes.edgecolor": BORD, "axes.labelcolor": TEXT,
        "xtick.color": TEXT, "ytick.color": TEXT,
        "text.color": TITLE, "grid.color": BORD,
        "grid.linewidth": 0.6, "font.family": "sans-serif", "font.size": 8,
    })

    # ── Figure 1: response curves ─────────────────────────
    fig1, axes = plt.subplots(2, 2, figsize=(11, 7), facecolor=BG)
    fig1.suptitle(
        "Sensitivity Analysis — each input swept from min to max (others fixed at ideal baseline)\n"
        "Starting point: ScreenGlances=10, IdleChecking=5, LateNightUse=10, SocialMedia=10%",
        fontsize=9, color=TITLE, fontweight="bold", y=1.01)

    for i, (iname, col) in enumerate(zip(INPUT_NAMES, COLS)):
        ax = axes[i//2][i%2]
        vals, res = run_sweep(iname)
        hb = res["HabitBalance"]
        rng = round(max(hb) - min(hb), 2)

        ax.plot(vals, hb,                    color=col,       lw=2.4, label=f"HabitBalance (Δ={rng:.1f})", zorder=4)
        ax.plot(vals, res["FocusQuality"],    color="#94a3b8", lw=1.0, ls="--", label="FocusQuality",    alpha=0.75)
        ax.plot(vals, res["SleepQuality"],    color="#64748b", lw=1.0, ls=":",  label="SleepQuality",    alpha=0.75)
        ax.plot(vals, res["DigitalOverload"], color="#f87171", lw=1.0, ls="-.", label="DigitalOverload", alpha=0.75)

        # shade the degradation zone
        ax.fill_between(vals, hb, min(hb), alpha=0.08, color=col)

        ax.set_title(SHORT[i], fontsize=9, color=TITLE, fontweight="bold", pad=4)
        ax.set_xlabel(iname, fontsize=7, color=TEXT, labelpad=2)
        ax.set_ylabel("Score (0–10)" if i%2==0 else "", fontsize=7, color=TEXT)
        ax.set_ylim(-0.3, 11.2)
        ax.set_yticks([0,2,4,6,8,10])
        ax.grid(True, alpha=0.4, axis="y")
        ax.spines[["top","right"]].set_visible(False)
        ax.spines[["left","bottom"]].set_color(BORD)
        ax.legend(fontsize=6.5, loc="lower left" if iname != "SocialMediaUsage" else "upper left",
                  framealpha=0.85, labelcolor=TEXT, edgecolor=BORD)

    fig1.tight_layout(pad=1.2)

    # ── Figure 2: ranking ─────────────────────────────────
    all_ranges = {iname: sensitivity_range(iname) for iname in INPUT_NAMES}

    fig2, ax2 = plt.subplots(figsize=(7, 4), facecolor=BG)
    ax2.set_facecolor(PANEL)
    fig2.suptitle("HabitBalance sensitivity ranking\n(how much can each input alone degrade the score?)",
                  fontsize=9, color=TITLE, fontweight="bold")

    hb_r = {iname: all_ranges[iname]["HabitBalance"] for iname in INPUT_NAMES}
    sorted_items = sorted(hb_r.items(), key=lambda x: x[1], reverse=True)
    names_s = [SHORT[INPUT_NAMES.index(k)] for k,_ in sorted_items]
    vals_s  = [v for _,v in sorted_items]
    bar_c   = [COLS[INPUT_NAMES.index(k)] for k,_ in sorted_items]

    bars = ax2.barh(names_s, vals_s, color=bar_c, edgecolor=BORD,
                    linewidth=0.5, alpha=0.88, height=0.45)
    for bar, val in zip(bars, vals_s):
        pct = val / 10 * 100
        ax2.text(val+0.05, bar.get_y()+bar.get_height()/2,
                 f"{val:.2f} pts  ({pct:.0f}% of scale)",
                 va="center", fontsize=8.5, color=TITLE, fontweight="bold")

    ax2.set_xlabel("HabitBalance variation (0–10 scale)", fontsize=8, color=TEXT, labelpad=4)
    ax2.set_xlim(0, 13)
    ax2.spines[["top","right"]].set_visible(False)
    ax2.spines[["left","bottom"]].set_color(BORD)
    ax2.grid(True, axis="x", alpha=0.35)
    ax2.tick_params(labelsize=9)
    fig2.tight_layout(pad=1.4)
    return fig1, fig2, all_ranges


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    fig1, fig2, ranges = make_sensitivity_figures()
    out = os.path.join(os.path.dirname(__file__), "..", "docs")
    os.makedirs(out, exist_ok=True)
    fig1.savefig(f"{out}/sensitivity_curves.png",  dpi=150, bbox_inches="tight")
    fig2.savefig(f"{out}/sensitivity_ranking.png", dpi=150, bbox_inches="tight")
    plt.close("all")

    print("\nHabitBalance sensitivity ranking:")
    hb = {k: ranges[k]["HabitBalance"] for k in ranges}
    for name, val in sorted(hb.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name:<22} range = {val:.2f} pts  ({val/10*100:.0f}% of scale)")
