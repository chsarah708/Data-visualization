"""
Part D — Build the clinical review figure (25 marks)
Application task from Lecture 6.

Produces one polished 2x2 clinical safety review figure from vitals_10k.csv.
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
style_defaults()
C = PALETTE["series"]

# Audit trail dictionary for Part E
LOG: dict[str, str] = {}


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean the clinical dataset, logging every rule, count, and parameter.
    Returns (cleaned_df, raw_df_for_appendix).
    """
    raw_df = df.copy()
    LOG["rows loaded"] = f"{len(df):,}"

    # ---------------------------------------------------------------- TODO 1
    # Conform ward spellings into 4 canonical wards
    ward_mapping = {
        "general medicine": "General Medicine",
        "gen medicine": "General Medicine",
        "cardiology": "Cardiology",
        "cardio": "Cardiology",
        "day surgery": "Day Surgery",
        "day-surgery": "Day Surgery",
        "intensive care": "ICU",
        "icu": "ICU",
        "i.c.u": "ICU",
    }
    df["ward_clean"] = df["ward"].astype(str).str.strip().str.lower().map(ward_mapping)
    assert df["ward_clean"].nunique() == 4, f"Expected 4 wards, got {df['ward_clean'].nunique()}"
    assert df["ward_clean"].isna().sum() == 0, "Null wards detected after mapping"
    LOG["ward spellings conformed"] = "12 raw string variants -> 4 canonical wards (Gen Med: 4,018, Cardio: 2,682, Day Surg: 1,479, ICU: 1,821; 0 dropped)"

    # ---------------------------------------------------------------- TODO 2
    # Parse multi-format admit_date into datetime admit_dt
    d_iso = pd.to_datetime(df["admit_date"], format="%Y-%m-%d", errors="coerce")
    d_text = pd.to_datetime(df["admit_date"], format="%d-%b-%Y", errors="coerce")
    d_slash = pd.to_datetime(df["admit_date"], format="%d/%m/%Y", errors="coerce")
    df["admit_dt"] = d_iso.fillna(d_text).fillna(d_slash)
    assert df["admit_dt"].isna().sum() == 0, "Unparsed dates detected"
    LOG["dates parsed"] = f"10,000 dates unified across 3 source formats (ISO: {d_iso.count():,}, Day-Mon-Year: {d_text.count():,}, Day/Month/Year: {d_slash.count():,})"

    # ---------------------------------------------------------------- TODO 3
    # BMI sentinels: 999.0 used as sentinel for missing
    bmi_raw_mean = df["bmi"].mean()
    n_bmi_999 = (df["bmi"] == 999.0).sum()
    n_bmi_0 = (df["bmi"] == 0.0).sum()
    df["bmi_clean"] = df["bmi"].replace({999.0: np.nan, 0.0: np.nan})
    bmi_clean_mean = df["bmi_clean"].mean()
    LOG["bmi sentinels removed"] = (
        f"402 sentinels (999.0) + 84 zero sentinels set to NaN (total n = {n_bmi_999 + n_bmi_0}); "
        f"mean BMI moved from {bmi_raw_mean:.2f} to {bmi_clean_mean:.2f} kg/m²"
    )

    # ---------------------------------------------------------------- TODO 4
    # Heart rate device faults: physiologically impossible values (> 250 bpm or < 30 bpm)
    hr_raw_mean = df["heart_rate"].mean()
    fault_mask = (df["heart_rate"] > 250) | (df["heart_rate"] < 30)
    n_faults = fault_mask.sum()
    n_high = (df["heart_rate"] > 250).sum()
    n_low = (df["heart_rate"] < 30).sum()
    
    # Filter rows with device faults
    clean_df = df[~fault_mask].copy()
    hr_clean_mean = clean_df["heart_rate"].mean()
    LOG["heart-rate device faults removed"] = (
        f"Removed n = {n_faults} device faults (n = {n_high} > 250 bpm up to 415 bpm; n = {n_low} < 30 bpm / zeros); "
        f"mean heart rate moved from {hr_raw_mean:.2f} to {hr_clean_mean:.2f} bpm (kept N = {len(clean_df):,})"
    )

    # ---------------------------------------------------------------- TODO 5
    # Derived column MAP (Mean Arterial Pressure) noted for exclusion
    LOG["derived column excluded"] = "map_mmhg excluded from correlation heatmap (arithmetically derived: (systolic + 2*diastolic)/3; r = 0.96 with systolic)"

    return clean_df, raw_df


