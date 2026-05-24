import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
import math

from fuzzy_engine import evaluate_fuzzy_system

st.set_page_config(
    page_title="fuzzy-detox · Digital Habit Balance",
    page_icon="🧠",
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
    background: #020408;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,212,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(245,158,11,0.05) 0%, transparent 55%),
        radial-gradient(ellipse 40% 60% at 50% 50%, rgba(99,102,241,0.03) 0%, transparent 70%);
    min-height: 100vh;
}
.block-container { padding: 1.5rem 1rem 4rem !important; max-width: 1600px !important; }
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; }
.stDeployButton { display: none; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; color: #e2e8f0; }

section[data-testid="stSidebar"] { background: rgba(2,8,20,0.97) !important; border-right: 1px solid rgba(0,212,255,0.1) !important; }
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 0.9rem !important; }
.sidebar-brand { font-family: 'JetBrains Mono', monospace; font-size: 0.63rem; font-weight: 500; color: rgba(0,212,255,0.55); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 1.5rem; padding-bottom: 0.8rem; border-bottom: 1px solid rgba(0,212,255,0.1); }
.zone-tag { display: inline-flex; align-items: center; gap: 5px; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 500; padding: 3px 10px; border-radius: 999px; margin-top: 3px; margin-bottom: 6px; }
.zone-low    { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(16,185,129,0.25); }
.zone-medium { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.25); }
.zone-high   { background: rgba(239,68,68,0.12);  color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

.hero-wrapper { padding: 1.8rem 2rem 1.6rem; border-radius: 20px; background: rgba(255,255,255,0.022); border: 1px solid rgba(0,212,255,0.1); position: relative; overflow: hidden; margin-bottom: 1.2rem; }
.hero-wrapper::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(0,212,255,0.6), rgba(245,158,11,0.4), transparent); }
.hero-eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(0,212,255,0.65); margin-bottom: 0.5rem; display: flex; align-items: center; gap: 8px; }
.hero-eyebrow::before { content: ''; display: inline-block; width: 18px; height: 1px; background: rgba(0,212,255,0.6); }
.hero-title { font-family: 'Outfit', sans-serif; font-size: 2.8rem; font-weight: 900; line-height: 1.0; letter-spacing: -0.02em; color: #f8fafc; margin-bottom: 0.4rem; }
.hero-title span { background: linear-gradient(135deg, #00d4ff, #a78bfa, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 300; color: rgba(226,232,240,0.45); max-width: 580px; line-height: 1.6; }
.hero-corner { position: absolute; right: 1.8rem; top: 50%; transform: translateY(-50%); font-family: 'JetBrains Mono', monospace; font-size: 4.5rem; font-weight: 700; color: rgba(0,212,255,0.035); letter-spacing: -0.05em; user-select: none; }

.profile-strip { display: flex; align-items: center; gap: 1rem; padding: 0.85rem 1.4rem; border-radius: 14px; background: rgba(99,102,241,0.07); border: 1px solid rgba(99,102,241,0.18); margin-bottom: 1.2rem; position: relative; overflow: hidden; }
.profile-strip::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: linear-gradient(180deg, #6366f1, #a78bfa); border-radius: 3px 0 0 3px; }
.profile-icon { font-size: 1.4rem; }
.profile-name { font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 700; color: #c4b5fd; }
.profile-desc { font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; color: rgba(196,181,253,0.55); }
.profile-right { margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: rgba(99,102,241,0.45); letter-spacing: 0.1em; text-transform: uppercase; }

.card { border-radius: 18px; padding: 1.2rem 1.3rem; background: rgba(255,255,255,0.022); border: 1px solid rgba(255,255,255,0.07); position: relative; overflow: hidden; height: 100%; }
.card-glow-cyan::before  { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(0,212,255,0.5), transparent); }
.card-glow-amber::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(245,158,11,0.55), transparent); }
.card-glow-violet::before{ content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(139,92,246,0.55), transparent); }
.card-glow-green::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(16,185,129,0.5), transparent); }
.card-glow-pink::before  { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(236,72,153,0.5), transparent); }
.card-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(226,232,240,0.3); margin-bottom: 0.9rem; display: flex; align-items: center; gap: 8px; }
.card-label::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.05); }

