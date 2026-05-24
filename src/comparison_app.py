"""
comparison_app.py
=================
Streamlit dashboard that runs BOTH the fuzzy engine and the crisp baseline
side by side, so you can see the difference live.

Run with:
    streamlit run comparison_app.py
"""

import pandas as pd
import streamlit as st
from fuzzy_engine_v4 import evaluate_fuzzy_system
from crisp_engine import evaluate_crisp_system

st.set_page_config(
    page_title="Fuzzy vs. Crisp — Digital Habit Comparison",
    page_icon="⚖️",
    layout="wide",
)

# ─── STYLING ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp { background: #f8fafc; }
.block-container { padding: 1.5rem 1rem 3rem !important; max-width: 1500px !important; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }

.hero {
    padding: 1.4rem 1.8rem; border-radius: 14px;
    background: #0D1B2A; color: white; margin-bottom: 1.2rem;
}
.hero-title  { font-size: 1.7rem; font-weight: 700; margin-bottom: 0.2rem; }
.hero-sub    { font-size: 0.9rem; color: #94a3b8; }

.engine-header {
    padding: 0.7rem 1rem; border-radius: 10px 10px 0 0;
    font-weight: 600; font-size: 0.95rem; text-align: center;
    margin-bottom: 0;
}
.fuzzy-header { background: #1B4F72; color: white; }
.crisp-header { background: #7f1d1d; color: white; }

.metric-card {
    background: white; border-radius: 10px; padding: 1rem 1.2rem;
    border: 1px solid #e2e8f0; margin-bottom: 0.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.metric-label { font-size: 0.72rem; font-weight: 600; color: #64748b;
                text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.2rem; }
.metric-value { font-size: 1.9rem; font-weight: 700; line-height: 1; }
.metric-tag   { font-size: 0.75rem; font-weight: 500; margin-top: 0.2rem; }

.diff-card {
    background: white; border-radius: 10px; padding: 1rem 1.2rem;
    border: 1px solid #e2e8f0; margin-bottom: 0.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.diff-label { font-size: 0.72rem; font-weight: 600; color: #64748b;
              text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.2rem; }
.diff-value { font-size: 1.6rem; font-weight: 700; }

.rec-box {
    padding: 0.9rem 1.1rem; border-radius: 10px; font-size: 0.88rem;
    line-height: 1.55; margin-top: 0.6rem;
}
.rec-fuzzy { background: #eff6ff; border-left: 3px solid #1B4F72; color: #1e3a5f; }
.rec-crisp { background: #fef2f2; border-left: 3px solid #991b1b; color: #7f1d1d; }

.class-badge {
    display: inline-block; padding: 2px 10px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; margin-right: 4px;
    font-family: 'JetBrains Mono', monospace;
}
.badge-low    { background: #d1fae5; color: #065f46; }
.badge-medium { background: #fef3c7; color: #78350f; }
.badge-high   { background: #fee2e2; color: #7f1d1d; }

.cliff-box {
    background: #fff7ed; border: 1px solid #fed7aa; border-radius: 10px;
    padding: 0.9rem 1.1rem; margin-top: 0.8rem; font-size: 0.85rem; color: #7c2d12;
}
.section-title { font-size: 0.8rem; font-weight: 600; color: #64748b;
                 text-transform: uppercase; letter-spacing: 0.08em;
                 margin-bottom: 0.5rem; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ────────────────────────────────────────────────────────────────
def score_color(val, invert=False):
    v = (10 - val) if invert else val
    if v >= 6.5: return "#059669"
    if v >= 3.5: return "#d97706"
    return "#dc2626"

def badge_cls(cls):
    return f'<span class="class-badge badge-{cls}">{cls.upper()}</span>'


# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Input Variables")
    st.caption("Adjust sliders — both engines update instantly.")

    sg = st.slider("Screen Glances",    0, 150, 50, 1, help="Phone unlocks / day")
    ic = st.slider("Idle Checking",      0,  80, 20, 1, help="Short habitual checks / day")
    ln = st.slider("Late Night Use",     0, 180, 30, 1, help="Minutes after 22:00")
    sm = st.slider("Social Media %",     0, 100, 40, 1, help="% of total screen time")

    st.divider()
    st.markdown("### 🧪 Preset Profiles")
    presets = {
        "Balanced User":       (25, 10, 10, 20),
        "Night Owl":           (60, 28,110, 70),
        "Distracted Achiever": (98, 50, 45, 68),
        "Focused Worker":      (30,  8, 35, 18),
        "Borderline SG=50":    (50, 20, 30, 40),
    }
    selected = st.selectbox("Load a preset", ["— custom —"] + list(presets.keys()))
    if selected != "— custom —":
        sg, ic, ln, sm = presets[selected]


# ─── EVALUATE ───────────────────────────────────────────────────────────────
fr = evaluate_fuzzy_system(sg, ic, ln, sm)
cr = evaluate_crisp_system(sg, ic, ln, sm)
fo = fr["outputs"]; co = cr["outputs"]
fl = fr["labels"];  cl = cr["labels"]
cc = cr["classes"]


# ─── HERO ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-title">⚖️ Fuzzy vs. Crisp — Digital Habit Comparison</div>
    <div class="hero-sub">
        Both engines receive the same inputs and produce a HabitBalance score (0–10).
        The difference reveals where fuzzy logic outperforms crisp if-else logic.
    </div>
</div>
""", unsafe_allow_html=True)

# Input classes row
st.markdown("**Crisp classification of your inputs:**")
cols_cls = st.columns(4)
labels_cls = [("Screen Glances", cc["ScreenGlances"], sg),
              ("Idle Checking",  cc["IdleChecking"],  ic),
              ("Late Night Use", cc["LateNightUse"],  ln),
              ("Social Media",   cc["SocialMediaUsage"], sm)]
for col, (name, cls, val) in zip(cols_cls, labels_cls):
    col.markdown(f"**{name}** ({val}) {badge_cls(cls)}", unsafe_allow_html=True)

st.divider()

# ─── MAIN COMPARISON ────────────────────────────────────────────────────────
col_fuzzy, col_diff, col_crisp = st.columns([2, 1, 2], gap="medium")

with col_fuzzy:
    st.markdown('<div class="engine-header fuzzy-header">🔵 FUZZY ENGINE</div>', unsafe_allow_html=True)
    st.markdown("")

    for label, key, invert in [
        ("Focus Quality",    "FocusQuality",    False),
        ("Sleep Quality",    "SleepQuality",    False),
        ("Digital Overload", "DigitalOverload", True),
    ]:
        val = fo[key]; lbl = fl[key]
        col = score_color(val, invert)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{col}">{val:.2f}</div>
            <div class="metric-tag" style="color:{col}">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    fh = fo["HabitBalance"]
    fh_col = score_color(fh)
    st.markdown(f"""
    <div class="metric-card" style="border:2px solid #1B4F72">
        <div class="metric-label">⭐ Habit Balance</div>
        <div class="metric-value" style="color:{fh_col};font-size:2.6rem">{fh:.2f}<span style="font-size:1rem;color:#94a3b8">/10</span></div>
        <div class="metric-tag" style="color:{fh_col}">{fl["HabitBalance"]}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="rec-box rec-fuzzy"><strong>Recommendation</strong><br>{fr["recommendation"]}</div>',
                unsafe_allow_html=True)

with col_diff:
    st.markdown("**Δ Difference**")
    st.caption("Fuzzy − Crisp")

    for label, key, invert in [
        ("Focus",    "FocusQuality",    False),
        ("Sleep",    "SleepQuality",    False),
        ("Overload", "DigitalOverload", False),
    ]:
        diff = fo[key] - co[key]
        sign = "+" if diff >= 0 else ""
        col  = "#059669" if diff > 0.05 else "#dc2626" if diff < -0.05 else "#94a3b8"
        st.markdown(f"""
        <div class="diff-card">
            <div class="diff-label">{label}</div>
            <div class="diff-value" style="color:{col}">{sign}{diff:.2f}</div>
        </div>""", unsafe_allow_html=True)

    hdiff = fh - co["HabitBalance"]
    hsign = "+" if hdiff >= 0 else ""
    hcol  = "#059669" if hdiff > 0.05 else "#dc2626" if hdiff < -0.05 else "#94a3b8"
    st.markdown(f"""
    <div class="diff-card" style="border:2px solid {hcol}">
        <div class="diff-label">⭐ Habit Balance</div>
        <div class="diff-value" style="color:{hcol};font-size:2rem">{hsign}{hdiff:.2f}</div>
    </div>""", unsafe_allow_html=True)

    # Cliff warning
    if sg >= 40 and sg <= 70:
        st.markdown(f"""
        <div class="cliff-box">
            ⚠️ <strong>Borderline zone</strong><br>
            SG={sg} is near the crisp threshold (65).
            Crisp assigns a fixed class — fuzzy uses partial membership.
        </div>""", unsafe_allow_html=True)

with col_crisp:
    st.markdown('<div class="engine-header crisp-header">🔴 CRISP ENGINE</div>', unsafe_allow_html=True)
    st.markdown("")

    for label, key, invert in [
        ("Focus Quality",    "FocusQuality",    False),
        ("Sleep Quality",    "SleepQuality",    False),
        ("Digital Overload", "DigitalOverload", True),
    ]:
        val = co[key]; lbl = cl[key]
        col = score_color(val, invert)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{col}">{val:.2f}</div>
            <div class="metric-tag" style="color:{col}">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    ch = co["HabitBalance"]
    ch_col = score_color(ch)
    st.markdown(f"""
    <div class="metric-card" style="border:2px solid #991b1b">
        <div class="metric-label">⭐ Habit Balance</div>
        <div class="metric-value" style="color:{ch_col};font-size:2.6rem">{ch:.2f}<span style="font-size:1rem;color:#94a3b8">/10</span></div>
        <div class="metric-tag" style="color:{ch_col}">{cl["HabitBalance"]}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="rec-box rec-crisp"><strong>Recommendation</strong><br>{cr["recommendation"]}</div>',
                unsafe_allow_html=True)


# ─── CHART ──────────────────────────────────────────────────────────────────
st.divider()
st.markdown("### 📊 Side-by-side Output Comparison")

metrics = ["FocusQuality", "SleepQuality", "DigitalOverload", "HabitBalance"]
labels  = ["Focus Quality", "Sleep Quality", "Digital Overload", "Habit Balance"]

chart_df = pd.DataFrame({
    "Metric": labels * 2,
    "Score":  [fo[m] for m in metrics] + [co[m] for m in metrics],
    "Engine": ["Fuzzy"] * 4 + ["Crisp"] * 4,
})

import altair as alt
chart = alt.Chart(chart_df).mark_bar().encode(
    x=alt.X("Metric:N", axis=alt.Axis(labelAngle=0), title=None),
    y=alt.Y("Score:Q", scale=alt.Scale(domain=[0,10]), title="Score (0–10)"),
    color=alt.Color("Engine:N", scale=alt.Scale(domain=["Fuzzy","Crisp"], range=["#1B4F72","#991b1b"])),
    xOffset="Engine:N",
    tooltip=["Engine:N","Metric:N", alt.Tooltip("Score:Q", format=".2f")],
).properties(height=320)

st.altair_chart(chart, use_container_width=True)


# ─── PROFILE TABLE ──────────────────────────────────────────────────────────
st.divider()
st.markdown("### 🧪 All Profiles — Fuzzy vs. Crisp")
st.caption("HabitBalance scores for all 4 reference profiles")

profiles = [
    ("Balanced User",        25, 10, 10, 20),
    ("Night Owl",            60, 28,110, 70),
    ("Distracted Achiever",  98, 50, 45, 68),
    ("Focused Worker",       30,  8, 35, 18),
    ("Borderline SG=50",     50, 20, 30, 40),
]

rows = []
for name, psg, pic, pln, psm in profiles:
    pf = evaluate_fuzzy_system(psg, pic, pln, psm)["outputs"]["HabitBalance"]
    pc = evaluate_crisp_system(psg, pic, pln, psm)["outputs"]["HabitBalance"]
    rows.append({
        "Profile": name,
        "Fuzzy HabitBalance": pf,
        "Crisp HabitBalance": pc,
        "Difference (F−C)": round(pf - pc, 2),
    })

df = pd.DataFrame(rows)
st.dataframe(
    df.style
      .format({"Fuzzy HabitBalance":"{:.2f}","Crisp HabitBalance":"{:.2f}","Difference (F−C)":"{:+.2f}"})
      .map(lambda v: "color: #059669; font-weight:600" if isinstance(v, float) and v > 0
                else ("color: #dc2626; font-weight:600" if isinstance(v, float) and v < 0 else ""),
                subset=["Difference (F−C)"]),
    width='stretch',
    hide_index=True,
)

with st.expander("Show raw JSON output"):
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Fuzzy result")
        st.json(fr)
    with c2:
        st.caption("Crisp result")
        st.json(cr)
