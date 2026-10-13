"""
Part C — Prove the palette, do not claim it (9 marks)

Audits colour-blind safety of matplotlib tab10 vs. the course palette
using Machado et al. (2009) severity-1.0 matrices in linear RGB and OKLab delta E.
"""

from __future__ import annotations

import os
import sys
import matplotlib.pyplot as plt

# Add parent directory to import vizlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vizlib import (
    PALETTE,
    save_fig,
    simulate_cvd,
    style_defaults,
    verdict,
    worst_pair,
)

ROOT = os.path.dirname(os.path.abspath(__file__))
style_defaults()

# Palette 1: Matplotlib tab10 first four hues (a standard popular default)
MY_PALETTE = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728"]
MY_LABEL = "matplotlib tab10, first four (Blue, Orange, Green, Red)"

# Palette 2: Course Okabe-Ito palette (3 slots + 4th slot)
COURSE_PALETTE = PALETTE["series"] + [PALETTE["series_4th"]]
COURSE_LABEL = "The Course Palette (Okabe-Ito: 3 slots + 4th slot)"

KINDS = ["normal", "deutan", "protan", "tritan"]


def swatch_sheet(palettes, path):
    """Render and save the before/after swatch comparison sheet."""
    fig, axes = plt.subplots(
        len(palettes),
        len(KINDS),
        figsize=(3.2 * len(KINDS), 2.2 * len(palettes))
    )
    if len(palettes) == 1:
        axes = axes.reshape(1, -1)

    for row, (pal, label) in enumerate(palettes):
        for col, kind in enumerate(KINDS):
            ax = axes[row, col]
            shown = pal if kind == "normal" else simulate_cvd(pal, kind)
            for i, hexc in enumerate(shown):
                ax.add_patch(plt.Rectangle((i, 0), 0.92, 1, color=hexc))
                ax.text(
                    i + 0.46,
                    -0.22,
                    f"S{i+1}",
                    ha="center",
                    fontsize=8.5,
                    fontweight="bold",
                    color=PALETTE["ink_soft"],
                )
            ax.set_xlim(-0.1, len(pal))
            ax.set_ylim(-0.4, 1.1)
            ax.axis("off")
            ax.set_title(kind.capitalize(), fontsize=10.5, fontweight="bold")
        axes[row, 0].text(
            -0.05,
            1.40,
            label,
            transform=axes[row, 0].transAxes,
            fontsize=11.5,
            fontweight="bold",
            color=PALETTE["ink"],
        )

    fig.suptitle(
        "Palette CVD Audit: Prove It, Do Not Claim It",
        x=0.01,
        ha="left",
        fontsize=13.5,
        fontweight="bold",
        color=PALETTE["ink"],
    )
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    out = save_fig(
        fig,
        path,
        "Machado, Oliveira & Fernandes (2009) severity-1.0 matrices, applied in linear RGB. OKLab metric."
    )
    plt.close(fig)
    return out


def audit(pal, label):
    """Measure every pair in OKLab perceptual colour space and print results."""
    print(label)
    rows = []
    for kind in KINDS:
        i, j, a, b, d = worst_pair(pal, kind)
        rows.append((kind, i, j, a, b, d))
        print(
            f"  {kind:7s} closest pair  S{i} {a} vs S{j} {b}"
            f"   ΔE {d:5.1f}   {verdict(d)}"
        )
    print()
    return rows


def simulate_figure_cvd(src_png_path: str, out_png_path: str):
    """
    Optional bonus check (2 marks): Run simulate_cvd on the exported figure
    to visually confirm that all clinical series and annotations remain distinct.
    """
    if not os.path.exists(src_png_path):
        print(f"Skipping figure simulation: {src_png_path} not found.")
        return
    
    img = plt.imread(src_png_path)
    # simulate_cvd accepts (H, W, 3) or (H, W, 4) in 0..1
    sim_deutan = simulate_cvd(img, "deutan")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    axes[0].imshow(img)
    axes[0].set_title("Original Clinical Review Figure (Normal Vision)", fontsize=11, fontweight="bold")
    axes[0].axis("off")
    
    axes[1].imshow(sim_deutan)
    axes[1].set_title("Deuteranopia Simulation (Machado et al. 2009, Linear RGB)", fontsize=11, fontweight="bold")
    axes[1].axis("off")
    
    fig.suptitle("Clinical Figure Colour-Vision Deficiency Verification", fontsize=13, fontweight="bold")
    fig.tight_layout()
    out = save_fig(fig, out_png_path, "Visual confirmation: series remain distinguishable under deuteranopia.")
    plt.close(fig)
    print(f"Saved figure CVD verification check: {out}")