.hab-score-wrap { text-align: center; padding: 0.3rem 0; }
.hab-number { font-family: 'Outfit', sans-serif; font-size: 4rem; font-weight: 900; line-height: 1; letter-spacing: -0.03em; }
.hab-denom { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 300; color: rgba(226,232,240,0.25); }
.hab-label { font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; padding: 3px 13px; border-radius: 999px; display: inline-block; margin-top: 0.4rem; }
.lab-good   { background: rgba(16,185,129,0.13); color: #34d399; border: 1px solid rgba(16,185,129,0.28); }
.lab-medium { background: rgba(245,158,11,0.13); color: #fbbf24; border: 1px solid rgba(245,158,11,0.28); }
.lab-poor   { background: rgba(239,68,68,0.13);  color: #f87171; border: 1px solid rgba(239,68,68,0.28);  }

.mini-metric { border-radius: 14px; padding: 1.1rem 1.2rem; background: rgba(255,255,255,0.022); border: 1px solid rgba(255,255,255,0.065); position: relative; overflow: hidden; }
.mini-metric-name { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(226,232,240,0.3); margin-bottom: 0.35rem; }
.mini-metric-val  { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; line-height: 1; letter-spacing: -0.02em; }
.mini-metric-lbl  { font-family: 'Space Grotesk', sans-serif; font-size: 0.68rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.35rem; }
.mini-bar-track   { height: 2px; border-radius: 1px; background: rgba(255,255,255,0.05); margin-top: 0.7rem; overflow: hidden; }
.mini-bar-fill    { height: 100%; border-radius: 1px; }

.rec-general { font-family: 'Outfit', sans-serif; font-size: 0.9rem; font-weight: 300; color: rgba(226,232,240,0.7); line-height: 1.6; padding: 0.9rem 1.1rem; border-radius: 10px; background: rgba(0,212,255,0.04); border-left: 2px solid rgba(0,212,255,0.35); margin-bottom: 0.7rem; }
.rec-item { font-family: 'Space Grotesk', sans-serif; font-size: 0.84rem; font-weight: 400; color: rgba(226,232,240,0.75); line-height: 1.5; padding: 0.7rem 0.9rem 0.7rem 1rem; border-radius: 9px; background: rgba(245,158,11,0.04); border-left: 2px solid rgba(245,158,11,0.35); margin-bottom: 0.45rem; }

.hist-row { display: flex; align-items: center; gap: 0.7rem; padding: 0.55rem 0.8rem; border-radius: 8px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); margin-bottom: 0.4rem; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; }
.hist-idx { color: rgba(226,232,240,0.2); width: 14px; }
.hist-score { font-weight: 700; min-width: 40px; }
.hist-bar { flex: 1; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.05); overflow: hidden; }
.hist-bar-fill { height: 100%; border-radius: 2px; }
.hist-trend { font-size: 0.8rem; min-width: 16px; text-align: right; }
.hist-label { color: rgba(226,232,240,0.3); font-size: 0.68rem; min-width: 60px; text-align: right; }

.cmp-row { display: flex; align-items: center; gap: 0.6rem; padding: 0.55rem 0.8rem; border-radius: 8px; margin-bottom: 0.35rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); }
.cmp-profile { font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; font-weight: 600; min-width: 130px; }
.cmp-score   { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 700; min-width: 44px; }
.cmp-bar     { flex: 1; height: 5px; border-radius: 3px; background: rgba(255,255,255,0.05); overflow: hidden; }
.cmp-bar-fill{ height: 100%; border-radius: 3px; }
.cmp-you     { background: rgba(0,212,255,0.08) !important; border-color: rgba(0,212,255,0.2) !important; }
.cmp-you .cmp-profile { color: #00d4ff !important; }

.rule-item { display: flex; align-items: flex-start; gap: 0.6rem; padding: 0.5rem 0.8rem; border-radius: 8px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); margin-bottom: 0.35rem; font-family: 'Space Grotesk', sans-serif; font-size: 0.8rem; color: rgba(226,232,240,0.65); line-height: 1.4; }
.rule-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; margin-top: 0.35rem; }

.section-label { font-family: 'JetBrains Mono', monospace; font-size: 0.63rem; font-weight: 500; color: rgba(0,212,255,0.55); letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.8rem; padding-bottom: 0.6rem; border-bottom: 1px solid rgba(0,212,255,0.1); }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.15); border-radius: 2px; }

