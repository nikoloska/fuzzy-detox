import pandas as pd
import streamlit as st
from fuzzy_engine import evaluate_fuzzy_system


st.set_page_config(
    page_title="Fuzzy Digital Habit Dashboard",
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# Styling
# ============================================================

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #111827 55%, #1e1b4b 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero-card {
        padding: 2rem;
        border-radius: 28px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        margin-bottom: 1.5rem;
    }

    .eyebrow {
        color: #93c5fd;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.05;
        color: #f8fafc;
        margin-bottom: 0.6rem;
    }

    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1.05rem;
        max-width: 850px;
    }

    .glass-card {
        padding: 1.4rem;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.065);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 18px 60px rgba(0,0,0,0.25);
        height: 100%;
    }

    .score-card {
        text-align: center;
        padding: 1.6rem;
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.075);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    .score-label {
        color: #cbd5e1;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 800;
    }

    .score-value {
        font-size: 3rem;
        font-weight: 900;
        color: #f8fafc;
        margin: 0.4rem 0;
    }

    .score-chip {
        display: inline-block;
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        background: rgba(96, 165, 250, 0.16);
        color: #bfdbfe;
        font-weight: 800;
        font-size: 0.85rem;
    }

    .recommendation {
        padding: 1.3rem 1.5rem;
        border-radius: 22px;
        background: rgba(96, 165, 250, 0.13);
        border: 1px solid rgba(147, 197, 253, 0.26);
        color: #dbeafe;
        font-size: 1.05rem;
        line-height: 1.55;
    }

    .section-title {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 900;
        margin-bottom: 0.8rem;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Header
# ============================================================

st.markdown(
    """
    <div class="hero-card">
        <div class="eyebrow">Mamdani Fuzzy Inference System</div>
        <div class="hero-title">Digital Habit Dashboard</div>
        <div class="hero-subtitle">
            Enter behavior values for screen glances, idle checking, late-night use, and social media usage.
            The Python fuzzy engine calculates Focus Quality, Sleep Quality, Digital Overload, and a final Habit Balance score.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Input sidebar
# ============================================================

with st.sidebar:
    st.header("Input Variables")

    st.caption("All inputs are crisp values. The fuzzy system then maps them to linguistic sets.")

    screen_glances = st.slider(
        "Screen Glances",
        min_value=0,
        max_value=150,
        value=50,
        step=1,
        help="Number of times the user checks or unlocks the phone per day.",
    )

    idle_checking = st.slider(
        "Idle Checking",
        min_value=0,
        max_value=80,
        value=20,
        step=1,
        help="Short, automatic, habitual checks during idle moments.",
    )

    late_night_use = st.slider(
        "Late Night Use",
        min_value=0,
        max_value=180,
        value=30,
        step=1,
        help="Minutes of phone use after 22:00.",
    )

    social_media_usage = st.slider(
        "Social Media Usage",
        min_value=0,
        max_value=100,
        value=40,
        step=1,
        help="Percentage of total screen time spent on social media.",
    )

    st.divider()

    st.write("Current input vector")
    st.json(
        {
            "ScreenGlances": screen_glances,
            "IdleChecking": idle_checking,
            "LateNightUse": late_night_use,
            "SocialMediaUsage": social_media_usage,
        }
    )


# ============================================================
# Evaluate fuzzy system
# ============================================================

result = evaluate_fuzzy_system(
    screen_glances_value=screen_glances,
    idle_checking_value=idle_checking,
    late_night_use_value=late_night_use,
    social_media_value=social_media_usage,
)

outputs = result["outputs"]
labels = result["labels"]


# ============================================================
# Main dashboard
# ============================================================

top_left, top_right = st.columns([1.2, 0.8])

with top_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Fuzzy Output Overview</div>', unsafe_allow_html=True)

    chart_data = pd.DataFrame(
        {
            "Score": [
                outputs["FocusQuality"],
                outputs["SleepQuality"],
                outputs["DigitalOverload"],
                outputs["HabitBalance"],
            ]
        },
        index=[
            "Focus Quality",
            "Sleep Quality",
            "Digital Overload",
            "Habit Balance",
        ],
    )

    st.bar_chart(chart_data, height=340)

    st.markdown("</div>", unsafe_allow_html=True)

with top_right:
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-label">Habit Balance</div>
            <div class="score-value">{outputs["HabitBalance"]:.2f}/10</div>
            <div class="score-chip">{labels["HabitBalance"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        f"""
        <div class="recommendation">
            <strong>Recommendation</strong><br>
            {result["recommendation"]}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.write("")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    st.metric(
        label="Focus Quality",
        value=f'{outputs["FocusQuality"]:.2f}/10',
        delta=labels["FocusQuality"],
    )

with metric_2:
    st.metric(
        label="Sleep Quality",
        value=f'{outputs["SleepQuality"]:.2f}/10',
        delta=labels["SleepQuality"],
    )

with metric_3:
    st.metric(
        label="Digital Overload",
        value=f'{outputs["DigitalOverload"]:.2f}/10',
        delta=labels["DigitalOverload"],
    )

with metric_4:
    st.metric(
        label="Habit Balance",
        value=f'{outputs["HabitBalance"]:.2f}/10',
        delta=labels["HabitBalance"],
    )


# ============================================================
# Explainability section
# ============================================================

st.write("")
with st.expander("Show fuzzy system explanation"):
    st.markdown(
        """
        This app uses a Mamdani fuzzy inference system.

        The crisp input values are fuzzified into linguistic sets such as **Low**, **Medium**, and **High**.
        The rule base then evaluates IF-THEN rules for each output variable.

        The three fuzzy outputs are:

        - **FocusQuality**
        - **SleepQuality**
        - **DigitalOverload**

        Each output is defuzzified using the **centroid method**.

        The final **HabitBalance** is computed as:

        ```text
        HabitBalance = 0.4 * FocusQuality
                     + 0.4 * SleepQuality
                     + 0.2 * (10 - DigitalOverload)
        ```

        DigitalOverload is inverted because a high overload score is negative,
        while high FocusQuality and SleepQuality scores are positive.
        """
    )

with st.expander("Show raw fuzzy result"):
    st.json(result)