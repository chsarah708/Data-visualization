"""
Part B — Lie Factor, in code (15 marks)

Tufte's Lie Factor:
                effect shown in the graphic
Lie Factor  =  ─────────────────────────────        effect = (final − initial) / initial
                   effect in the data

Honest is 1.0. Tufte accepts 0.95 – 1.05.
"""

from __future__ import annotations

import os
import sys
import pandas as pd

# Add parent directory to path to import vizlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vizlib import lie_factor, lie_verdict


def run_part_b():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "case07_lie_factor.csv")
    df = pd.read_csv(data_path)

    print("=" * 80)
    print("PART B: LIE FACTOR AUDIT (COMPUTED IN PYTHON)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Question 1: Compute table of data effect, graphic effect, Lie Factor, verdict (5 marks)
    # -------------------------------------------------------------------------
    print("\n--- Question 1: Lie Factor Audit Table (Graphics A-E) ---\n")
    
    results = []
    for _, row in df.iterrows():
        lf, de, ge = lie_factor(
            row.value_start,
            row.value_end,
            row.ink_start,
            row.ink_end,
            ink_dimension=int(row.ink_dimension)
        )
        verdict = lie_verdict(lf)
        results.append({
            "Chart": row.chart_id,
            "Subject": row.subject,
            "Value Start": row.value_start,
            "Value End": row.value_end,
            "Data Effect": f"{de:+.4f} ({de*100:+.1f}%)",
            "Ink Start": f"{row.ink_start} {row.ink_unit}",
            "Ink End": f"{row.ink_end} {row.ink_unit}",
            "Dim": row.ink_dimension,
            "Graphic Effect": f"{ge:+.4f} ({ge*100:+.1f}%)",
            "Lie Factor": f"{lf:.3f}",
            "Verdict": verdict
        })

    res_df = pd.DataFrame(results)
    # Format table nicely
    print(f"{'Chart':<6} {'Subject':<30} {'Data Effect':<18} {'Graphic Effect':<20} {'Lie Factor':<12} {'Verdict'}")
    print("-" * 105)
    for r in results:
        print(f"{r['Chart']:<6} {r['Subject']:<30} {r['Data Effect']:<18} {r['Graphic Effect']:<20} {r['Lie Factor']:<12} {r['Verdict']}")
    print("-" * 105)

    # -------------------------------------------------------------------------
    # Question 2: Exactly one is honest. Say which, and what others do wrong (3 marks)
    # -------------------------------------------------------------------------
    print("\n--- Question 2: Audit of Honest vs. Distorted Graphics ---\n")
    print(
        "• Honest Graphic: Chart C (Export earnings) is the ONLY honest graphic (Lie Factor = 1.000).\n"
        "  Its bars originate from a true zero baseline, and ink length scales in strict 1:1 proportion\n"
        "  to the 20.0% data increase ($25B -> $30B, ink 5.0cm -> 6.0cm).\n\n"
        "• Distortions in the other four graphics:\n"
        "  - Chart A (Corporate tax rate, LF = 75.000): Severe truncation of the baseline. Bars are drawn\n"
        "    from a 29.6% baseline instead of zero, displaying only the tips. A modest 6.67% rate increase\n"
        "    (30% -> 32%) is depicted as a 500.0% ink explosion (4mm -> 24mm), exaggerating reality 75-fold.\n"
        "  - Chart B (Federal health budget, LF = 2.500): 2D area encoding of a 1D scalar. Sizing both\n"
        "    height and width of a coin icon by 1.5x for a 50% budget increase (Rs 40B -> 60B) squares the visual\n"
        "    surface area (1.5^2 = 2.25x ink, +125% graphic effect), exaggerating the increase 2.5 times.\n"
        "  - Chart D (Air-pollution index, LF = 0.250): Compressed baseline / downward offset. A 50.0% rise\n"
        "    in air pollution (100 -> 150) is encoded as only a 12.5% bar height increase (8.0cm -> 9.0cm),\n"
        "    understating the pollution surge by a factor of 4 (LF = 0.25).\n"
        "  - Chart E (City population, LF = 5.000): Bubble radius scaling. Encoding a 300.0% population\n"
        "    growth (2M -> 8M, a 4x factor) by scaling bubble RADIUS 4x results in area scaling by 4^2 = 16x\n"
        "    (+1500.0% ink area), exaggerating growth 5-fold."
    )

    # -------------------------------------------------------------------------
    # Question 3: ink_dimension=2 graphics and what goes wrong if left at 1 (3 marks)
    # -------------------------------------------------------------------------
    print("\n--- Question 3: Dimensionality of Ink (ink_dimension=2) ---\n")
    print(
        "• Graphics requiring ink_dimension=2: Chart B (coin icon) and Chart E (bubble graphic).\n"
        "  Both represent data magnitudes using two-dimensional visual surface area rather than a 1D line/bar length.\n\n"
        "• What goes wrong if left at ink_dimension=1:\n"
        "  If ink_dimension is left at 1, the formula incorrectly assumes the reader's eye perceives only the 1D linear\n"
        "  dimension (diameter or radius) rather than the 2D surface area (ink ~ r^2); for Chart B this would falsely\n"
        "  report an honest Lie Factor of 1.00 (ignoring the 2.25x area expansion), and for Chart E it would report\n"
        "  a Lie Factor of 1.00 instead of the true 5.00x visual area distortion."
    )

    # -------------------------------------------------------------------------
    # Question 4: Lie Factor below 1, distortion rationale, and beneficiaries (2 marks)
    # -------------------------------------------------------------------------
    print("\n--- Question 4: Understated Lie Factor (LF < 1) ---\n")
    print(
        "• Why an understated chart is still a distortion:\n"
        "  Visual integrity requires faithful proportionality in both directions; understating a magnitude\n"
        "  lulls the viewer into false complacency by suppressing the true scale of growth, creating a visual\n"
        "  perception that change is minor when it is substantial.\n\n"
        "• Who benefits:\n"
        "  Polluting industries, municipal regulators, or environmental agencies benefit from Chart D because\n"
        "  understating a severe 50% spike in hazardous smog (100 -> 150 AQI) as an almost imperceptible bump (8cm -> 9cm)\n"
        "  minimizes public outcry, evades regulatory scrutiny, and shields polluters from liability."
    )

    # -------------------------------------------------------------------------
    # Question 5: Chart F (dual-axis series) Lie Factor audit and reality (2 marks)
    # -------------------------------------------------------------------------
    print("\n--- Question 5: Chart F (Dual-Axis Chart) Audit & Reality ---\n")
    dual_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "case07_dual_axis_series.csv")
    df_dual = pd.read_csv(dual_path)
    df_dual["profit_pkr_m"] = df_dual["revenue_pkr_m"] - df_dual["cost_pkr_m"]
    
    print(
        "• Can we compute Lie Factor for Chart F? No, Lie Factor is mathematically undefined for this chart.\n"
        "  Tufte's Lie Factor formula strictly assumes a single physical coordinate system mapping a univariate\n"
        "  quantity to ink length or area relative to a fixed baseline.\n"
        "  In Chart F, two independent y-axes with mismatched scales and offsets (revenue 50-80 PKR M, cost 40-56 PKR M)\n"
        "  are superimposed. The apparent physical distance between the two lines and their intersection point are\n"
        "  purely arbitrary artifacts of how the designer tuned the two axis limits.\n"
        "  If one attempts to evaluate the difference (Profit = Revenue - Cost):\n"
        "  In January, the real data difference is POSITIVE (+8M PKR), but on the graphic the cost line is drawn\n"
        "  visually ABOVE revenue (a negative visual difference). A positive real effect mapped to a negative visual effect\n"
        "  yields an absurd negative Lie Factor that breaks the ratio metric.\n\n"
        "• What the data actually shows:\n"
        "  ShaheenGo was NEVER running at a loss. It was solidly profitable in EVERY single month:\n"
    )
    for _, r in df_dual.iterrows():
        print(f"    - {r['month']}: Revenue = {r['revenue_pkr_m']}M PKR, Cost = {r['cost_pkr_m']}M PKR -> Profit = +{r['profit_pkr_m']}M PKR")
    print(
        f"  Profits expanded continuously from +8M PKR in Jan to +25M PKR in June.\n"
        f"  The claim that 'ShaheenGo ran at a loss until May' is a total fabrication engineered by dual-axis manipulation."
    )
    print("=" * 80)


if __name__ == "__main__":
    run_part_b()