.stSlider > div { padding-top: 0 !important; }
.stDivider { border-color: rgba(255,255,255,0.05) !important; }
.streamlit-expanderHeader { font-family: 'Space Grotesk', sans-serif !important; font-size: 0.82rem !important; color: rgba(226,232,240,0.35) !important; }
div[data-testid="stMetricValue"] { color: #f8fafc; }
div[data-testid="stMetricLabel"] { color: #cbd5e1; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE — History
# ============================================================
if "history" not in st.session_state:
    st.session_state.history = []  # list of {inputs, outputs}

# ============================================================
# HELPERS
# ============================================================
def _ui_tier(val: float, invert: bool = False) -> str:
    """
    Derive the UI display tier from fuzzy MFs.
    Uses Maximum Membership Principle (Zadeh, 1965).

    5 tiers mapped from 5 MF terms:
      High        → very_good
      Medium High → good
      Medium      → moderate
      Low         → poor
      Very Low    → very_poor

    For DigitalOverload (invert=True) semantics are reversed:
      Very Low overload → very_good  (best case)
      High overload     → very_poor  (worst case)
    """
    from fuzzy_engine import _label_from_mf, focus_quality
    raw = _label_from_mf(val, focus_quality)  # same MF shape for all outputs

    mapping = {
        "High":        "very_good",
        "Medium High": "good",
        "Medium":      "moderate",
        "Low":         "poor",
        "Very Low":    "very_poor",
    }
    mapping_inv = {
        "Very Low":    "very_good",
        "Low":         "good",
        "Medium":      "moderate",
        "Medium High": "poor",
        "High":        "very_poor",
    }
    return (mapping_inv if invert else mapping).get(raw, "moderate")


def score_color(val, invert=False):
    return {
        "very_good": "#34d399",
        "good":      "#86efac",
        "moderate":  "#fbbf24",
        "poor":      "#f97316",
        "very_poor": "#f87171",
    }[_ui_tier(val, invert)]


def score_label(val, invert=False):
    return {
        "very_good": ("Very Good", "lab-good"),
        "good":      ("Good",      "lab-good"),
        "moderate":  ("Moderate",  "lab-medium"),
        "poor":      ("Poor",      "lab-poor"),
        "very_poor": ("Very Poor", "lab-poor"),
    }[_ui_tier(val, invert)]

def zone_tag(val, lo, hi):
    if val <= lo:  return "Low",    "zone-low"
    if val <= hi:  return "Medium", "zone-medium"
    return "High", "zone-high"

def _mu_input(var_name: str, term: str, value: float) -> float:
    """Compute membership degree for a raw input value """
    import skfuzzy as fuzz
    import fuzzy_engine as _eng
    var = getattr(_eng, var_name)
    return float(fuzz.interp_membership(var.universe, var[term].mf, value))


def detect_profile(sg, ic, ln, sm):
    """
    Detect user profile using fuzzy membership degrees.
    Each profile corresponds to a dominant pattern in the input MF space.
    """
    mu_ln_high = _mu_input("late_night_use", "high",   ln)
    mu_sm_high = _mu_input("social_media",   "high",   sm)
    mu_sg_high = _mu_input("screen_glances", "high",   sg)
    mu_ic_high = _mu_input("idle_checking",  "high",   ic)
    mu_sg_low  = _mu_input("screen_glances", "low",    sg)
    mu_sm_low  = _mu_input("social_media",   "low",    sm)
    mu_ln_low  = _mu_input("late_night_use", "low",    ln)
    mu_ic_low  = _mu_input("idle_checking",  "low",    ic)

    if mu_ln_high > 0.4 and mu_sm_high > 0.4:
        return "🌙", "Night Owl", "High late-night + dominant social media"
    if mu_sg_high > 0.4 and mu_ic_high > 0.4:
        return "📲", "Distracted Achiever", "High screen glances + compulsive idle checking"
    if mu_sg_low > 0.5 and mu_ic_low > 0.5 and mu_ln_low > 0.5 and mu_sm_low > 0.5:
        return "⚖️", "Balanced User", "Low across all — intentional use"
    if mu_sg_low > 0.4 and mu_sm_low > 0.5:
        return "📚", "Focused Worker", "Low glances + low social media"
    return "🔀", "Mixed Profile", "Combination of overlapping behaviour patterns"


def specific_recs(sg, ic, ln, sm):
    """
    Sidebar warnings derived from input MF membership degrees.
    """
    recs = []
    if _mu_input("late_night_use", "high", ln) > 0.3:
        recs.append(f"🌙 <b>LateNightUse = {ln} min</b> — Enable bedtime mode after 22:00 and stop scrolling 30 min before sleep.")
    if _mu_input("idle_checking",  "high", ic) > 0.3:
        recs.append(f"⏳ <b>IdleChecking = {ic}/day</b> — Keep your phone out of reach during study breaks and idle moments.")
    if _mu_input("screen_glances", "high", sg) > 0.3:
        recs.append(f"👁 <b>ScreenGlances = {sg}/day</b> — Disable non-essential notifications to reduce automatic unlocking.")
    if _mu_input("social_media",   "high", sm) > 0.3:
        recs.append(f"📱 <b>SocialMedia = {sm}%</b> — Set fixed time windows for social apps instead of checking continuously.")
    # Medium late-night use — gentle nudge before it becomes high
    if _mu_input("late_night_use", "medium", ln) > 0.4 and _mu_input("late_night_use", "high", ln) <= 0.3:
        recs.append(f"🛏 <b>LateNightUse = {ln} min</b> — Try reducing by 10 minutes each evening. Small reductions are easier to sustain than sudden curfews.")

    # Medium social media — passive scrolling warning
    if _mu_input("social_media", "medium", sm) > 0.4 and _mu_input("social_media", "high", sm) <= 0.3:
        recs.append(f"📲 <b>SocialMedia = {sm}%</b> — Use apps with a clear purpose, not as default boredom relief. Passive scrolling drives most of the negative wellbeing effect.")

    # Screen glances + idle checking both elevated — combined fragmentation
    if _mu_input("screen_glances", "high", sg) > 0.2 and _mu_input("idle_checking", "high", ic) > 0.2:
        recs.append(f"🔁 <b>ScreenGlances + IdleChecking both elevated</b> — Create phone-free zones in your workspace and at the dining table to break the checking loop.")

    # Late night + social media combined — the worst sleep disruptor pattern
    if _mu_input("late_night_use", "high", ln) > 0.2 and _mu_input("social_media", "high", sm) > 0.2:
        recs.append(f"😴 <b>Late-night social media detected</b> — Switch off devices at least 1 hour before bed and replace the habit with an offline wind-down activity like reading or light stretching.")

    # Medium screen glances — worth scheduling intentional checks
    if _mu_input("screen_glances", "medium", sg) > 0.4 and _mu_input("screen_glances", "high", sg) <= 0.3:
        recs.append(f"⏱ <b>ScreenGlances = {sg}/day</b> — Schedule device-free periods of 90 minutes during your day. Checking less frequently reduces stress even when overall use feels moderate.")

    # Positive reinforcement when all inputs are genuinely low
    mu_all_low = min(
        _mu_input("screen_glances", "low", sg),
        _mu_input("idle_checking",  "low", ic),
        _mu_input("late_night_use", "low", ln),
        _mu_input("social_media",   "low", sm),
    )
    if mu_all_low > 0.3:
        recs.append("🌿 <b>All habits in the low zone.</b> Keep one daily phone-free moment — a meal, a walk, or a morning routine — to protect this balance long-term.")

    if not recs:
        recs.append("✅ <b>All habits look balanced.</b> Maintain intentional phone use and avoid notification creep.")
    return recs

def gauge_svg(score, color, size=195):
    pct   = score / 10.0
    angle = pct * 180
    rad   = math.radians(180 - angle)
    cx, cy = size/2, size * 0.60
    r = size * 0.36
    ex = cx + r * math.cos(rad); ey = cy - r * math.sin(rad)
    laf = 1 if angle > 180 else 0
    tx1, ty1 = cx - r, cy; tx2, ty2 = cx + r, cy
    nx = cx + (r * 0.70) * math.cos(rad); ny = cy - (r * 0.70) * math.sin(rad)
    sw = int(size * 0.09); h = int(size * 0.66)
    ticks = "".join([
        f'<line x1="{cx + (r+sw//2+2)*math.cos(math.radians(180-i*18)):.1f}" y1="{cy-(r+sw//2+2)*math.sin(math.radians(180-i*18)):.1f}" x2="{cx+(r+sw//2+6)*math.cos(math.radians(180-i*18)):.1f}" y2="{cy-(r+sw//2+6)*math.sin(math.radians(180-i*18)):.1f}" stroke="#cbd5e1" stroke-width="1.2" stroke-linecap="round"/>'
        for i in range(11)])
    # Target zone indicator (>6.5 = green zone)
    tgt_rad1 = math.radians(180 - 6.5*18); tgt_rad2 = math.radians(180 - 10*18)
    tx_1 = cx + r*math.cos(tgt_rad1); ty_1 = cy - r*math.sin(tgt_rad1)
    tx_2 = cx + r*math.cos(tgt_rad2); ty_2 = cy - r*math.sin(tgt_rad2)
    return f"""<svg width="{size}" height="{h}" viewBox="0 0 {size} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="g1"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="arcGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#ef4444"/>
      <stop offset="35%" style="stop-color:#f97316"/>
      <stop offset="60%" style="stop-color:#eab308"/>
      <stop offset="80%" style="stop-color:#84cc16"/>
      <stop offset="100%" style="stop-color:#22c55e"/>
    </linearGradient>
  </defs>
  <path d="M {tx1},{ty1} A {r},{r} 0 0,1 {tx2},{ty2}" fill="none" stroke="#e2e8f0" stroke-width="{sw}" stroke-linecap="round"/>
  <path d="M {tx_1:.1f},{ty_1:.1f} A {r},{r} 0 0,1 {tx_2:.1f},{ty_2:.1f}" fill="none" stroke="rgba(34,197,94,0.15)" stroke-width="{sw}" stroke-linecap="butt"/>
  <path d="M {tx1},{ty1} A {r},{r} 0 {laf},1 {ex:.1f},{ey:.1f}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" opacity="0.9"/>
  {ticks}
  <line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#e2e8f0" stroke-width="{int(size*0.034)}" stroke-linecap="round"/>
  <line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="rgba(226,232,240,0.75)" stroke-width="{int(size*0.02)}" stroke-linecap="round" opacity="0.85"/>
  <circle cx="{cx}" cy="{cy}" r="{int(size*0.048)}" fill="white" stroke="#e2e8f0" stroke-width="1.5"/>
  <circle cx="{cx}" cy="{cy}" r="{int(size*0.022)}" fill="{color}" opacity="0.9"/>
  <text x="{tx1-5}" y="{ty1+14}" fill="rgba(226,232,240,0.3)" font-size="9" font-family="JetBrains Mono,monospace">0</text>
  <text x="{cx-4}" y="{cy-r-sw//2-8}" fill="rgba(226,232,240,0.3)" font-size="9" font-family="JetBrains Mono,monospace">5</text>
  <text x="{tx2-12}" y="{ty2+14}" fill="rgba(226,232,240,0.3)" font-size="9" font-family="JetBrains Mono,monospace">10</text>
</svg>"""

def radar_svg(focus, sleep, overload, habit, size=230):
    cx, cy = size/2, size/2; r_max = size*0.34
    labels = ["Focus","Sleep","Balance","Not\nOverloaded"]
    values = [focus/10, sleep/10, habit/10, (10-overload)/10]
    angles = [90, 0, 270, 180]
    clrs   = [score_color(focus), score_color(sleep), score_color(habit), score_color(overload, invert=True)]
    grid = ""
    for lvl in [0.25,0.5,0.75,1.0]:
        pts = []
        for a in angles:
            rd = math.radians(a)
            pts.append((cx+r_max*lvl*math.cos(rd), cy-r_max*lvl*math.sin(rd)))
        poly = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
        op = 0.04 + lvl*0.05
        grid += f'<polygon points="{poly}" fill="rgba(99,102,241,{op:.2f})" stroke="rgba(99,102,241,{op*2:.2f})" stroke-width="0.8"/>'
    axes = ""
    for a in angles:
        rd = math.radians(a)
        axes += f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx+r_max*math.cos(rd):.1f}" y2="{cy-r_max*math.sin(rd):.1f}" stroke="#e2e8f0" stroke-width="1"/>'
    pts_d = []
    for val, a in zip(values, angles):
        rd = math.radians(a); pts_d.append((cx+r_max*val*math.cos(rd), cy-r_max*val*math.sin(rd)))
    poly_d = " ".join(f"{x:.1f},{y:.1f}" for x,y in pts_d)
    data_shape = f'<polygon points="{poly_d}" fill="rgba(99,102,241,0.08)" stroke="rgba(99,102,241,0.6)" stroke-width="1.8"/>'
    dots = ""; label_els = ""
    for (x,y),lbl,col,val,a in zip(pts_d,labels,clrs,values,angles):
        dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{col}" opacity="0.12"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{col}" opacity="0.9"/>'
        rd = math.radians(a); lx = cx+(r_max+25)*math.cos(rd); ly = cy-(r_max+25)*math.sin(rd)
        anchor = "middle"
        if a == 0: anchor,lx = "start",lx+2
        if a == 180: anchor,lx = "end",lx-2
        for i,line in enumerate(lbl.split("\n")):
            label_els += f'<text x="{lx:.1f}" y="{ly+i*12:.1f}" fill="rgba(99,102,241,0.38)" font-size="10" font-family="Inter,sans-serif" text-anchor="{anchor}" font-weight="500">{line}</text>'
        vx = cx+(r_max*val+18)*math.cos(rd); vy = cy-(r_max*val+18)*math.sin(rd)
        label_els += f'<text x="{vx:.1f}" y="{vy+4:.1f}" fill="{col}" font-size="11" font-weight="700" font-family="JetBrains Mono,monospace" text-anchor="middle">{val*10:.1f}</text>'
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">{grid}{axes}{data_shape}{dots}{label_els}</svg>"""

def sparkline_svg(values, width=200, height=40):
    if len(values) < 2: return ""
    mn, mx = min(values), max(values)
    rng = mx - mn if mx > mn else 1
    pts = []
    for i, v in enumerate(values):
        x = 8 + (i / (len(values)-1)) * (width-16)
        y = height - 8 - ((v - mn) / rng) * (height-16)
        pts.append((x, y))
    path = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    fill_path = path + f" L {pts[-1][0]:.1f},{height} L {pts[0][0]:.1f},{height} Z"
    last_col = score_color(values[-1])
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{last_col}" opacity="0.7"/>' for x,y in pts)
    return f"""<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{last_col}" stop-opacity="0.2"/><stop offset="100%" stop-color="{last_col}" stop-opacity="0"/></linearGradient></defs>
  <path d="{fill_path}" fill="url(#sg)"/>
  <path d="{path}" fill="none" stroke="{last_col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>
  {dots}
</svg>"""

MF = {"ScreenGlances":(40,65),"IdleChecking":(20,40),"LateNightUse":(30,60),"SocialMediaUsage":(25,40)}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">◈ fuzzy-detox · inputs</div>', unsafe_allow_html=True)
    sliders = [
        ("ScreenGlances","Screen Glances",0,150,50,1,"Phone unlocks / day"),
        ("IdleChecking","Idle Checking",0,80,20,1,"Habitual short checks / day"),
        ("LateNightUse","Late Night Use",0,120,30,1,"Minutes of use before bedtime"),
        ("SocialMediaUsage","Social Media %",0,100,40,1,"% of total screen time"),
    ]
    vals = {}
    for key,label,mn,mx,default,step,hint in sliders:
        col_sl, col_num = st.columns([3,1])
        with col_sl:
            val = st.slider(label, mn, mx, default, step, help=hint, label_visibility="visible")
        with col_num:
            st.markdown(f'<div style="font-family:JetBrains Mono,monospace;font-size:0.85rem;color:rgba(226,232,240,0.6);padding-top:1.8rem;text-align:center">{val}</div>', unsafe_allow_html=True)
        z_name, z_cls = zone_tag(val, *MF[key])
        st.markdown(f'<div class="zone-tag {z_cls}">◆ {z_name}</div>', unsafe_allow_html=True)
        vals[key] = val

    st.divider()

    st.divider()
    st.markdown('<div class="sidebar-brand" style="margin-top:0">◈ session history</div>', unsafe_allow_html=True)
    if st.button("📸 Save this reading", use_container_width=True):
        st.session_state.history.append(dict(vals))
        if len(st.session_state.history) > 8:
            st.session_state.history = st.session_state.history[-8:]
    if st.button("🗑 Clear history", use_container_width=True):
        st.session_state.history = []

# ============================================================
# EVALUATE
# ============================================================
result = evaluate_fuzzy_system(
    screen_glances_value=vals["ScreenGlances"],
    idle_checking_value=vals["IdleChecking"],
    late_night_use_value=vals["LateNightUse"],
    social_media_value=vals["SocialMediaUsage"],
)
o = result["outputs"]
focus, sleep, overload, habit = o["FocusQuality"], o["SleepQuality"], o["DigitalOverload"], o["HabitBalance"]

hab_col = score_color(habit)
hab_lbl, hab_cls = score_label(habit)
p_icon, p_name, p_desc = detect_profile(vals["ScreenGlances"], vals["IdleChecking"], vals["LateNightUse"], vals["SocialMediaUsage"])
recs = specific_recs(vals["ScreenGlances"], vals["IdleChecking"], vals["LateNightUse"], vals["SocialMediaUsage"])

# Profile comparison data
PROFILE_BENCHMARKS = [
    ("⚖️ Balanced User",       {"ScreenGlances":25,"IdleChecking":10,"LateNightUse":10,"SocialMediaUsage":20}),
    ("📚 Focused Worker",      {"ScreenGlances":30,"IdleChecking":8, "LateNightUse":35,"SocialMediaUsage":18}),
    ("🌙 Night Owl",           {"ScreenGlances":60,"IdleChecking":28,"LateNightUse":110,"SocialMediaUsage":70}),
    ("📲 Distracted Achiever", {"ScreenGlances":98,"IdleChecking":50,"LateNightUse":45,"SocialMediaUsage":68}),
]
cmp_results = []
for pname, pinputs in PROFILE_BENCHMARKS:
    pr = evaluate_fuzzy_system(
        screen_glances_value=pinputs["ScreenGlances"],
        idle_checking_value=pinputs["IdleChecking"],
        late_night_use_value=pinputs["LateNightUse"],
        social_media_value=pinputs["SocialMediaUsage"],
    )
    cmp_results.append((pname, pr["outputs"]["HabitBalance"]))

# History scores
hist_scores = []
for h in st.session_state.history:
    hr = evaluate_fuzzy_system(
        screen_glances_value=h["ScreenGlances"],
        idle_checking_value=h["IdleChecking"],
        late_night_use_value=h["LateNightUse"],
        social_media_value=h["SocialMediaUsage"],
    )
    hist_scores.append(hr["outputs"]["HabitBalance"])

# ============================================================
# HERO
# ============================================================
st.markdown(f"""
<div class="hero-wrapper">
    <div class="hero-eyebrow">Mamdani Fuzzy Inference System</div>
    <div class="hero-title">Digital Habit <span>Balance</span></div>
    <div class="hero-sub">Real-time fuzzy analysis of your digital wellbeing..</div>
    <div class="hero-corner">FIS</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="profile-strip">
    <div class="profile-icon">{p_icon}</div>
    <div><div class="profile-name">{p_name}</div><div class="profile-desc">{p_desc}</div></div>
    <div class="profile-right">Profile detected ↗</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ROW 1 — Gauge · Radar · Recommendations
# ============================================================
c1, c2, c3 = st.columns([1, 1.15, 1.3], gap="small")

with c1:
    g_svg = gauge_svg(habit, hab_col, size=195)
    st.markdown(f'''
    <div class="card card-glow-cyan">
        <div class="card-label">Habit Balance Score</div>
        <div style="display:flex;justify-content:center">{g_svg}</div>
        <div class="hab-score-wrap">
            <span class="hab-number" style="color:{hab_col}">{habit:.2f}</span>
            <span class="hab-denom">/10</span><br>
            <span class="hab-label {hab_cls}">{hab_lbl}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with c2:
    r_svg = radar_svg(focus, sleep, overload, habit, size=230)
    st.markdown(f'''
    <div class="card card-glow-violet">
        <div class="card-label">Output Profile Radar</div>
        <div style="display:flex;justify-content:center">{r_svg}</div>
    </div>
    ''', unsafe_allow_html=True)

with c3:
    recs_html = "".join(f'<div class="rec-item">{r}</div>' for r in recs)
    st.markdown(f'''
    <div class="card card-glow-amber">
        <div class="card-label">Recommendations</div>
        <div class="rec-general">{result["recommendation"]}</div>
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:rgba(245,158,11,0.45);margin:0.7rem 0 0.4rem">Actions to take right now:</div>
        {recs_html}
    </div>
    ''', unsafe_allow_html=True)

# ============================================================
# ROW 2 — Metric cards
# ============================================================
st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4, gap="small")

def mini_card(col, name, val, invert=False, note=""):
    col_hex = score_color(val, invert)
    lbl, _  = score_label(val, invert)
    bar_w   = int(((10-val) if invert else val) / 10 * 100)
    col.markdown(f"""
    <div class="mini-metric">
        <div class="mini-metric-name">{name}{note}</div>
        <div class="mini-metric-val" style="color:{col_hex}">{val:.2f}</div>
        <div class="mini-metric-lbl" style="color:{col_hex}">{lbl}</div>
        <div class="mini-bar-track"><div class="mini-bar-fill" style="width:{bar_w}%;background:{col_hex};opacity:0.75"></div></div>
    </div>
    """, unsafe_allow_html=True)

mini_card(m1, "Focus Quality",   focus,   False)
mini_card(m2, "Sleep Quality",   sleep,   False)
mini_card(m3, "Digital Overload",overload, True, " ↓")
mini_card(m4, "Habit Balance",   habit,   False)

# ============================================================
# ROW 3 — History · Comparison · Rule Breakdown
# ============================================================
st.markdown('<div style="height:0.8rem"></div>', unsafe_allow_html=True)
r3a, r3b, r3c = st.columns([1, 1, 1.2], gap="small")

# History
with r3a:
    if hist_scores:
        spark = sparkline_svg(hist_scores, width=220, height=44)
        hist_html = f'<div style="display:flex;justify-content:center;margin-bottom:0.5rem">{spark}</div>'
        trend_val = hist_scores[-1] - hist_scores[-2] if len(hist_scores) >= 2 else 0
        trend_sym = "↑" if trend_val > 0.1 else "↓" if trend_val < -0.1 else "→"
        trend_col = "#34d399" if trend_val > 0.1 else "#f87171" if trend_val < -0.1 else "#fbbf24"
        rows = ""
        for i, sc in enumerate(reversed(hist_scores[-5:])):
            idx = len(hist_scores) - i
            col_h = score_color(sc)
            lbl_h, _ = score_label(sc)
            w = int(sc/10*100)
            rows += f'<div class="hist-row"><span class="hist-idx">#{idx}</span><span class="hist-score" style="color:{col_h}">{sc:.2f}</span><div class="hist-bar"><div class="hist-bar-fill" style="width:{w}%;background:{col_h};opacity:0.7"></div></div><span style="color:{col_h};font-size:0.72rem">{lbl_h}</span></div>'
        st.markdown(f'''
        <div class="card card-glow-green">
            <div class="card-label">Session History</div>
            {hist_html}
            <div style="font-family:JetBrains Mono,monospace;font-size:0.68rem;color:{trend_col};margin-bottom:0.5rem">Trend: {trend_sym} {abs(trend_val):.2f} from last reading</div>
            {rows}
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="card card-glow-green">
            <div class="card-label">Session History</div>
            <div style="text-align:center;padding:2rem 0;font-family:Space Grotesk,sans-serif;font-size:0.85rem;color:rgba(226,232,240,0.3)">
                <div style="font-size:2rem;margin-bottom:0.5rem">📸</div>
                No readings saved yet.<br>Use the sidebar button to save this reading.
            </div>
        </div>
        ''', unsafe_allow_html=True)

# Profile comparison
with r3b:
    rows = ""
    you_added = False
    all_scores = [(pname, sc) for pname, sc in cmp_results] + [("🫵 You", habit)]
    all_scores_sorted = sorted(all_scores, key=lambda x: -x[1])
    for pname, sc in all_scores_sorted:
        col_c = score_color(sc)
        w = int(sc/10*100)
        is_you = pname == "🫵 You"
        extra = 'cmp-you' if is_you else ''
        rows += f'<div class="cmp-row {extra}"><span class="cmp-profile" style="color:{"#00d4ff" if is_you else "rgba(226,232,240,0.65)"}">{pname}</span><span class="cmp-score" style="color:{col_c}">{sc:.2f}</span><div class="cmp-bar"><div class="cmp-bar-fill" style="width:{w}%;background:{col_c};opacity:0.75"></div></div></div>'
    st.markdown(f'''
    <div class="card card-glow-violet">
        <div class="card-label">Profile Comparison</div>
        <div style="font-family:Space Grotesk,sans-serif;font-size:0.78rem;color:rgba(226,232,240,0.3);margin-bottom:0.7rem">HabitBalance ranked against all 4 archetypes</div>
        {rows}
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:rgba(0,212,255,0.55);margin-top:0.7rem;letter-spacing:0.08em">◈ your score highlighted</div>
    </div>
    ''', unsafe_allow_html=True)

# Rule breakdown
with r3c:
    rules_fired = []
    sg, ic, ln, sm = vals["ScreenGlances"], vals["IdleChecking"], vals["LateNightUse"], vals["SocialMediaUsage"]

    # Compute membership degrees for all inputs — the real fuzzy activations
    mu_sg_h = _mu_input("screen_glances", "high",   sg)
    mu_sg_m = _mu_input("screen_glances", "medium", sg)
    mu_sg_l = _mu_input("screen_glances", "low",    sg)
    mu_ic_h = _mu_input("idle_checking",  "high",   ic)
    mu_ic_l = _mu_input("idle_checking",  "low",    ic)
    mu_ln_h = _mu_input("late_night_use", "high",   ln)
    mu_ln_l = _mu_input("late_night_use", "low",    ln)
    mu_sm_h = _mu_input("social_media",   "high",   sm)
    mu_sm_l = _mu_input("social_media",   "low",    sm)

    # Focus rules — fire when activation > 0.1
    if mu_sg_h > 0.1: rules_fired.append(("focus",f"IF ScreenGlances IS High (μ={mu_sg_h:.2f}) → FocusQuality IS Low","#fbbf24"))
    if mu_ln_h > 0.1: rules_fired.append(("focus",f"IF LateNightUse IS High (μ={mu_ln_h:.2f}) → FocusQuality IS Low","#fbbf24"))
    if mu_ic_h > 0.1 and mu_sg_h > 0.1: rules_fired.append(("focus",f"IF IdleChecking IS High (μ={mu_ic_h:.2f}) AND ScreenGlances IS High (μ={mu_sg_h:.2f}) → FocusQuality IS Very Low","#f87171"))
    elif mu_ic_h > 0.1: rules_fired.append(("focus",f"IF IdleChecking IS High (μ={mu_ic_h:.2f}) → FocusQuality IS Low","#fbbf24"))
    if mu_sm_h > 0.1: rules_fired.append(("focus",f"IF SocialMedia IS High (μ={mu_sm_h:.2f}) → FocusQuality IS Low","#fbbf24"))
    if mu_sg_l > 0.5 and mu_sm_l > 0.5: rules_fired.append(("focus",f"IF ScreenGlances IS Low (μ={mu_sg_l:.2f}) AND SocialMedia IS Low (μ={mu_sm_l:.2f}) → FocusQuality IS High","#34d399"))
    if mu_sg_m > 0.3 and mu_ln_l > 0.5: rules_fired.append(("focus",f"IF ScreenGlances IS Medium (μ={mu_sg_m:.2f}) AND LateNightUse IS Low (μ={mu_ln_l:.2f}) → FocusQuality IS Medium High","#34d399"))

    # Sleep rules
    if mu_ln_h > 0.1 and mu_sm_h > 0.1: rules_fired.append(("sleep",f"IF LateNightUse IS High (μ={mu_ln_h:.2f}) AND SocialMedia IS High (μ={mu_sm_h:.2f}) → SleepQuality IS Very Low","#f87171"))
    if mu_ln_h > 0.1 and mu_sg_h > 0.1: rules_fired.append(("sleep",f"IF LateNightUse IS High (μ={mu_ln_h:.2f}) AND ScreenGlances IS High (μ={mu_sg_h:.2f}) → SleepQuality IS Very Low","#f87171"))
    if mu_ln_l > 0.5 and mu_sg_l > 0.5 and mu_ic_l > 0.5: rules_fired.append(("sleep",f"IF LateNightUse IS Low (μ={mu_ln_l:.2f}) AND ScreenGlances IS Low (μ={mu_sg_l:.2f}) AND IdleChecking IS Low (μ={mu_ic_l:.2f}) → SleepQuality IS High","#34d399"))

    # Overload rules
    if mu_sg_h > 0.1 and mu_sm_h > 0.1: rules_fired.append(("overload",f"IF ScreenGlances IS High (μ={mu_sg_h:.2f}) AND SocialMedia IS High (μ={mu_sm_h:.2f}) → DigitalOverload IS High","#f87171"))
    if mu_ic_h > 0.1 and mu_sm_h > 0.1: rules_fired.append(("overload",f"IF IdleChecking IS High (μ={mu_ic_h:.2f}) AND SocialMedia IS High (μ={mu_sm_h:.2f}) → DigitalOverload IS High","#f87171"))
    if mu_sm_h > 0.1 and mu_sg_l > 0.5 and mu_ln_l > 0.5: rules_fired.append(("overload",f"IF SocialMedia IS High (μ={mu_sm_h:.2f}) AND Glances IS Low (μ={mu_sg_l:.2f}) → DigitalOverload IS Medium","#fbbf24"))
    if mu_sg_l > 0.5 and mu_sm_l > 0.5: rules_fired.append(("overload",f"IF ScreenGlances IS Low (μ={mu_sg_l:.2f}) AND SocialMedia IS Low (μ={mu_sm_l:.2f}) → DigitalOverload IS Very Low","#34d399"))

    if not rules_fired:
        rules_fired.append(("mixed","Values in overlap zones — multiple rules firing with moderate activation","#fbbf24"))

    type_labels = {"focus":"FQ","sleep":"SQ","overload":"DO","mixed":"MX"}
    type_colors = {"focus":"rgba(96,165,250,0.6)","sleep":"rgba(139,92,246,0.6)","overload":"rgba(239,68,68,0.6)","mixed":"rgba(245,158,11,0.6)"}
    rules_html = ""
    for rtype, rdesc, rcol in rules_fired[:7]:
        tc = type_colors.get(rtype,"rgba(226,232,240,0.3)")
        tl = type_labels.get(rtype,"?")
        rules_html += f'<div class="rule-item"><span style="background:{tc};color:white;font-family:JetBrains Mono,monospace;font-size:0.6rem;font-weight:700;padding:1px 6px;border-radius:4px;flex-shrink:0">{tl}</span><div class="rule-dot" style="background:{rcol};flex-shrink:0"></div>{rdesc}</div>'

    st.markdown(f'''
    <div class="card card-glow-pink">
        <div class="card-label">Active Fuzzy Rules</div>
        <div style="font-family:Space Grotesk,sans-serif;font-size:0.78rem;color:rgba(226,232,240,0.3);margin-bottom:0.7rem">Rules currently firing based on your inputs</div>
        {rules_html}
        <div style="font-family:JetBrains Mono,monospace;font-size:0.6rem;color:rgba(226,232,240,0.3);margin-top:0.6rem;letter-spacing:0.06em">FQ = FocusQuality · SQ = SleepQuality · DO = DigitalOverload</div>
    </div>
    ''', unsafe_allow_html=True)

# ============================================================
# MEMBERSHIP FUNCTION VISUALISATION
# ============================================================
st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'JetBrains Mono',monospace;font-size:0.63rem;font-weight:500;
color:rgba(0,212,255,0.55);letter-spacing:0.2em;text-transform:uppercase;
margin-bottom:0.8rem;padding-bottom:0.6rem;border-bottom:1px solid rgba(0,212,255,0.1)">
◈ fuzzy reasoning — membership functions
</div>""", unsafe_allow_html=True)

try:
    from mf_viz import make_input_mf_figure, make_output_mf_figure, make_hierarchy_figure

    with st.expander("↗ Input membership functions — where do your values fall?", expanded=True):
        st.markdown(
            "<p style='font-size:0.78rem;color:rgba(226,232,240,0.45);margin-bottom:0.6rem'>"
            "The dashed cyan line shows your current input value inside each membership function. "
            "Where it lands determines the fuzzy label (Low / Medium / High) and with what degree (0–1)."
            "</p>", unsafe_allow_html=True)
        fig_in = make_input_mf_figure(
            vals["ScreenGlances"], vals["IdleChecking"],
            vals["LateNightUse"], vals["SocialMediaUsage"]
        )
        st.pyplot(fig_in, use_container_width=True)
        plt.close(fig_in)

    with st.expander("↗ Output membership functions — how are scores computed?", expanded=True):
        st.markdown(
            "<p style='font-size:0.78rem;color:rgba(226,232,240,0.45);margin-bottom:0.6rem'>"
            "After inference, the fuzzy output sets are <b>defuzzified via centroid</b> to produce crisp scores. "
            "HabitBalance is produced by the <b>4th Mamdani FIS</b> — not a formula."
            "</p>", unsafe_allow_html=True)
        fig_out = make_output_mf_figure(
            o["FocusQuality"], o["SleepQuality"],
            o["DigitalOverload"], o["HabitBalance"]
        )
        st.pyplot(fig_out, use_container_width=True)
        plt.close(fig_out)

except Exception as e:
    st.warning(f"MF visualisation unavailable: {e}")

# ============================================================
# EXPANDERS
# ============================================================
st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

with st.expander("↗ Raw fuzzy result (JSON)"):
        st.json(result)

# ============================================================
# FUZZY vs CRISP COMPARISON
# ============================================================
st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'JetBrains Mono',monospace;font-size:0.63rem;font-weight:500;
color:rgba(0,212,255,0.55);letter-spacing:0.2em;text-transform:uppercase;
margin-bottom:0.8rem;padding-bottom:0.6rem;border-bottom:1px solid rgba(0,212,255,0.1)">
◈ evaluation — fuzzy vs crisp comparison
</div>""", unsafe_allow_html=True)

try:
    from comparison_viz import (make_sweep_figure, make_threshold_demo_figure,
                                make_profile_comparison_figure)
    from crisp_engine import evaluate_crisp_system

    cr = evaluate_crisp_system(
        vals["ScreenGlances"], vals["IdleChecking"],
        vals["LateNightUse"],  vals["SocialMediaUsage"]
    )

    # Live side-by-side for current inputs
    diff = round(o["HabitBalance"] - cr["outputs"]["HabitBalance"], 2)
    diff_color = "#34d399" if abs(diff) < 0.5 else "#fbbf24" if abs(diff) < 1.5 else "#f87171"
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin-bottom:0.8rem">
      <div style="flex:1;padding:0.9rem 1.2rem;background:rgba(0,212,255,0.06);
           border:1px solid rgba(0,212,255,0.2);border-radius:12px;text-align:center">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
             color:rgba(0,212,255,0.55);letter-spacing:0.15em;margin-bottom:4px">FUZZY SYSTEM</div>
        <div style="font-size:2rem;font-weight:800;color:#00d4ff">{o["HabitBalance"]}</div>
        <div style="font-size:0.75rem;color:rgba(226,232,240,0.45)">HabitBalance</div>
      </div>
      <div style="flex:1;padding:0.9rem 1.2rem;background:rgba(248,113,113,0.06);
           border:1px solid rgba(248,113,113,0.2);border-radius:12px;text-align:center">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
             color:rgba(248,113,113,0.6);letter-spacing:0.15em;margin-bottom:4px">CRISP SYSTEM</div>
        <div style="font-size:2rem;font-weight:800;color:#f87171">{cr["outputs"]["HabitBalance"]}</div>
        <div style="font-size:0.75rem;color:rgba(226,232,240,0.45)">HabitBalance</div>
      </div>
      <div style="flex:1;padding:0.9rem 1.2rem;background:rgba(255,255,255,0.02);
           border:1px solid rgba(255,255,255,0.05);border-radius:12px;text-align:center">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
             color:{diff_color};letter-spacing:0.15em;margin-bottom:4px">DIFFERENCE</div>
        <div style="font-size:2rem;font-weight:800;color:{diff_color}">{diff:+.2f}</div>
        <div style="font-size:0.75rem;color:rgba(226,232,240,0.45)">Fuzzy − Crisp</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.warning(f"Comparison section unavailable: {e}")

