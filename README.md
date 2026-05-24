# Fuzzy-detox Recommendation System

**Hierarchical Mamdani Fuzzy Inference System for Digital Habit Analysis** 
  
>University of Fribourg · Fuzzy Sets and Systems II · Spring 2026  
>*Course: Fuzzy Sets and Systems II — Prof. Dr. Edy Portmann, Human-IST Institute*

**Allizha Theiventhiram** — University of Neuchâtel  
**Tishana Suthenthiran** — University of Fribourg  
**Sandra Nikoloska** — University of Bern  

---

## What is fuzzy-detox?

**fuzzy-detox** analyses a user's digital device habits using a two-layer hierarchical Mamdani Fuzzy Inference System and produces a personalised **HabitBalance score (0–10)** along with evidence-based recommendations.

Unlike existing tools (Apple Screen Time, Google Digital Wellbeing) that only count total minutes, fuzzy-detox evaluates *how* you use your phone — detecting automatic checking behaviour, late-night use patterns, social media exposure, and screen glances — and handles the inherent ambiguity of human behaviour through fuzzy logic.

**The core argument:** "50 phone checks per day" is not simply good or bad. Fuzzy logic captures this grey area. A crisp rule-based system drops your score by 1.5 points for 2 extra glances at a threshold. The fuzzy system transitions smoothly — 7× more stable.

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/nikoloska/fuzzy-detox.git
### Prerequisite: Python version >= 3.11
cd fuzzy-detox # if not already there
pip install -r requirements.txt
pip install scipy matplotlib
```

### 2. Launch the dashboard

```bash
streamlit run src/app.py
```

The browser opens at `http://localhost:8501`. Use the sidebar sliders to enter your values — scores and recommendations update in real time.

### 3. Run the tests

```bash
pytest tests/test_fuzzy_model.py -v
```

Expected: **27 passed**.

### 4. Run the notebooks

```bash
jupyter notebook
```

Open in order:
- `data_simulation/data_simulation.ipynb` — simulated dataset and real data distributions
- `model_prototyping/model_prototyping.ipynb` — engine evaluation on 200 synthetic users
- `notebooks/Screen_Time_Balance_FCM_Scenario.ipynb` — Fuzzy Cognitive Map scenario analysis

---

## System Architecture

fuzzy-detox uses a **two-layer hierarchical fuzzy system** — a recognised design pattern for complex problems (Mendel, 2001).

<p align="center">
  <img src="fuzzy_system_architecture.png" alt="System Architecture of fuzzy-detox" width="100%">
</p>

> **Figure 1.** Two-layer hierarchical Mamdani fuzzy inference system used in fuzzy-detox. Raw behavioural inputs are processed through three parallel fuzzy subsystems (FocusQuality, SleepQuality, and DigitalOverload), whose outputs feed a fourth fuzzy inference system that produces the final HabitBalance score and personalised recommendation.

**Why hierarchical?** Each subsystem captures a distinct dimension of digital behaviour with its own rule base. Their defuzzified outputs feed a dedicated 4th FIS rather than a crisp formula — preserving fuzziness throughout the entire pipeline.

---

## Inputs

All Membership Functions and the entire rule database can be found in docs/Membership Functions and Rules.pdf.

| Variable | Unit | Range | Literature anchor |
|---|---|---|---|
| `ScreenGlances` | checks/day | 0–150 |
| `IdleChecking` | checks/day | 0–80 |
| `LateNightUse` | min before bedtime use | 0–180 |
| `SocialMediaUsage` | % of screen time | 0–100 |

## Outputs

| Variable | Range | Description |
|---|---|---|
| `FocusQuality` | 0–10 | Ability to concentrate without digital interruption |
| `SleepQuality` | 0–10 | Likely sleep quality based on night-time patterns |
| `DigitalOverload` | 0–10 | Level of cognitive overload from digital stimulation |
| **`HabitBalance`** | **0–10** | **Overall digital habit health — main score** |

---

## Using the Engine Directly

```python
from src.fuzzy_engine import evaluate_fuzzy_system

result = evaluate_fuzzy_system(
    screen_glances_value = 78,   # checks/day
    idle_checking_value  = 24,   # idle checks/day
    late_night_use_value = 67,   # minutes after 22:00
    social_media_value   = 62,   # % of screen time
)

print(result['outputs']['HabitBalance'])   # → 3.85
print(result['recommendation'])            # → personalised advice string
```

### Example output

```json
{
  "inputs": {
    "ScreenGlances": 78, "IdleChecking": 24,
    "LateNightUse": 67,  "SocialMediaUsage": 62
  },
  "outputs": {
    "FocusQuality": 4.28, "SleepQuality": 5.21,
    "DigitalOverload": 6.86, "HabitBalance": 3.85
  },
  "labels": {
    "FocusQuality": "Medium", "SleepQuality": "Medium",
    "DigitalOverload": "High", "HabitBalance": "Low"
  },
  "recommendation": "Replace late-night social scrolling with one planned offline wind-down activity."
}
```

---

## Dashboard Features

