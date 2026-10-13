# Week 3 — Assignments: Matplotlib & Seaborn
**Course:** CDB601220 Data Visualization (Lectures 5 & 6)  
**Student:** Muhammad Maheem  
**Student ID:** SU92-BSAIM-F24-054  

---

## 🚀 Quick Start / Installation

### 1. Requirements
- Python 3.9+ (Python 3.11 or 3.12 recommended)
- Install all dependencies via pip:
```bash
pip install -r requirements.txt
```
*(Packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `reportlab`, `pypdf`)*

### 2. Run Everything in One Command
```bash
./run_all.sh
```
This script runs every part sequentially, confirms all self-checks, and regenerates all figures, tables, and PDF reports from the clean raw datasets.

---

## 📁 Repository Structure & Deliverables

```
week3/assignments/
├── README.md                      # This guide
├── requirements.txt               # Dependencies
├── run_all.sh                     # Automated runner script
├── TASKS.md                       # Assignment prompt & rubric
├── vizlib.py                      # Course visualization toolkit
│
├── data/                          # 10 synthetic datasets & DATA_DICTIONARY.md
│   ├── DATA_DICTIONARY.md
│   ├── case01_helmet_rickshaw.csv
│   ├── case02_chai_quizzes.csv
│   ├── case03_aqi_monitors.csv
│   ├── case04_quartet_depts.csv
│   ├── case05_same_stats_shapes.csv
│   ├── case06_sensor_matrix.csv
│   ├── case07_dual_axis_series.csv
│   ├── case07_lie_factor.csv
│   ├── vitals_10k.csv
│   └── ward_los_wide.csv
│
├── partA_charts.py                # Part A: Rebuilds 9 claims & plots 9 redesigns
├── generate_partA_pdf.py          # Part A: Compiles formal diagnosis PDF
├── figures_partA/                 # 18 individual rebuild & redesign PNGs (300 DPI)
├── partA_diagnosis.pdf            # 9-page formal diagnosis report
│
├── partB_lie_factor.py            # Part B: Lie Factor audit script
├── partB_output.txt               # Part B: Printed audit table & answers
│
├── partC_palette.py               # Part C: Palette CVD simulation script
├── partC_palette.png              # Part C: Before/after swatch comparison
├── partC_figure_deutan_check.png  # Part C: Figure-level deuteranopia check
│
├── partD_figure.py                # Part D: Data cleaning & 2x2 clinical review figure
├── partD_figure.png               # Part D: Exported 300 DPI clinical review figure
│
├── generate_partE_pdf.py          # Part E: Compiles strictly 1-page justification PDF
├── partE_justification.pdf        # Part E: Exactly 1-page written justification
│
├── popout_experiment.py           # Bonus: Preattentive pop-out experiment
├── popout_panels.png              # Bonus: 4 visual search condition panels
├── popout_experiment_chart.png    # Bonus: Reaction time chart (summary + raw points)
│
└── W3_SU92-BSAIM-F24-054.zip      # Complete LMS submission archive
```

---

## 🔍 Part-by-Part Summary

### Part A · Diagnosing the Nine Claims (36 Marks)
- **Case 1 (Helmet Rickshaw):** Simpson's Paradox. Premium helmets are 25–28% safer across every road type; 85% of Premium trips were on high-risk Motorways.
- **Case 2 (Chai vs Quizzes):** Spurious scale correlation. Total enrollment grew from 1,765 to 5,406; normalized per-student rate collapses correlation to $r = 0.29$.
- **Case 3 (Lahore AQI):** Monitor attrition bias. All 6 high-pollution industrial monitors went offline on Day 61; active zones experienced 0% improvement.
- **Case 4 (Anscombe's Quartet):** Summary moments mask distinct structural distributions (linear, quadratic curve, outlier-corrupted line, and leverage point).
- **Case 5 (Datasaurus Shapes):** Annealed geometric point clouds (star, ring, line, X, clusters) sharing identical statistical moments.
- **Case 6 (Sensor Matrix):** Single leverage outlier (Row 0: 1,050 µmol/L, 15.8%) created spurious $r = 0.77$ (clean $r = -0.00$); paired with diverging heatmap.
- **Case 7 (ShaheenGo Dual-Axis):** Superimposed twin y-axes created fake crossover; single common axis from zero proves company was profitable in every month (+8M to +25M PKR).
- **Case 8 (Histogram Bins):** Discretization sensitivity; `bins=45` ($\approx 2.4\text{ mmHg}$) correctly reveals clinical bimodality without comb empty-bin aliasing.
- **Case 9 (SpO2 Boundary Leak):** Unbounded Gaussian KDE leaked probability across physical 100% ceiling; fixed with integer-binned unit histogram.

### Part B · Lie Factor Audit (15 Marks)
- Chart C is the **only honest graphic** ($LF = 1.000$).
- Chart A exaggerates 75.00× (truncated baseline at 29.6%).
- Charts B and E require `ink_dimension=2` (icon and bubble area).
- Chart D understates a 50% pollution jump as 12.5% ($LF = 0.250$), shielding polluters.
- Chart F (dual-axis) has an undefined Lie Factor because the two lines exist on arbitrary unlinked coordinate systems.

### Part C · Color-Blind Safety (9 Marks)
- `tab10` fails under protanopia ($\Delta E = 0.7$) and deuteranopia ($\Delta E = 4.1$).
- Course palette 4th slot (#CC79A7) yields $\Delta E = 7.5$ under deuteranopia, requiring a redundant channel.
- Rule for $>3$ categories: never rely on color alone; use marker shapes, direct labels, or small multiples.

### Part D · Clinical Review Figure (25 Marks)
- 12 ward spelling variants conformed to 4 canonical wards (0 rows dropped).
- 10,000 admission dates parsed across 3 text formats.
- 486 BMI sentinels (999.0 and 0.0) replaced with NaN.
- Derived MAP column excluded from discovery heatmap.
- 4 panels answering clear clinical questions with declared parameters, course palette, and 300 DPI export.

### Part E · Written Justification (15 Marks)
- Strictly **one page** covering channel rules, parameter nominations, cleaning audit trail, and the mandatory ethics clause with symmetry test.
- Heart rate telemetry faults ($n = 29 > 250\text{ bpm}$ up to 415 bpm, $n = 8 < 30\text{ bpm}$) removed as physical impossibilities (mean moves from 78.83 to 78.05 bpm, $N = 9,963$).

### Bonus · Preattentive Pop-out (5 Marks)
- Evaluates 4 visual search conditions across $n = 5$ subjects.
- Proves colour and redundant coding speed detection 6× over serial search (2.80s vs 18.76s) with zero speed cost for redundant accessibility encoding.

---

## 📜 Academic Integrity & Data Citation
All data in this folder is synthetic and generated for course CDB601220 from fixed pseudorandom seeds.
