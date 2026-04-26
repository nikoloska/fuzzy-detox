# Project : Fuzzy-detox 🧠📱

> **Fuzzy Logic–Based Screen Time Balance and Digital Habit Recommendation System**  
> University of Fribourg · Fuzzy Sets and Systems · April 2026

---

## Overview

**fuzzy-detox** is a two-subsystem Mamdani fuzzy inference system that analyses a user's digital device habits and provides personalised recommendations for healthier screen time balance.

Instead of measuring *how much* you use your phone, the system evaluates *how well* — detecting automatic checking behaviour, late-night use, and social media overload, then translating these into actionable advice.

### The Problem

Existing screen-time tools (Apple Screen Time, Google Digital Wellbeing) only count total minutes. They ignore:
- **When** you check your phone (idle moments, late at night)
- **What** you consume (social media vs. productive content)
- **How** checking behaviour fragments attention and disrupts sleep

### Our Solution

A fuzzy logic system that captures the grey area of human digital behaviour — because "50 phone checks per day" is not simply good or bad. It depends on context.

---

## System Architecture

```
Raw Inputs (4 variables)
        │
        ▼
┌───────────────────────┐
│     Subsystem 1       │  Fuzzification → IF-THEN rules → Defuzzification
│  (Behaviour Analysis) │
└───────────────────────┘
        │
        ▼
Intermediate Outputs:
  FocusQuality · SleepQuality · DigitalOverload
        │
        ▼
┌───────────────────────┐
│     Subsystem 2       │  Weighted aggregation
│   (Habit Scoring)     │
└───────────────────────┘
        │
        ▼
Final Output: HabitBalance (0–10) + Personalised Recommendation
```

### Input Variables

| Variable | Range | Source |
|---|---|---|
| `ScreenGlances` | 0–150 checks/day | Ellis & Shaw, Lancaster (2018) |
| `IdleChecking` | 0–80 checks/day | Mark et al. (2008) — 23-min recovery time |
| `LateNightUse` | 0–180 min after 22:00 | Combertaldi et al., Fribourg (2021) |
| `SocialMediaUsage` | 0–100 % of screen time | Twenge & Campbell (2018) |

### Intermediate Outputs (Subsystem 1)

| Variable | Range | Key rule source |
|---|---|---|
| `FocusQuality` | 0–10 | Ward et al. (2017) — Brain Drain effect |
| `SleepQuality` | 0–10 | Rasch & Born (2013), Fribourg sleep lab |
| `DigitalOverload` | 0–10 | Kushlev et al. (2017), Sweller CLT (1991) |

### Final Output (Subsystem 2)

```
HabitBalance = 0.4 × FocusQuality
             + 0.4 × SleepQuality
             + 0.2 × (10 − DigitalOverload)
```

---

## Repository Structure

```
fuzzy-detox/
├── src/
│   ├── fuzzy_engine.py          # Core Mamdani FIS — all MFs, rules, evaluation function
│   └── app.py                   # Streamlit dashboard (run this)
│
├── notebooks/
│   ├── 01_data_exploration.ipynb      # Data simulation — hybrid dataset (200 user-days)
│   ├── 02_model_prototyping.ipynb     # Engine evaluation — scenarios, fuzzy vs crisp, sensitivity
│   └── Screen_Time_Balance_FCM_Scenario.ipynb  # Fuzzy Cognitive Map — scenario & intervention analysis
│
├── tests/
│   └── test_fuzzy_model.py      # pytest unit tests — 20 tests across 6 test classes
│
├── data/
│   ├── simulated_dataset.csv          # 200 synthetic user-days (4 profiles × 50)
│   └── simulated_dataset_full.csv     # Same + source tags per variable
│
├── requirements.txt
└── README.md
```

---

## Quick Start

### 1. Clone & install

```bash
git clone https://github.com/nikoloska/fuzzy-detox.git
cd fuzzy-detox
pip install -r requirements.txt
```

### 2. Run the dashboard

```bash
cd src
python -m streamlit run app.py
```

The dashboard opens in your browser. Use the sliders to input your behaviour values and see your HabitBalance score and recommendation in real time.

### 3. Run the notebooks

```bash
cd notebooks
jupyter notebook
```

Open in order:
- `01_data_exploration.ipynb` — explore the simulated dataset and real data distributions
- `02_model_prototyping.ipynb` — run the engine on 200 simulated users, validate scenarios
- `Screen_Time_Balance_FCM_Scenario.ipynb` — FCM scenario and intervention analysis

### 4. Run the tests

```bash
pytest tests/test_fuzzy_model.py -v
```

---

## The Fuzzy Engine

The core function in `src/fuzzy_engine.py`:

```python
from fuzzy_engine import evaluate_fuzzy_system

result = evaluate_fuzzy_system(
    screen_glances_value = 78,   # checks/day
    idle_checking_value  = 24,   # idle checks/day
    late_night_use_value = 67,   # minutes after 22:00
    social_media_value   = 62,   # % of screen time
)

print(result['outputs']['HabitBalance'])    # e.g. 3.1
print(result['recommendation'])             # personalised advice
```

