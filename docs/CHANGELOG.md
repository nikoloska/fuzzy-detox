# Changelog — fuzzy-detox

## v4.0 — Final Release (May 2026)

### Added
- **4th Mamdani FIS for HabitBalance** (`fuzzy_engine_v4.py`): HabitBalance is now
  produced by a dedicated FIS with 27 IF-THEN rules and centroid defuzzification,
  completing a fully hierarchical fuzzy pipeline end-to-end.
- **Membership function visualisation** (`mf_viz.py`): interactive matplotlib panels
  showing input and output MFs with current values marked.
- **Hierarchical FIS overview bar chart**: all 4 output scores at a glance.
- **27 unit tests** across 6 classes (structure, ranges, profiles, smoothness, labels,
  clamping). All pass on Python 3.10–3.13.
- **User manual** (`docs/USER_MANUAL.md`): installation, inputs, outputs, architecture.

### Changed
- `app_v3.py` / `app.py`: imports updated to `fuzzy_engine_v4`; MF visualisation
  panels added below the main dashboard.
- System explanation updated to reflect the hierarchical Mamdani design (Mendel, 2001).
- Kushlev reference corrected from 2017 to 2015.

---

## v3.0 — Mid-term iteration (April 2026)

### Added
- Dashboard redesign: gauge, radar chart, profile detector, what-if simulator.
- Literature-grounded recommendations (15 rules from 8 sources).
- Session history with up to 8 saved readings.
- Crisp comparison app (`comparison_app.py`, `crisp_engine.py`).

### Changed
- `fuzzy_engine_v3.py`: refined membership function boundaries based on
  Christensen et al. (2016) and Digital Wellness Institute (2024) thresholds.

---

## v2.0 — First working prototype (March 2026)

### Added
- Three Mamdani subsystems: FocusQuality, SleepQuality, DigitalOverload.
- Basic Streamlit interface with sliders.
- Profile archetypes: Balanced, Night Owl, Doomscroller, Focused Worker.

---

## v1.0 — Design dash prototype (February 2026)

### Added
- Initial fuzzy engine proof-of-concept with single FIS.
- FCM notebook (fuzzy cognitive maps) for course programming tutorial.
- Simulated dataset of 500 synthetic users.