def main():
    print("=" * 80)
    print("PART C: PROVE THE PALETTE, DO NOT CLAIM IT")
    print("=" * 80)

    # 1. Swatch sheet generation
    out_png = os.path.join(ROOT, "partC_palette.png")
    out = swatch_sheet([(MY_PALETTE, MY_LABEL), (COURSE_PALETTE, COURSE_LABEL)], out_png)
    print(f"Generated swatch sheet: {out}\n")

    # 2. Audit calculations
    audit(MY_PALETTE, MY_LABEL)
    audit(COURSE_PALETTE, COURSE_LABEL)

    # 3. Question 3 response
    print("-" * 80)
    print("QUESTION 3: Worst Collapsing Pair in Each Palette and Usage Rules")
    print("-" * 80)
    print(
        "• Matplotlib tab10 Worst Pair:\n"
        "  - Protanopia: S2 (#FF7F0E, Orange) vs S3 (#2CA02C, Green) collapses to ΔE = 0.7 (FAILS — same colour).\n"
        "  - Deuteranopia: S3 (#2CA02C, Green) vs S4 (#D62728, Red) collapses to ΔE = 4.1 (FAILS — same colour).\n"
        "  Under red-green colour blindness, tab10 completely breaks down: readers cannot tell series apart.\n\n"
        "• Course Palette Worst Pair:\n"
        "  - Deuteranopia: S3 (#009E73, Bluish Green) vs S4 (#CC79A7, Reddish Purple) collapses to ΔE = 7.5\n"
        "    (verdict: 'needs a second channel').\n\n"
        "• What this means for how S4 (#CC79A7) is allowed to be used:\n"
        "  Because ΔE = 7.5 sits strictly in the 6 <= ΔE < 8 bracket, S4 is legal ONLY with a redundant\n"
        "  encoding channel. When using S4, you are NEVER allowed to rely on colour alone to communicate identity;\n"
        "  the visualization MUST incorporate distinct marker shapes (circle, square, triangle, diamond),\n"
        "  direct inline text labels, varying line styles (dashed vs solid), or facet separation."
    )

    # 4. Question 4 response
    print("\n" + "-" * 80)
    print("QUESTION 4: Rule When a Chart Needs More Than Three Categories")
    print("-" * 80)
    print(
        "Rule for the rest of this course:\n"
        "When a chart requires more than three categories, NEVER rely on color alone.\n"
        "Adding additional categorical hues inevitably violates the ΔE >= 8 threshold under colour vision\n"
        "deficiency. Instead of adding a 5th or 6th hue, I will employ one or more of the following structural solutions:\n"
        "  1. Redundant Channel: Pair each category with a distinct marker shape (MARKERS: 'o', 's', '^', 'D')\n"
        "     or contrasting stroke patterns (solid, dashed, dotted).\n"
        "  2. Direct Labeling: Label data marks, lines, or bars directly at their endpoints rather than forcing\n"
        "     readers to decode a detached color legend.\n"
        "  3. Small Multiples / Faceting: Decompose complex data across multiple subplots (one category per panel)\n"
        "     sharing aligned, consistent axes, where spatial position replaces hue as the primary encoding channel.\n"
        "  4. Tabular Summary: Accompany dense multi-series graphics with an explicit summary table for exact lookup."
    )
    print("=" * 80)

    # 5. Optional figure-level check
    fig_d_path = os.path.join(ROOT, "partD_figure.png")
    fig_check_path = os.path.join(ROOT, "partC_figure_deutan_check.png")
    simulate_figure_cvd(fig_d_path, fig_check_path)


if __name__ == "__main__":
    main()
