import pandas as pd
import streamlit as st
import math
from crisp_engine import evaluate_crisp_system

st.set_page_config(
    page_title="crisp-detox · Digital Habit Recommender",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# DESIGN SYSTEM
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;700&family=Outfit:wght@200;300;400;600;700;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #0a0a0a;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(220,38,38,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(180,30,30,0.05) 0%, transparent 55%);
    min-height: 100vh;
}
.block-container { padding: 1.5rem 1rem 4rem !important; max-width: 1600px !important; }
#MainMenu, footer { visibility: hidden; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; color: #e2e8f0; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(10,0,0,0.97) !important;
    border-right: 1px solid rgba(220,38,38,0.1) !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 0.9rem !important; }
.sidebar-brand {
    font-family: 'JetBrains Mono', monospace; font-size: 0.63rem; font-weight: 500;
    color: rgba(220,38,38,0.55); letter-spacing: 0.2em; text-transform: uppercase;
    margin-bottom: 1.5rem; padding-bottom: 0.8rem;
    border-bottom: 1px solid rgba(220,38,38,0.1);
}
.zone-tag {
    display: inline-flex; align-items: center; gap: 5px;
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 500;
    padding: 3px 10px; border-radius: 999px; margin-top: 3px; margin-bottom: 6px;
}
.zone-low    { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(16,185,129,0.25); }
.zone-medium { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.25); }
.zone-high   { background: rgba(239,68,68,0.12);  color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

/* HERO */
.hero-wrapper {
    padding: 1.8rem 2rem 1.6rem; border-radius: 20px;
    background: rgba(255,255,255,0.022);
    border: 1px solid rgba(220,38,38,0.12);
    position: relative; overflow: hidden; margin-bottom: 1.2rem;
}
.hero-wrapper::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(220,38,38,0.7), rgba(180,30,30,0.4), transparent);
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: rgba(220,38,38,0.75);
    margin-bottom: 0.5rem; display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before { content: ''; display: inline-block; width: 18px; height: 1px; background: rgba(220,38,38,0.6); }
.hero-title {
    font-family: 'Outfit', sans-serif; font-size: 2.8rem; font-weight: 900;
    line-height: 1.0; letter-spacing: -0.02em; color: #f8fafc; margin-bottom: 0.4rem;
}
.hero-title span { background: linear-gradient(135deg, #f87171, #dc2626, #991b1b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 300; color: rgba(226,232,240,0.45); max-width: 580px; line-height: 1.6; }
.hero-corner { position: absolute; right: 1.8rem; top: 50%; transform: translateY(-50%); font-family: 'JetBrains Mono', monospace; font-size: 4.5rem; font-weight: 700; color: rgba(220,38,38,0.04); letter-spacing: -0.05em; user-select: none; }

/* CRISP LABEL STRIP */
.crisp-strip {
    display: flex; align-items: center; gap: 1rem; padding: 0.85rem 1.4rem;
    border-radius: 14px; background: rgba(220,38,38,0.07);
    border: 1px solid rgba(220,38,38,0.2); margin-bottom: 1.2rem;
    position: relative; overflow: hidden;
}
.crisp-strip::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: linear-gradient(180deg, #dc2626, #991b1b); border-radius: 3px 0 0 3px; }
.crisp-strip-label { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: rgba(248,113,113,0.7); letter-spacing: 0.12em; text-transform: uppercase; }
.crisp-class { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 700; }
.cls-low    { color: #34d399; }
.cls-medium { color: #fbbf24; }
.cls-high   { color: #f87171; }

/* CARDS */
.card {
    border-radius: 18px; padding: 1.2rem 1.3rem;
    background: rgba(255,255,255,0.022); border: 1px solid rgba(255,255,255,0.07);
    position: relative; overflow: hidden; height: 100%;
}
.card-glow-red::before    { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(220,38,38,0.6), transparent); }
.card-glow-amber::before  { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(245,158,11,0.55), transparent); }
.card-glow-green::before  { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(16,185,129,0.5), transparent); }
.card-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; font-weight: 500;
    letter-spacing: 0.16em; text-transform: uppercase; color: rgba(226,232,240,0.3);
    margin-bottom: 0.9rem; display: flex; align-items: center; gap: 8px;
}
.card-label::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.05); }