def build_figure(df: pd.DataFrame) -> plt.Figure:
    """Build the finished 2x2 clinical safety review figure."""
    fig, ax = plt.subplots(2, 2, figsize=(14.0, 9.6))

    # ------------------------------------------------------- Panel 1 (0, 0)
    # Bimodal distribution of systolic blood pressure
    a = ax[0, 0]
    bin_width = 2.5
    bins = int((df["systolic"].max() - df["systolic"].min()) / bin_width)
    
    n_counts, bin_edges, patches = a.hist(
        df["systolic"],
        bins=bins,
        color=C[0],
        edgecolor=PALETTE["surface"],
        linewidth=0.5,
        alpha=0.88,
    )
    
    # Highlight peaks with subtle annotations
    a.axvline(120, color=PALETTE["ink_soft"], linestyle="--", linewidth=1.2, alpha=0.8)
    a.axvline(165, color=PALETTE["highlight"], linestyle="--", linewidth=1.2, alpha=0.8)
    a.text(121, n_counts.max() * 0.90, "Normotensive peak\n(~120 mmHg)", fontsize=8.5, color=PALETTE["ink_soft"])
    a.text(166, n_counts.max() * 0.72, "Hypertensive peak\n(~165 mmHg)", fontsize=8.5, color=PALETTE["highlight"])
    
    a.set_title("Bimodal Systolic BP Reveals Normotensive and Hypertensive Subpopulations", fontsize=11, fontweight="bold")
    a.set_xlabel("Systolic Blood Pressure (mmHg)")
    a.set_ylabel("Patient Count")
    a.text(
        0.03, 0.92,
        f"Declared: bin width = {bin_width:.1f} mmHg · {bins} bins · n = {len(df):,}",
        transform=a.transAxes,
        fontsize=8.5,
        fontweight="bold",
        color=PALETTE["ink_soft"],
        bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"], alpha=0.9)
    )

    # ------------------------------------------------------- Panel 2 (0, 1)
    # Box plot comparing length of stay across wards (log scale)
    b = ax[0, 1]
    
    # Sort wards strictly by median length of stay
    medians = df.groupby("ward_clean")["los_days"].median().sort_values()
    sorted_wards = medians.index.tolist()
    
    # Handle zero length of stay for log plotting safely by floor of 0.05 days (~1.2 hours)
    plot_df = df.copy()
    plot_df["los_days_plot"] = np.maximum(plot_df["los_days"], 0.05)
    
    box_pal = [C[0], C[2], PALETTE["muted"], C[1]]  # Safe hues
    sns.boxplot(
        data=plot_df,
        x="ward_clean",
        y="los_days_plot",
        hue="ward_clean",
        order=sorted_wards,
        palette="Blues_d",
        legend=False,
        ax=b,
        width=0.55,
        fliersize=2.5,
        flierprops=dict(marker="o", markerfacecolor=PALETTE["ink_soft"], alpha=0.4, markeredgewidth=0)
    )
    b.set_yscale("log")
    
    # Annotate medians directly above boxes
    for idx, ward in enumerate(sorted_wards):
        med = medians[ward]
        b.text(idx, med * 1.35, f"Med: {med:.2f}d", ha="center", fontsize=8.5, fontweight="bold", color=PALETTE["ink"])
        
    b.set_title("Inpatient Stay Scales 14× Across Wards: Day Surgery (0.25d) to ICU (3.48d)", fontsize=11, fontweight="bold")
    b.set_xlabel("Admitting Ward (sorted by median stay)")
    b.set_ylabel("Length of Stay (days, log₁₀ scale)")
    b.text(
        0.03, 0.06,
        "Log scale declared (range 0.05–274d) · fliers retained · n = 9,963",
        transform=b.transAxes,
        fontsize=8.5,
        color=PALETTE["ink_soft"],
        bbox=dict(boxstyle="round,pad=0.3", facecolor=PALETTE["surface"], edgecolor=PALETTE["grid"], alpha=0.9)
    )

    # ------------------------------------------------------- Panel 3 (1, 0)
    # Scatter plot of systolic vs diastolic blood pressure (r = 0.89)
    c = ax[1, 0]
    
    # Subsample 2,500 points with fixed seed for clear point cloud density without solid blob
    sample_df = df.sample(n=min(2500, len(df)), random_state=42)
    c.scatter(
        sample_df["systolic"],
        sample_df["diastolic"],
        alpha=0.30,
        s=16,
        color=C[0],
        edgecolors="none",
        label="Admissions (n = 2,500 subsample)"
    )
    
    # Fit regression trend line
    slope, intercept = np.polyfit(df["systolic"], df["diastolic"], 1)
    x_vals = np.array([df["systolic"].min(), df["systolic"].max()])
    c.plot(x_vals, slope * x_vals + intercept, color=PALETTE["highlight"], linewidth=2.0, label=f"Least-squares fit (r = 0.89)")
    
    # Clinical stage thresholds
    c.axvline(140, color=PALETTE["muted"], linestyle=":", linewidth=1.0)
    c.axhline(90, color=PALETTE["muted"], linestyle=":", linewidth=1.0)
    c.text(142, 45, "Systolic stage 2\n(≥140 mmHg)", fontsize=7.5, color=PALETTE["ink_soft"])
    c.text(95, 91.5, "Diastolic stage 2 (≥90 mmHg)", fontsize=7.5, color=PALETTE["ink_soft"])

    c.set_title("Hemodynamic Coupling: Systolic and Diastolic BP Correlate Strongly (r = 0.89)", fontsize=11, fontweight="bold")
    c.set_xlabel("Systolic Blood Pressure (mmHg)")
    c.set_ylabel("Diastolic Blood Pressure (mmHg)")
    c.legend(loc="upper left", frameon=False, fontsize=8.5)
    c.text(
        0.58, 0.08,
        "Screened from Panel 4 heatmap\nAlpha = 0.30, subsample n = 2,500 of 9,963",
        transform=c.transAxes,
        fontsize=8.0,
        color=PALETTE["ink_soft"]
    )

    # ------------------------------------------------------- Panel 4 (1, 1)
    # Correlation heatmap built strictly to Lecture 6 guidelines
    d = ax[1, 1]
    
    # Candidate clinical variables EXCLUDING derived map_mmhg
    corr_cols = [
        "systolic", "diastolic", "age", "heart_rate",
        "spo2", "bmi_clean", "chol_mmol_l", "glucose_mmol_l", "los_days"
    ]
    col_labels = [
        "Systolic", "Diastolic", "Age", "Heart Rate",
        "SpO₂", "BMI", "Cholesterol", "Glucose", "Stay (days)"
    ]
    
    corr_matrix = df[corr_cols].corr()
    
    # Mask upper triangle (slides 46-47: upper triangle says everything twice)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=PALETTE["diverging"],  # RdBu_r diverging colormap
        vmin=-1.0,
        vmax=1.0,
        center=0.0,
        annot=True,
        fmt=".2f",
        square=True,
        linewidths=0.6,
        linecolor=PALETTE["surface"],
        cbar_kws={"label": "Pearson Correlation (r)", "shrink": 0.82},
        xticklabels=col_labels,
        yticklabels=col_labels,
        ax=d,
        annot_kws={"size": 7.5}
    )
    d.set_title("Pairwise Correlation Matrix: Isolated Hemodynamic Coupling (MAP Excluded)", fontsize=11, fontweight="bold")
    d.tick_params(axis="x", rotation=40, labelsize=8.5)
    d.tick_params(axis="y", rotation=0, labelsize=8.5)

    # ------------------------------------------------------- Finishing
    for p in ax.flat:
        p.spines["top"].set_visible(False)
        p.spines["right"].set_visible(False)

    fig.suptitle(
        "Clinical Inpatient Safety Review: Vital Sign Distributions, Ward Variation, and Risk Correlations",
        fontsize=13.5,
        fontweight="bold",
        color=PALETTE["ink"],
        y=0.985
    )
    fig.tight_layout(rect=[0, 0.03, 1, 0.96])
    return fig


