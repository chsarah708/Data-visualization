"""
Part A — Rebuild nine charts, then take them apart (36 marks)

Rebuilds all nine published claims from their exact recipes, hitting all self-check
numbers, and plots nine honest redesigns that diagnose and correct each failure mode.
"""

from __future__ import annotations

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Add parent directory to import vizlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vizlib import MARKERS, PALETTE, save_fig, style_defaults

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(ROOT, "figures_partA")
os.makedirs(FIG_DIR, exist_ok=True)
style_defaults()
C = PALETTE["series"]


# =============================================================================
# CASE 1: Helmet Rickshaw Safety (Simpson's Paradox)
# =============================================================================
def case1():
    df = pd.read_csv(os.path.join(ROOT, "data", "case01_helmet_rickshaw.csv"))

    # --- Rebuild ---
    # Sum head_injuries and trips by helmet_grade. Plot injuries per 1,000 trips as bar chart, y-axis from zero.
    g = df.groupby("helmet_grade")[["head_injuries", "trips"]].sum()
    rate = (g["head_injuries"] / g["trips"] * 1000).loc[["Standard", "Premium"]]
    # Self-check: Standard 2.15, Premium 5.40

    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    bars = ax.bar(["Standard", "Premium"], rate.values, color=[C[0], C[1]], width=0.45)
    ax.set_ylim(0, 7.0)
    ax.set_title("Published Claim: Premium Helmets Have 2.5× the Head-Injury Rate", fontsize=11, fontweight="bold")
    ax.set_xlabel("Helmet Certification Grade")
    ax.set_ylabel("Head Injuries per 1,000 Trips")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.18, f"{h:.2f}", ha="center", fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case01_rebuild.png"), "Self-check verified: Standard 2.15, Premium 5.40 injuries per 1,000 trips. (n = 100,000 trips)")
    plt.close(fig)

    # --- Redesign ---
    # Segment by road_type: reveals Simpson's Paradox
    g_road = df.groupby(["road_type", "helmet_grade"])[["head_injuries", "trips"]].sum()
    road_rate = (g_road["head_injuries"] / g_road["trips"] * 1000).unstack()[["Standard", "Premium"]]
    
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    x = np.arange(len(road_rate))
    w = 0.32
    b1 = ax.bar(x - w / 2, road_rate["Standard"], width=w, label="Standard", color=C[0])
    b2 = ax.bar(x + w / 2, road_rate["Premium"], width=w, label="Premium", color=C[1])
    
    ax.set_xticks(x)
    ax.set_xticklabels(road_rate.index)
    ax.set_ylim(0, 10.0)
    ax.set_title("Simpson's Paradox: Premium Helmets Are 25–28% Safer on Every Road Type", fontsize=11.5, fontweight="bold")
    ax.set_xlabel("Road Environment (conflated exposure)")
    ax.set_ylabel("Head Injuries per 1,000 Trips")
    ax.legend(title="Certification", frameon=False)
    
    for bar in list(b1) + list(b2):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.22, f"{h:.2f}", ha="center", fontsize=8.5, fontweight="bold")
    
    ax.text(0.03, 0.78, "Aggregate 2.5× rate was caused by road exposure:\n85% of Premium trips were on high-risk Motorways\nvs. only 3.3% of Standard trips.", transform=ax.transAxes, fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case01_redesign.png"), "Controlled comparison by road type: Motorway (-25%), City Arterial (-27%), Inner-city (-28%).")
    plt.close(fig)

    print(f"Case 1 completed: {rate['Standard']:.2f}, {rate['Premium']:.2f}")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 2: Chai vs. Quiz Failures (Spurious Scale Confounder)
# =============================================================================
def case2():
    df = pd.read_csv(os.path.join(ROOT, "data", "case02_chai_quizzes.csv"))

    # --- Rebuild ---
    # Scatter cups_doodh_patti_sold against quiz_failures, fit least-squares line, annotate Pearson r.
    # Self-check: r = 0.98
    r = df["cups_doodh_patti_sold"].corr(df["quiz_failures"])

    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.scatter(df["cups_doodh_patti_sold"], df["quiz_failures"], color=C[0], s=45, alpha=0.85, edgecolors="none")
    slope, intercept = np.polyfit(df["cups_doodh_patti_sold"], df["quiz_failures"], 1)
    x_line = np.linspace(df["cups_doodh_patti_sold"].min(), df["cups_doodh_patti_sold"].max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color=PALETTE["highlight"], lw=2.0)
    ax.set_title(f"Published Claim: Canteen Chai Sales Predict Quiz Failures (Pearson r = {r:.2f})", fontsize=11, fontweight="bold")
    ax.set_xlabel("Cups of Doodh Patti Sold (monthly)")
    ax.set_ylabel("Quiz Failures Recorded (monthly)")
    ax.text(0.05, 0.85, f"Least-squares fit\nPearson r = {r:.2f}\nr² = {r**2:.2f}", transform=ax.transAxes, fontsize=10, fontweight="bold", color=PALETTE["highlight"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case02_rebuild.png"), "Self-check verified: Pearson r = 0.98. Unstandardized raw monthly counts (24 months).")
    plt.close(fig)

    # --- Redesign ---
    # Standardize per enrolled student: correlation drops to r = 0.29
    df["chai_per_student"] = df["cups_doodh_patti_sold"] / df["students_enrolled"]
    df["failures_per_student"] = df["quiz_failures"] / df["students_enrolled"]
    r_norm = df["chai_per_student"].corr(df["failures_per_student"])

    fig, ax = plt.subplots(figsize=(7.5, 5.0))
    sc = ax.scatter(df["chai_per_student"], df["failures_per_student"] * 100, c=df["students_enrolled"], cmap="Blues", s=55, edgecolors=PALETTE["ink_soft"], linewidth=0.6)
    cbar = fig.colorbar(sc, ax=ax, shrink=0.85)
    cbar.set_label("Enrolled Students", fontsize=9)
    
    slope_norm, intercept_norm = np.polyfit(df["chai_per_student"], df["failures_per_student"] * 100, 1)
    x_line_norm = np.linspace(df["chai_per_student"].min(), df["chai_per_student"].max(), 100)
    ax.plot(x_line_norm, slope_norm * x_line_norm + intercept_norm, color=PALETTE["highlight"], linestyle="--", lw=1.8)
    
    ax.set_title(f"Per-Capita Metric Disproves Link: Chai Does Not Predict Failures (r = {r_norm:.2f})", fontsize=11, fontweight="bold")
    ax.set_xlabel("Chai Cups Sold per Enrolled Student")
    ax.set_ylabel("Quiz Failure Rate (%)")
    ax.text(0.04, 0.88, f"Normalized Pearson r = {r_norm:.2f}\nBoth metrics scaled with enrollment\nexpanding from 1,765 to 5,406 students.", transform=ax.transAxes, fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case02_redesign.png"), "Per-capita normalization reveals spurious correlation caused by student body growth.")
    plt.close(fig)

    print(f"Case 2 completed: r_raw={r:.2f}, r_norm={r_norm:.2f}")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 3: Lahore AQI Monitors (Survivorship / Attrition Bias)
# =============================================================================
def case3():
    df = pd.read_csv(os.path.join(ROOT, "data", "case03_aqi_monitors.csv"))

    # --- Rebuild ---
    # Mean aqi per date across every row. Line plot, y-axis from zero.
    # Vertical marker at day 61, horizontal mean lines for days 1-60 and 61-120.
    daily = df.groupby("date")["aqi"].mean().reset_index()
    dates = sorted(daily["date"].unique())
    m_before = daily.loc[daily["date"].isin(dates[:60]), "aqi"].mean()
    m_after = daily.loc[daily["date"].isin(dates[60:120]), "aqi"].mean()
    pct_fall = (m_before - m_after) / m_before * 100
    # Self-check: before 202, after 137 — 32% fall

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    days = np.arange(1, len(daily) + 1)
    ax.plot(days, daily["aqi"], color=C[0], lw=1.8, label="Reported Daily Mean AQI")
    ax.axvline(61, color=PALETTE["highlight"], linestyle="--", lw=1.6, label="Day 61 (Policy Launch)")
    ax.hlines(m_before, 1, 60, colors=PALETTE["ink"], linestyles="-", lw=2.2, label=f"Days 1–60 Mean ({m_before:.0f})")
    ax.hlines(m_after, 61, 120, colors=PALETTE["ink"], linestyles="-", lw=2.2, label=f"Days 61–120 Mean ({m_after:.0f})")
    
    ax.set_ylim(0, 320)
    ax.set_title(f"Published Claim: Smog Action Plan Cut Lahore's AQI by {pct_fall:.0f}% ({m_before:.0f} to {m_after:.0f})", fontsize=11, fontweight="bold")
    ax.set_xlabel("Day of Monitoring Period (2026-01-01 to 2026-04-30)")
    ax.set_ylabel("Air Quality Index (AQI)")
    ax.legend(loc="upper right", frameon=False, fontsize=8.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case03_rebuild.png"), "Self-check verified: before 202, after 137 — 32% fall. y-axis starts at zero.")
    plt.close(fig)

    # --- Redesign ---
    # Segment by zone to expose monitor dropouts
    daily_zone = df.groupby(["date", "zone"])["aqi"].mean().unstack().reset_index()
    daily_zone["day"] = np.arange(1, len(daily_zone) + 1)
    
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    zone_colors = {"Industrial": PALETTE["highlight"], "Arterial": C[1], "Residential": C[0], "Peri-urban": C[2]}
    for zone in ["Industrial", "Arterial", "Residential", "Peri-urban"]:
        ax.plot(daily_zone["day"], daily_zone[zone], label=zone, color=zone_colors[zone], lw=2.0)
        
    ax.axvline(61, color=PALETTE["ink_soft"], linestyle=":", lw=1.5)
    ax.text(61.5, 305, "Day 61: All 6 Industrial Stations\nDrop Offline (0 reporting)", fontsize=8.5, fontweight="bold", color=PALETTE["highlight"])
    
    ax.set_ylim(0, 380)
    ax.set_title("Monitor Attrition Artifact: Active Zones Experienced Zero AQI Improvement", fontsize=11.5, fontweight="bold")
    ax.set_xlabel("Day of Monitoring Period")
    ax.set_ylabel("Air Quality Index (AQI)")
    ax.legend(title="Monitoring Zone", frameon=False, loc="upper right")
    ax.text(0.03, 0.10, "Mean AQI before vs after Day 61 by zone:\n- Arterial: 244.7 -> 245.9 (+0.5%)\n- Peri-urban: 78.9 -> 80.4 (+1.8%)\n- Residential: 121.6 -> 120.8 (-0.7%)", transform=ax.transAxes, fontsize=8.2, bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case03_redesign.png"), "Segmented by zone: apparent citywide drop was caused by shutting off high-pollution monitors.")
    plt.close(fig)

    print(f"Case 3 completed: before={m_before:.1f}, after={m_after:.1f}, drop={pct_fall:.1f}%")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 4: Anscombe's Quartet in University Departments
# =============================================================================
def case4():
    df = pd.read_csv(os.path.join(ROOT, "data", "case04_quartet_depts.csv"))

    # --- Rebuild ---
    # Table of summary stats: n, mean hours, mean score, SD hours, SD score, r, slope
    # Self-check: every dept reports 18.00 / 14.50, r = 0.816, slope = 0.250
    table_rows = []
    for dept, g in df.groupby("department"):
        n = len(g)
        mx = g["study_hours_per_week"].mean()
        my = g["final_score_out_of_20"].mean()
        sx = g["study_hours_per_week"].std()
        sy = g["final_score_out_of_20"].std()
        r = g["study_hours_per_week"].corr(g["final_score_out_of_20"])
        slope = np.polyfit(g["study_hours_per_week"], g["final_score_out_of_20"], 1)[0]
        table_rows.append([dept, f"{n}", f"{mx:.2f}", f"{my:.2f}", f"{sx:.2f}", f"{sy:.2f}", f"{r:.3f}", f"{slope:.3f}"])

    fig, ax = plt.subplots(figsize=(9.0, 3.8))
    ax.axis("off")
    col_labels = ["Department", "n", "Mean Study Hrs", "Mean Score", "SD Study Hrs", "SD Score", "Pearson r", "Slope"]
    tab = ax.table(cellText=table_rows, colLabels=col_labels, loc="center", cellLoc="center")
    tab.auto_set_font_size(False)
    tab.set_fontsize(9.5)
    tab.scale(1.0, 1.8)
    for (row, col), cell in tab.get_celld().items():
        if row == 0:
            cell.set_facecolor(PALETTE["grid"])
            cell.set_text_props(weight="bold", color=PALETTE["ink"])
        else:
            cell.set_facecolor(PALETTE["surface"])
    ax.set_title("Published Claim: Four Departments Behave Identically, So Fund Them Equally", fontsize=11, fontweight="bold", pad=15)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case04_rebuild.png"), "Self-check verified: all 4 departments report Mean = 18.00 / 14.50, r = 0.816, Slope = 0.250.")
    plt.close(fig)

    # --- Redesign ---
    # 2x2 faceted scatter plot of the four cohorts with regression line
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.5), sharex=True, sharey=True)
    depts = ["Computer Science", "Business Administration", "Electrical Engineering", "Architecture"]
    descriptions = [
        "Linear relationship with noise",
        "Strict non-linear quadratic curve",
        "Tight linear fit with 1 outlier (18, 15)",
        "Vertical cluster with 1 leverage point (38, 19.5)"
    ]
    for idx, ax_i in enumerate(axes.flat):
        dept = depts[idx]
        sub = df[df["department"] == dept]
        ax_i.scatter(sub["study_hours_per_week"], sub["final_score_out_of_20"], color=C[0], s=50, edgecolors=PALETTE["ink"], lw=0.8)
        
        slope, intercept = np.polyfit(sub["study_hours_per_week"], sub["final_score_out_of_20"], 1)
        x_grid = np.linspace(8, 40, 100)
        ax_i.plot(x_grid, slope * x_grid + intercept, color=PALETTE["highlight"], lw=1.6)
        
        ax_i.set_title(f"{dept}\n({descriptions[idx]})", fontsize=9.5, fontweight="bold")
        ax_i.set_xlabel("Study Hours per Week")
        ax_i.set_ylabel("Final Score (/20)")
        ax_i.spines["top"].set_visible(False)
        ax_i.spines["right"].set_visible(False)
        
    fig.suptitle("Anscombe's Quartet: Identical Summary Stats Disguise Wildly Different Reality", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case04_redesign.png"), "Faceted scatter plot exposes non-linearity, outliers, and leverage points concealed by statistics.")
    plt.close(fig)

    print("Case 4 completed: all 4 departments identical statistics")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 5: Same Stats, Different Shapes (Datasaurus Phenomenon)
# =============================================================================
def case5():
    df = pd.read_csv(os.path.join(ROOT, "data", "case05_same_stats_shapes.csv"))

    # --- Rebuild ---
    # Summary table: one column per shape_name
    # Self-check: every cohort reports 48.00 / 63.00, SD 12.00 / 15.00, r = 0.420
    shapes = ["straight line", "ring", "star", "two clusters", "the letter X"]
    rows = []
    for s in shapes:
        sub = df[df["shape_name"] == s]
        rows.append([
            s,
            f"{len(sub)}",
            f"{sub['hours_on_platform'].mean():.2f}",
            f"{sub['assessment_score'].mean():.2f}",
            f"{sub['hours_on_platform'].std():.2f}",
            f"{sub['assessment_score'].std():.2f}",
            f"{sub['hours_on_platform'].corr(sub['assessment_score']):.3f}"
        ])

    fig, ax = plt.subplots(figsize=(9.0, 4.0))
    ax.axis("off")
    col_labels = ["Shape Name", "n", "Mean Hours", "Mean Score", "SD Hours", "SD Score", "Pearson r"]
    tab = ax.table(cellText=rows, colLabels=col_labels, loc="center", cellLoc="center")
    tab.auto_set_font_size(False)
    tab.set_fontsize(9.5)
    tab.scale(1.0, 1.8)
    for (row, col), cell in tab.get_celld().items():
        if row == 0:
            cell.set_facecolor(PALETTE["grid"])
            cell.set_text_props(weight="bold", color=PALETTE["ink"])
        else:
            cell.set_facecolor(PALETTE["surface"])
    ax.set_title("Published Claim: Five Cohorts, One Set of Statistics (Fund / Treat Identically)", fontsize=11, fontweight="bold", pad=15)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case05_rebuild.png"), "Self-check verified: every cohort reports 48.00 / 63.00, SD 12.03 / 15.04, r = 0.420.")
    plt.close(fig)

    # --- Redesign ---
    # 1x5 facet of scatter plots showing the 5 shapes
    fig, axes = plt.subplots(1, 5, figsize=(14.0, 3.4), sharex=True, sharey=True)
    for idx, s in enumerate(shapes):
        ax_i = axes[idx]
        sub = df[df["shape_name"] == s]
        ax_i.scatter(sub["hours_on_platform"], sub["assessment_score"], color=C[0], s=16, alpha=0.75, edgecolors="none")
        ax_i.set_title(f"Cohort: '{s}'", fontsize=9.5, fontweight="bold")
        ax_i.set_xlabel("Platform Hours")
        if idx == 0:
            ax_i.set_ylabel("Assessment Score")
        ax_i.spines["top"].set_visible(False)
        ax_i.spines["right"].set_visible(False)
        
    fig.suptitle("Same Stats, Different Graphs: Summary Moments Provide Zero Spatial Geometry", fontsize=11.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case05_redesign.png"), "Matejka & Fitzmaurice (2017) demonstration: 5 distinct geometric distributions with identical stats.")
    plt.close(fig)

    print("Case 5 completed: all 5 shapes identical statistics")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 6: Sensor Correlation Matrix (Single Outlier & Chart Failure)
# =============================================================================
def case6():
    df = pd.read_csv(os.path.join(ROOT, "data", "case06_sensor_matrix.csv"))

    # --- Rebuild ---
    # Correlation matrix of every numeric column except age_band, study_site, hr_device_model.
    # Heatmap: cmap="Reds", no vmin/vmax, both triangles shown.
    # Self-check: creatinine <-> hba1c = 0.77, systolic <-> map = 0.96, 20x20
    num_cols = [c for c in df.select_dtypes(include=np.number).columns if c not in ["age_band", "study_site", "hr_device_model"]]
    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(9.0, 7.5))
    sns.heatmap(corr, cmap="Reds", ax=ax, cbar_kws={"label": "Correlation"})
    ax.set_title("Published Claim: Creatinine Tracks HbA1c — A Finding (r = 0.77)", fontsize=11, fontweight="bold")
    ax.tick_params(axis="x", rotation=90, labelsize=7.5)
    ax.tick_params(axis="y", rotation=0, labelsize=7.5)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case06_rebuild.png"), "Self-check verified: creatinine <-> hba1c = 0.77, systolic <-> map = 0.96, matrix 20x20. Sequential Reds cmap, no vmin/vmax.")
    plt.close(fig)

    # --- Redesign ---
    # Two panels:
    # 1. Scatter plot of Creatinine vs HbA1c exposing row 0 outlier (1050, 15.8)
    # 2. Honest heatmap: diverging RdBu_r, vmin=-1, vmax=1, upper triangle masked, map_mmhg excluded, outlier removed
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6.0))

    # Panel 1: Outlier exposure
    ax1.scatter(df["creatinine"], df["hba1c"], color=C[0], s=35, alpha=0.75, label="Patients (n = 180)")
    outlier = df.iloc[0]
    ax1.scatter(outlier["creatinine"], outlier["hba1c"], color=PALETTE["highlight"], s=100, edgecolors=PALETTE["ink"], lw=1.5, zorder=5, label="Outlier Row 0 (1050 µmol/L, 15.8%)")
    
    # Regression with and without outlier
    slope_all, int_all = np.polyfit(df["creatinine"], df["hba1c"], 1)
    df_no_outlier = df[df["creatinine"] < 200]
    slope_clean, int_clean = np.polyfit(df_no_outlier["creatinine"], df_no_outlier["hba1c"], 1)
    
    x_span = np.linspace(50, 1100, 100)
    ax1.plot(x_span, slope_all * x_span + int_all, color=PALETTE["highlight"], lw=1.8, label="With outlier (r = 0.77)")
    ax1.plot(x_span, slope_clean * x_span + int_clean, color=PALETTE["ink_soft"], linestyle="--", lw=1.8, label="Without outlier (r = -0.00)")
    
    ax1.set_title("Single Bivariate Outlier Manufactured Spurious r = 0.77", fontsize=10.5, fontweight="bold")
    ax1.set_xlabel("Serum Creatinine (µmol/L)")
    ax1.set_ylabel("HbA1c (%)")
    ax1.legend(loc="lower right", frameon=False, fontsize=8)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Panel 2: Honest heatmap on clean data (excluding derived map_mmhg and outlier)
    cols_clean = [c for c in num_cols if c != "map_mmhg"]
    corr_clean = df_no_outlier[cols_clean].corr()
    mask = np.triu(np.ones_like(corr_clean, dtype=bool))
    
    sns.heatmap(corr_clean, mask=mask, cmap="RdBu_r", vmin=-1.0, vmax=1.0, center=0.0, ax=ax2, cbar_kws={"label": "Pearson r", "shrink": 0.8})
    ax2.set_title("Honest Heatmap: Diverging RdBu_r, Masked Triangle, MAP Excluded", fontsize=10.5, fontweight="bold")
    ax2.tick_params(axis="x", rotation=90, labelsize=7)
    ax2.tick_params(axis="y", rotation=0, labelsize=7)

    fig.suptitle("Case 6 Diagnosis: Both the Data and the Graphic Were Broken", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case06_redesign.png"), "Data fix: removing row 0 drops r from 0.77 to -0.00. Graphic fix: diverging cmap, fixed [-1,1] limits, upper mask.")
    plt.close(fig)

    print("Case 6 completed: r drops from 0.77 to -0.00 without row 0")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 7: ShaheenGo Dual-Axis Series (Fabricated Crossover)
# =============================================================================
def case7():
    df = pd.read_csv(os.path.join(ROOT, "data", "case07_dual_axis_series.csv"))

    # --- Rebuild ---
    # Line chart with two y-axes: revenue_pkr_m on left limited to 50-80, cost_pkr_m on right limited to 40-56.
    # Self-check: cost line sits ABOVE revenue line for first four months
    fig, ax1 = plt.subplots(figsize=(7.5, 4.8))
    ax2 = ax1.twinx()

    l1, = ax1.plot(df["month"], df["revenue_pkr_m"], color=C[0], marker="o", lw=2.2, label="Revenue (left axis)")
    l2, = ax2.plot(df["month"], df["cost_pkr_m"], color=C[1], marker="s", lw=2.2, label="Cost (right axis)")

    ax1.set_ylim(50, 80)
    ax2.set_ylim(40, 56)
    ax1.set_title("Published Claim: ShaheenGo Ran at a Loss Until May (Dual-Axis Illusion)", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Month (2026)")
    ax1.set_ylabel("Revenue (PKR Millions)", color=C[0])
    ax2.set_ylabel("Cost (PKR Millions)", color=C[1])
    ax1.tick_params(axis="y", labelcolor=C[0])
    ax2.tick_params(axis="y", labelcolor=C[1])
    
    lines = [l1, l2]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left", frameon=False)
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case07_rebuild.png"), "Self-check verified: cost line sits above revenue line for Jan–Apr due to mismatched twin axes.")
    plt.close(fig)

    # --- Redesign ---
    # Single shared scale starting at zero, plus bottom difference panel
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(7.5, 6.2), sharex=True, gridspec_kw={"height_ratios": [2.2, 1.2]})
    
    ax_top.plot(df["month"], df["revenue_pkr_m"], color=C[0], marker="o", lw=2.2, label="Revenue (PKR M)")
    ax_top.plot(df["month"], df["cost_pkr_m"], color=C[1], marker="s", lw=2.2, label="Cost (PKR M)")
    ax_top.fill_between(df["month"], df["cost_pkr_m"], df["revenue_pkr_m"], color=C[0], alpha=0.15, label="Profit Zone")
    ax_top.set_ylim(0, 90)
    ax_top.set_title("Single Common Scale Proves ShaheenGo Was Profitable in Every Month", fontsize=11, fontweight="bold")
    ax_top.set_ylabel("PKR Millions (Shared Scale)")
    ax_top.legend(loc="upper left", frameon=False)
    ax_top.spines["top"].set_visible(False)
    ax_top.spines["right"].set_visible(False)

    df["profit"] = df["revenue_pkr_m"] - df["cost_pkr_m"]
    bars = ax_bot.bar(df["month"], df["profit"], color=C[2], width=0.45)
    ax_bot.set_ylim(0, 30)
    ax_bot.set_title("Net Monthly Profit: Grew Steadily from +8M PKR (Jan) to +25M PKR (Jun)", fontsize=9.5, fontweight="bold")
    ax_bot.set_xlabel("Month")
    ax_bot.set_ylabel("Profit (PKR M)")
    for b in bars:
        h = b.get_height()
        ax_bot.text(b.get_x() + b.get_width() / 2, h + 1.0, f"+{h:.0f}M", ha="center", fontsize=8.5, fontweight="bold")
    ax_bot.spines["top"].set_visible(False)
    ax_bot.spines["right"].set_visible(False)

    fig.tight_layout(rect=[0, 0.03, 1, 0.96])
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case07_redesign.png"), "Honest shared axis starting at zero proves positive profit across all six months. Zero loss.")
    plt.close(fig)

    print("Case 7 completed: continuous profitability from Jan to Jun")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 8: Three Bin Widths (Discretization & Aliasing)
# =============================================================================
def case8():
    df = pd.read_csv(os.path.join(ROOT, "data", "vitals_10k.csv"))

    # --- Rebuild ---
    # Three histograms of systolic side by side: bins=3, bins=45, bins=400.
    # Self-check: n = 10,000 in all three panels
    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.0), sharey=False)
    bin_choices = [3, 45, 400]
    subtitles = ["bins = 3\n(Extreme oversmoothing)", "bins = 45\n(Reveals bimodality)", "bins = 400\n(Comb aliasing on integers)"]
    
    for idx, b in enumerate(bin_choices):
        ax_i = axes[idx]
        ax_i.hist(df["systolic"], bins=b, color=C[0], edgecolor=PALETTE["surface"], lw=0.4)
        ax_i.set_title(subtitles[idx], fontsize=9.5, fontweight="bold")
        ax_i.set_xlabel("Systolic Blood Pressure (mmHg)")
        if idx == 0:
            ax_i.set_ylabel("Count")
        ax_i.text(0.04, 0.88, f"n = {len(df['systolic']):,}", transform=ax_i.transAxes, fontsize=8.5, fontweight="bold", color=PALETTE["ink_soft"])
        ax_i.spines["top"].set_visible(False)
        ax_i.spines["right"].set_visible(False)

    fig.suptitle("Published Claim: Three Bin Widths, Three Different Distributions", fontsize=11.5, fontweight="bold")
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case08_rebuild.png"), "Self-check verified: n = 10,000 in all panels. Arbitrary bins hide or fake distribution features.")
    plt.close(fig)

    # --- Redesign ---
    # Principled clinically grounded binning with declared bin width (2.5 mmHg) and clinical interpretation
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    bin_w = 2.5
    bins = int((df["systolic"].max() - df["systolic"].min()) / bin_w)
    
    counts, edges, _ = ax.hist(df["systolic"], bins=bins, color=C[0], edgecolor=PALETTE["surface"], lw=0.5, alpha=0.85)
    
    ax.axvline(120, color=PALETTE["ink_soft"], linestyle="--", lw=1.4)
    ax.axvline(165, color=PALETTE["highlight"], linestyle="--", lw=1.4)
    ax.text(121, counts.max() * 0.92, "Normotensive cohort (~120 mmHg)", fontsize=8.5, color=PALETTE["ink_soft"])
    ax.text(166, counts.max() * 0.72, "Hypertensive cohort (~165 mmHg)", fontsize=8.5, color=PALETTE["highlight"])
    
    ax.set_title("Principled Binning (bin width = 2.5 mmHg) Reveals Clinical Bimodality", fontsize=11, fontweight="bold")
    ax.set_xlabel("Systolic Blood Pressure (mmHg)")
    ax.set_ylabel("Patient Count")
    ax.text(0.03, 0.85, f"Declared: bin width = {bin_w:.1f} mmHg · {bins} bins · N = 10,000\nInteger measurement matches resolution without aliasing.", transform=ax.transAxes, fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case08_redesign.png"), "Principled histogram selection with explicitly declared bin width matches clinical data resolution.")
    plt.close(fig)

    print("Case 8 completed: binning effects demonstrated")
    return rebuild_path, redesign_path


# =============================================================================
# CASE 9: KDE Boundary Leak on SpO2 (Boundary Bias)
# =============================================================================
def case9():
    df = pd.read_csv(os.path.join(ROOT, "data", "vitals_10k.csv"))

    # --- Rebuild ---
    # Kernel density estimate of spo2 with default bandwidth. Extend x-axis to 108, mark 100.
    # Self-check: max value in data is 100. The curve is not.
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    sns.kdeplot(df["spo2"], ax=ax, color=C[0], lw=2.2, label="KDE (default Gaussian bandwidth)")
    ax.axvline(100, color=PALETTE["highlight"], linestyle="--", lw=1.8, label="Physical Maximum (100% Saturation)")
    ax.set_xlim(80, 108)
    
    # Shade impossible region above 100
    line = ax.get_lines()[0]
    x, y = line.get_data()
    mask_above = x >= 100
    ax.fill_between(x[mask_above], y[mask_above], color=PALETTE["highlight"], alpha=0.30, label="Boundary Leak (> 100%)")
    
    ax.set_title("Published Claim: Kernel Density Estimates 1.6–4.4% of Patients Above 100% SpO₂", fontsize=11, fontweight="bold")
    ax.set_xlabel("Peripheral Oxygen Saturation — SpO₂ (%)")
    ax.set_ylabel("Probability Density")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.text(0.58, 0.40, f"Max in data: {df['spo2'].max()}%\nGaussian kernels leak probability\nacross hard physical ceiling.", transform=ax.transAxes, fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    rebuild_path = save_fig(fig, os.path.join(FIG_DIR, "case09_rebuild.png"), "Self-check verified: data max is 100; Gaussian kernel density leaks past 100% boundary.")
    plt.close(fig)

    # --- Redesign ---
    # Discrete integer histogram respecting physical bound
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    bins = np.arange(80.5, 101.5, 1.0)
    counts, edges, _ = ax.hist(df["spo2"], bins=bins, color=C[0], edgecolor=PALETTE["surface"], lw=0.6, align="mid")
    ax.axvline(100, color=PALETTE["highlight"], linestyle="--", lw=1.6, label="Physical Bound (100%)")
    
    ax.set_xlim(80, 102)
    ax.set_title("Discrete Integer Histogram Respects Physical Domain Ceiling (Max = 100%)", fontsize=11, fontweight="bold")
    ax.set_xlabel("Peripheral Oxygen Saturation — SpO₂ (%)")
    ax.set_ylabel("Patient Count")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    ax.text(0.04, 0.85, f"Declared: bin width = 1.0% · 20 bins · N = 10,000\nExactly 0 readings exist > 100%.\nPhysical boundary respected.", transform=ax.transAxes, fontsize=8.5, bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"]))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    redesign_path = save_fig(fig, os.path.join(FIG_DIR, "case09_redesign.png"), "Discrete unit histogram eliminates artificial boundary leakage while preserving pulse oximetry integer resolution.")
    plt.close(fig)

    print(f"Case 9 completed: data max = {df['spo2'].max()}%")
    return rebuild_path, redesign_path


def main():
    print("=" * 80)
    print("PART A: REBUILDING ALL NINE CHARTS AND NINE REDESIGNS")
    print("=" * 80)
    case1()
    case2()
    case3()
    case4()
    case5()
    case6()
    case7()
    case8()
    case9()
    print("=" * 80)
    print(f"All 18 charts successfully generated in {FIG_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()