/* HABIT BALANCE */
.hab-score-wrap { text-align: center; padding: 0.3rem 0; }
.hab-number { font-family: 'Outfit', sans-serif; font-size: 4rem; font-weight: 900; line-height: 1; letter-spacing: -0.03em; }
.hab-denom  { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 300; color: rgba(226,232,240,0.25); }
.hab-label  { font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 13px; border-radius: 999px; display: inline-block; margin-top: 0.4rem; }
.lab-good   { background: rgba(16,185,129,0.13);  color: #34d399; border: 1px solid rgba(16,185,129,0.28); }
.lab-medium { background: rgba(245,158,11,0.13);  color: #fbbf24; border: 1px solid rgba(245,158,11,0.28); }
.lab-poor   { background: rgba(239,68,68,0.13);   color: #f87171; border: 1px solid rgba(239,68,68,0.28);  }

/* MINI METRICS */
.mini-metric { border-radius: 14px; padding: 1.1rem 1.2rem; background: rgba(255,255,255,0.022); border: 1px solid rgba(255,255,255,0.065); position: relative; overflow: hidden; }
.mini-metric-name { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(226,232,240,0.3); margin-bottom: 0.35rem; }
.mini-metric-val  { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; line-height: 1; letter-spacing: -0.02em; }
.mini-metric-lbl  { font-family: 'Space Grotesk', sans-serif; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.35rem; }
.mini-bar-track   { height: 2px; border-radius: 1px; background: rgba(255,255,255,0.05); margin-top: 0.7rem; overflow: hidden; }
.mini-bar-fill    { height: 100%; border-radius: 1px; }

/* RECOMMENDATION */
.rec-general { font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 300; color: rgba(226,232,240,0.7); line-height: 1.6; padding: 0.9rem 1.1rem; border-radius: 10px; background: rgba(220,38,38,0.04); border-left: 2px solid rgba(220,38,38,0.4); margin-bottom: 0.7rem; }
.rec-item     { font-family: 'Space Grotesk', sans-serif; font-size: 0.84rem; font-weight: 400; color: rgba(226,232,240,0.75); line-height: 1.5; padding: 0.7rem 0.9rem 0.7rem 1rem; border-radius: 9px; background: rgba(245,158,11,0.04); border-left: 2px solid rgba(245,158,11,0.35); margin-bottom: 0.45rem; }

/* LIMITATION BOX */
.limit-box {
    padding: 0.9rem 1.1rem; border-radius: 12px; margin-top: 0.8rem;
    background: rgba(220,38,38,0.06); border: 1px solid rgba(220,38,38,0.18);
    font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem;
    color: rgba(248,113,113,0.8); line-height: 1.5;
}

div[data-testid="stMetricValue"] { color: #f8fafc; }
div[data-testid="stMetricLabel"] { color: #cbd5e1; }
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: rgba(220,38,38,0.15); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPERS
# ============================================================
def score_color(val, invert=False):
    v = (10 - val) if invert else val
    if v >= 6.5: return "#34d399"
    if v >= 3.5: return "#fbbf24"
    return "#f87171"

def score_label(val, invert=False):
    v = (10 - val) if invert else val
    if v >= 6.5: return "Good",    "lab-good"
    if v >= 3.5: return "Moderate","lab-medium"
    return "Poor", "lab-poor"

def specific_recs(sg, ic, ln, sm):
    recs = []
    if ln >= 65: recs.append(f"🌙 <b>LateNightUse = {ln} min</b> — Enable bedtime mode after 22:00.")
    if ic >= 40: recs.append(f"⏳ <b>IdleChecking = {ic}/day</b> — Keep phone out of reach during idle moments.")
    if sg >= 65: recs.append(f"👁 <b>ScreenGlances = {sg}/day</b> — Disable non-essential notifications.")
    if sm >= 55: recs.append(f"📱 <b>SocialMedia = {sm}%</b> — Set fixed time windows for social apps.")
    if not recs:
        recs.append("✅ <b>All habits look balanced.</b> Maintain intentional phone use.")
    return recs

THRESHOLDS = {
    "ScreenGlances":    (40, 65),
    "IdleChecking":     (20, 40),
    "LateNightUse":     (25, 65),
    "SocialMediaUsage": (30, 55),
}

def zone_tag(val, lo, hi):
    if val <= lo:  return "Low",    "zone-low"
    if val <= hi:  return "Medium", "zone-medium"
    return "High", "zone-high"

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">◈ crisp-detox · inputs</div>', unsafe_allow_html=True)

    sliders = [
        ("ScreenGlances",    "Screen Glances",  0, 150, 50, 1, "Phone unlocks / day"),
        ("IdleChecking",     "Idle Checking",   0,  80, 20, 1, "Habitual short checks / day"),
        ("LateNightUse",     "Late Night Use",  0, 180, 30, 1, "Minutes of use after 22:00"),
        ("SocialMediaUsage", "Social Media %",  0, 100, 40, 1, "% of total screen time"),
    ]
    vals = {}
    for key, label, mn, mx, default, step, hint in sliders:
        col_sl, col_num = st.columns([3, 1])
        with col_sl:
            val = st.slider(label, mn, mx, default, step, help=hint)
        with col_num:
            st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.85rem;color:rgba(226,232,240,0.6);padding-top:1.8rem;text-align:center">{val}</div>', unsafe_allow_html=True)
        z_name, z_cls = zone_tag(val, *THRESHOLDS[key])
        st.markdown(f'<div class="zone-tag {z_cls}">◆ {z_name}</div>', unsafe_allow_html=True)
        vals[key] = val

# ============================================================
# EVALUATE
# ============================================================
result = evaluate_crisp_system(
    screen_glances_value=vals["ScreenGlances"],
    idle_checking_value=vals["IdleChecking"],
    late_night_use_value=vals["LateNightUse"],
    social_media_value=vals["SocialMediaUsage"],
)
o  = result["outputs"]
lb = result["labels"]
cl = result["classes"]

habit   = o["HabitBalance"]
focus   = o["FocusQuality"]
sleep   = o["SleepQuality"]
overload= o["DigitalOverload"]

hab_col = score_color(habit)
hab_lbl, hab_cls = score_label(habit)
recs = specific_recs(vals["ScreenGlances"], vals["IdleChecking"],
                     vals["LateNightUse"],  vals["SocialMediaUsage"])

# ============================================================
# HERO
# ============================================================
st.markdown(f"""
<div class="hero-wrapper">
    <div class="hero-eyebrow">Crisp If-Else Rule System · Fixed Thresholds</div>
    <div class="hero-title">Digital Habit <span>Recommender</span></div>
    <div class="hero-sub">Enter your phone behaviour values. The system classifies each input into a fixed category and returns a HabitBalance score (0–10) with a personalised recommendation.</div>
    <div class="hero-corner">CRS</div>
</div>
""", unsafe_allow_html=True)

# Crisp classes strip
sg_c = cl["ScreenGlances"]; ic_c = cl["IdleChecking"]
ln_c = cl["LateNightUse"];  sm_c = cl["SocialMediaUsage"]
st.markdown(f"""
<div class="crisp-strip">
    <div class="crisp-strip-label">Classified as →</div>
    <div>
        <span style="color:rgba(226,232,240,0.4);font-size:0.75rem">ScreenGlances</span>
        <span class="crisp-class cls-{sg_c}"> {sg_c.upper()}</span>
    </div>
    <div>
        <span style="color:rgba(226,232,240,0.4);font-size:0.75rem">IdleChecking</span>
        <span class="crisp-class cls-{ic_c}"> {ic_c.upper()}</span>
    </div>
    <div>
        <span style="color:rgba(226,232,240,0.4);font-size:0.75rem">LateNightUse</span>
        <span class="crisp-class cls-{ln_c}"> {ln_c.upper()}</span>
    </div>
    <div>
        <span style="color:rgba(226,232,240,0.4);font-size:0.75rem">SocialMedia</span>
        <span class="crisp-class cls-{sm_c}"> {sm_c.upper()}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ROW 1 — Score · Recommendations
# ============================================================
c1, c2 = st.columns([1, 1.4], gap="small")

with c1:
    st.markdown(f"""
    <div class="card card-glow-red">
        <div class="card-label">Habit Balance Score</div>
        <div class="hab-score-wrap">
            <span class="hab-number" style="color:{hab_col}">{habit:.2f}</span>
            <span class="hab-denom">/10</span><br>
            <span class="hab-label {hab_cls}">{hab_lbl}</span>
        </div>
        <div class="limit-box" style="margin-top:1rem">
            ⚠️ <strong>Crisp limitation:</strong> scores change in fixed steps.
            A value of {vals["ScreenGlances"]} ScreenGlances is classified as
            <strong>{sg_c.upper()}</strong> — 1 unit more or less can flip the entire category.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    recs_html = "".join(f'<div class="rec-item">{r}</div>' for r in recs)
    st.markdown(f"""
    <div class="card card-glow-amber">
        <div class="card-label">Recommendations</div>
        <div class="rec-general">{result["recommendation"]}</div>
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:rgba(245,158,11,0.45);margin:0.7rem 0 0.4rem">Specific actions</div>
        {recs_html}
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ROW 2 — Metric cards
# ============================================================
st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4, gap="small")

def mini_card(col, name, val, invert=False, note=""):
    col_hex = score_color(val, invert)
    lbl, _  = score_label(val, invert)
    bar_w   = int(((10 - val) if invert else val) / 10 * 100)
    col.markdown(f"""
    <div class="mini-metric">
        <div class="mini-metric-name">{name}{note}</div>
        <div class="mini-metric-val" style="color:{col_hex}">{val:.2f}</div>
        <div class="mini-metric-lbl" style="color:{col_hex}">{lbl}</div>
        <div class="mini-bar-track"><div class="mini-bar-fill" style="width:{bar_w}%;background:{col_hex};opacity:0.75"></div></div>
    </div>
    """, unsafe_allow_html=True)

mini_card(m1, "Focus Quality",    focus,    False)
mini_card(m2, "Sleep Quality",    sleep,    False)
mini_card(m3, "Digital Overload", overload, True, " ↓")
mini_card(m4, "Habit Balance",    habit,    False)

# ============================================================
# ROW 3 — Profile comparison table
# ============================================================
st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;letter-spacing:0.16em;
text-transform:uppercase;color:rgba(226,232,240,0.3);margin-bottom:0.5rem">
◈ reference profiles · crisp scores
</div>
""", unsafe_allow_html=True)

profiles = [
    ("⚖️ Balanced User",       25, 10, 10, 20),
    ("🌙 Night Owl",           60, 28,110, 70),
    ("📲 Distracted Achiever", 98, 50, 45, 68),
    ("📚 Focused Worker",      30,  8, 35, 18),
]
rows = []
for pname, psg, pic, pln, psm in profiles:
    pr = evaluate_crisp_system(psg, pic, pln, psm)
    po = pr["outputs"]
    rows.append({
        "Profile":         pname,
        "ScreenGlances":   psg,
        "IdleChecking":    pic,
        "LateNightUse":    pln,
        "SocialMedia %":   psm,
        "FocusQuality":    po["FocusQuality"],
        "SleepQuality":    po["SleepQuality"],
        "DigitalOverload": po["DigitalOverload"],
        "HabitBalance":    po["HabitBalance"],
    })

df = pd.DataFrame(rows)
st.dataframe(
    df.style.format({
        "FocusQuality":"{:.2f}", "SleepQuality":"{:.2f}",
        "DigitalOverload":"{:.2f}", "HabitBalance":"{:.2f}",
    }).background_gradient(subset=["HabitBalance"], cmap="RdYlGn", vmin=0, vmax=10),
    width='stretch', hide_index=True,
)

# ============================================================
# EXPANDERS
# ============================================================
st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
col_e1, col_e2 = st.columns(2)

with col_e1:
    with st.expander("↗ How crisp classification works"):
        st.markdown("""
**Crisp thresholds used:**

| Input | Low | Medium | High |
|---|---|---|---|
| ScreenGlances | ≤ 40 | 41–64 | ≥ 65 |
| IdleChecking | ≤ 20 | 21–39 | ≥ 40 |
| LateNightUse | ≤ 25 | 26–64 | ≥ 65 |
| SocialMedia % | ≤ 30 | 31–54 | ≥ 55 |

Each input is assigned to **exactly one** class.
The scores are fixed lookup values — no gradual transitions.

**Limitation:** A value of 64 and 65 for ScreenGlances give completely
different results, even though they are almost identical in reality.
This is the **cliff effect** — which fuzzy logic solves.
""")

with col_e2:
    with st.expander("↗ Raw crisp result (JSON)"):
        st.json(result)