| Section | What it shows |
|---|---|
| **HabitBalance gauge** | Live score with colour-coded needle |
| **Profile detector** | Which of 4 archetypes matches your pattern |
| **Radar chart** | Focus, Sleep, Balance, Not-Overloaded at a glance |
| **Recommendations** | 3 personalised, literature-grounded actions |
| **Session history** | Up to 8 saved readings with sparkline trend |
| **Profile comparison** | Your score vs. 4 archetypes |
| **Rules firing** | Which IF-THEN rules are currently active |
| **Input MF visualisation** | Where your values fall on each fuzzy set |
| **Output MF visualisation** | How each score is defuzzified |
| **Fuzzy vs. crisp comparison** | Live side-by-side + 3 analysis charts |
| **Sensitivity analysis** | Which input drives HabitBalance the most |

---

## Evaluation

### Fuzzy vs. Crisp Comparison

A crisp rule-based baseline (`src/crisp_engine.py`) uses the same thresholds as the fuzzy MF crossover points. At the critical threshold of 40 glances/day:

| | 39 glances | 41 glances | Δ |
|---|---|---|---|
| **Crisp** | 7.00 | 5.50 | **−1.50 pts** |
| **Fuzzy** | 6.60 | 6.40 | **−0.20 pts** |

The fuzzy system is **7.5× more stable** at threshold boundaries — consistent with the rationale for fuzzy logic in human behaviour modelling.

### Sensitivity Analysis

Each input was swept across its full range while others were fixed at ideal values. HabitBalance variation:

| Input | Range of HabitBalance | Influence |
|---|---|---|
| `ScreenGlances` | 5.01 pts (50% of scale) | ★★★★ Highest |
| `LateNightUse` | 4.68 pts (47% of scale) | ★★★★ High |
| `IdleChecking` | 2.68 pts (27% of scale) | ★★★ Medium |
| `SocialMediaUsage` | 1.25 pts (12% of scale) | ★★ Lowest |

ScreenGlances and LateNightUse are the most critical variables for digital habit health.

---

## Testing

27 unit tests across 6 classes:

```
TestOutputStructure   (6)  — return type, required keys, variable names
TestOutputRanges      (5)  — all outputs within 0–10 for 5 input combinations
TestProfileOrdering   (6)  — balanced > night owl, correct score directions
TestFuzzySmoothness   (2)  — no abrupt jumps, monotonic decrease
TestLabels            (4)  — correct label assignments and valid label set
TestInputClamping     (2)  — graceful handling of out-of-range inputs
```

```bash
pytest tests/test_fuzzy_model.py -v
# 27 passed in ~12s
```

---

## Repository Structure

```
fuzzy-detox-main/
│
├── src/
│   ├── app.py                  # Streamlit dashboard — run this
│   ├── fuzzy_engine.py      # Hierarchical Mamdani FIS (4 subsystems)
│   ├── crisp_engine.py         # Crisp if-else baseline for comparison
│   ├── mf_viz.py               # Membership function visualisation (matplotlib)
│   ├── comparison_viz.py       # Fuzzy vs. crisp comparison charts
│   ├── sensitivity.py          # Sensitivity analysis module
│   ├── comparison_app.py       # Standalone fuzzy vs. crisp Streamlit app
|
├── previous versions/
│   └── [app_v1–v3, engine_v1–v3, crisp_app]  — iteration history
│
├── notebooks/
│   ├── Screen_Time_Balance_FCM_Scenario.ipynb  # FCM tutorial (course deliverable)
│   └── [see also data_simulation/ and model_prototyping/]
│
├── data_simulation/
│   ├── data_simulation.ipynb         # Hybrid dataset construction
│   ├── simulated_dataset.csv         # 200 synthetic user-days
│   └── simulated_dataset_full.csv    # With source tags per variable
│
├── model_prototyping/
│   ├── model_prototyping.ipynb       # Engine evaluation on 200 users
│   ├── fuzzy_results.csv             # Output scores for all 200 users
│   └── [sensitivity, MF, output distribution plots]
│
├── docs/
│   ├── USER_MANUAL.md                      # Installation and usage guide
│   ├── Membership Functions and Rules.pdf  # Literature based Rule Base
│   ├── CHANGELOG.md                        # v1 → v4 iteration log
│   ├── comparison_threshold.png            # Threshold problem visualisation
│   ├── comparison_sweep.png                # Full sweep comparison chart
│   ├── comparison_profiles.png             # 5-profile comparison
│   ├── sensitivity_curves.png              # Response curves per input
│   └── sensitivity_ranking.png             # Input influence ranking
│
├── tests/
│   └── test_fuzzy_model.py           # 27 unit tests (pytest)
│
├── requirements.txt
└── README.md
```

---

## Data Strategy

The dataset covers 4 user archetypes identified from user interviews:

| Profile | Behaviour | Expected HabitBalance |
|---|---|---|
| ⚖️ Balanced User | Low across all inputs — intentional use | High (≥ 7) |
| 📚 Focused Worker | Low glances, low social media | Medium–High |
| 🌙 Night Owl | High late-night use, high social media | Low |
| 📲 Distracted Achiever | High glances, high idle checking | Low |

---