### Example output

```json
{
  "inputs": {
    "ScreenGlances": 78, "IdleChecking": 24,
    "LateNightUse": 67,  "SocialMediaUsage": 62
  },
  "outputs": {
    "FocusQuality": 3.4,  "SleepQuality": 2.9,
    "DigitalOverload": 8.1, "HabitBalance": 3.1
  },
  "labels": {
    "FocusQuality": "Low", "SleepQuality": "Low",
    "DigitalOverload": "High", "HabitBalance": "Low"
  },
  "recommendation": "Sleep quality is weak. Reduce late-night use after 22:00."
}
```

---

## Data Strategy

No single public dataset contains all four input variables. We use a **hybrid approach**:

| Variable | Source |
|---|---|
| `ScreenGlances` | Anchored to real distributions — `Phone_Unlocks_Per_Day` from the Global Mobile Phone Addiction Dataset (Kaggle, n=3,000) |
| `SocialMediaUsage` | Derived from `Social_Media_Usage_Hours / Daily_Screen_Time_Hours` (same Kaggle dataset) |
| `IdleChecking` | Simulated — distributions from Ellis & Shaw, Lancaster University (2018) |
| `LateNightUse` | Simulated — distributions from Combertaldi, Ort, Cordi, Fahr & Rasch, University of Fribourg (2021) |

The simulated dataset covers **4 user archetypes** identified from user interviews:

| Profile | Behaviour pattern | Expected HabitBalance |
|---|---|---|
| 🟢 Balanced User | Low on all inputs — intentional use | High (> 6) |
| 🔵 Focused Worker | Low glances, low social media | Medium-High |
| 🟣 Night Owl | High late-night use, high social media | Low |
| 🔴 Distracted Achiever | High glances, high idle checking | Low |

---

## Membership Functions

All membership functions use **trapezoid** (Low, High sets) and **triangle** (Medium set) shapes with deliberate overlaps. The overlap zones ensure smooth, gradual output changes rather than abrupt threshold jumps.

Example — `ScreenGlances`:
- **Low:** `trapMF [0, 0, 20, 40]` — below 40 checks: intentional, controlled use
- **Medium:** `triMF [20, 50, 90]` — peak at 50: Lancaster study average
- **High:** `trapMF [65, 90, 150, 150]` — above 65: cognitive stress zone (Kushlev 2017)

---

## Evaluation Methodology

Three evaluation approaches (see `02_model_prototyping.ipynb`):

**1. Scenario-Based Testing**  
200 synthetic user-days across 4 profiles are fed through the engine. 12 explicit pass/fail checks validate that each profile receives the expected output direction.

**2. Fuzzy vs. Crisp Logic Comparison**  
The fuzzy system is compared against a traditional if-else baseline at borderline input values. The fuzzy system produces smooth, proportional transitions; the crisp baseline produces abrupt jumps.

**3. Sensitivity Analysis**  
Each input is varied in +5 increments while others are held fixed. Output curves are monotonic and smooth — confirming the Centroid defuzzification behaves correctly.

---

## Authors & Collaboration

- Allizha Theiventhiram — University of Neuchâtel  
- Tishana Suthenthiran — University of Fribourg  
- Sandra Nikoloska — University of Bern  
---

## Key References

- Sweller, J. (1991). Cognitive Load Theory. *Cognitive Science*, 12(2).
- Ward, A. F. et al. (2017). Brain Drain: Smartphone presence reduces cognitive capacity. *JACR*, 2(2).
- Kushlev, K. et al. (2017). Digitally connected, socially disconnected. *Computers in Human Behavior*, 76.
- Przybylski, A. K., & Weinstein, N. (2017). Goldilocks hypothesis. *Psychological Science*, 28(2).
- Twenge, J. M., & Campbell, W. K. (2018). Screen time and lower well-being. *Preventive Medicine Reports*, 12.
- Combertaldi, S. L., Ort, A., Cordi, M., Fahr, A., & Rasch, B. (2021). Pre-sleep social media use does not strongly disturb sleep. *Sleep Medicine*, 87. **University of Fribourg.**
- Ellis, D. A., & Shaw, H. (2018). Typical smartphone usage dataset. Lancaster University.
- Mark, G., Gudith, D., & Klocke, U. (2008). The cost of interrupted work. *CHI '08*.
- Siebers, T. et al. (2024). Adolescents' digital nightlife. *Journal of Communication*, 74(5).
- Brautsch, L. A. et al. (2023). Digital media use and sleep. *Sleep Medicine Reviews*, 68.
- Newport, C. (2016). *Deep Work*. Grand Central Publishing.
- E. Portmann, G. Wilke, L. Terán, and S. D'Onofrio, Eds. *Fuzzy Sets and Systems I*. Springer Nature Switzerland, 2026.
