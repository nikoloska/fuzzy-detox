# fuzzy-detox — User Manual

## What is fuzzy-detox?

fuzzy-detox is a digital habit analyser built on a **hierarchical Mamdani Fuzzy Inference System**. It takes four behavioural measurements as input and produces a personalised HabitBalance score (0–10) along with targeted recommendations grounded in academic literature.

## Installation

**Requirements:** Python 3.10+ with pip or conda.

```bash
git clone https://github.com/your-repo/fuzzy-detox.git
cd fuzzy-detox-main
pip install -r requirements.txt
pip install scipy matplotlib
```

## Running the app

```bash
streamlit run src/app.py
```

The browser opens automatically at `http://localhost:8501`.

## Inputs

| Input | Unit | Range | What it measures |
|---|---|---|---|
| ScreenGlances | glances/day | 0–150 | How often you pick up your phone |
| IdleChecking | checks/day | 0–80 | Checking phone without a clear purpose |
| LateNightUse | min after 22:00 | 0–180 | Phone use after 10 PM |
| SocialMediaUsage | % of screen time | 0–100 | Share of time on social platforms |

Use the sliders in the left sidebar to enter your values.

## Outputs

| Output | Range | Meaning |
|---|---|---|
| FocusQuality | 0–10 | Ability to concentrate without digital interruption |
| SleepQuality | 0–10 | Likely sleep quality based on night-time usage |
| DigitalOverload | 0–10 | Level of digital stimulation overload |
| **HabitBalance** | **0–10** | **Overall digital habit health (main score)** |

A score above 7 is healthy. Below 4 indicates digital habits that likely affect focus and sleep.

## How it works

fuzzy-detox uses a **two-layer hierarchical fuzzy system**:

**Layer 1:** Three parallel Mamdani FIS analyse the raw inputs and produce FocusQuality, SleepQuality, and DigitalOverload via centroid defuzzification.

**Layer 2:** A 4th Mamdani FIS with 27 IF-THEN rules aggregates the three intermediate scores and produces HabitBalance via centroid defuzzification.

This design preserves fuzziness end-to-end (Mendel, 2001).

## Membership function visualisation

Expand the **"Input membership functions"** and **"Output membership functions"** panels below the main dashboard to see exactly where your values fall on each fuzzy set and how the inference is computed.

## Running tests

```bash
pytest tests/test_fuzzy_model.py -v
```

Expected output: `27 passed`.

## Comparison mode

The app includes a crisp rule-based comparison system (`src/crisp_engine.py`). Run `streamlit run src/comparison_app.py` to see side-by-side how the fuzzy system handles borderline cases more gracefully than crisp thresholds.

## References

- Kushlev, K. et al. (2015). Checking email less frequently reduces stress. *Computers in Human Behavior*.
- Christensen, M.A. et al. (2016). Direct measurements of smartphone screen-time. *PLOS ONE*.
- Digital Wellness Institute (2024). Digital Wellness Framework.
- Mendel, J.M. (2001). *Uncertain Rule-Based Fuzzy Systems*. Springer.