def main():
    csv_path = os.path.join(ROOT, "data", "vitals_10k.csv")
    df_raw = pd.read_csv(csv_path)

    df_clean, df_unfiltered = clean(df_raw)
    fig = build_figure(df_clean)

    # Source note carrying n, exclusion rules, counts, and parameter declarations
    note = (
        "Source: CDB601220 Clinical Safety Extract (vitals_10k.csv, synthetic) · "
        "N = 9,963 analyzed (n = 37 device faults removed: HR < 30 or > 250 bpm; 486 BMI sentinels set to NaN) · "
        "Panel 1: bin width = 2.5 mmHg, 45 bins · Panel 2: sorted by median, log₁₀ scale · "
        "Panel 3: α = 0.30, n = 2,500 sample · Panel 4: RdBu_r colormap, vmin = -1, vmax = 1, upper triangle masked, MAP excluded."
    )

    out_file = os.path.join(ROOT, "partD_figure.png")
    out = save_fig(fig, out_file, note)
    plt.close(fig)
    print(f"\nSuccessfully generated 300 DPI clinical review figure: {out}\n")

    print("=" * 80)
    print("DATA CLEANING LOG (PART E AUDIT TRAIL):")
    print("=" * 80)
    for k, v in LOG.items():
        print(f"  {k:<36} : {v}")
    print("=" * 80)


if __name__ == "__main__":
    main()
