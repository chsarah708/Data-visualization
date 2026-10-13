"""
Generate partE_justification.pdf using ReportLab.
MUST BE EXACTLY ONE PAGE.
Covers:
1. Per-panel questions, chart types, Week 2 channel rules (6 marks)
2. Every parameter chosen, named and defended (5 marks)
3. Every row removed, rule, count, before/after numbers, and ethics clause (4 marks)
"""

from __future__ import annotations

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

ROOT = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(ROOT, "partE_justification.pdf")


def build_pdf():
    # Target: Exactly 1 page (792 pt height, 612 pt width)
    # Margins: 24 pt all around -> printable height 744 pt
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=24,
        rightMargin=24,
        topMargin=22,
        bottomMargin=22
    )

    styles = getSampleStyleSheet()
    
    header_title = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#16202E"),
    )
    header_meta = ParagraphStyle(
        "HeaderMeta",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#5B6573"),
    )
    section_title = ParagraphStyle(
        "SecTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0072B2"),
        spaceBefore=3,
        spaceAfter=2,
    )
    item_title = ParagraphStyle(
        "ItemTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#16202E"),
    )
    body_text = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=6.8,
        leading=8.6,
        textColor=colors.HexColor("#16202E"),
    )
    ethics_box = ParagraphStyle(
        "EthicsBox",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=6.8,
        leading=8.6,
        textColor=colors.HexColor("#16202E"),
    )

    story = []

    # Title & Metadata Header
    story.append(Paragraph("Part E — Design Justification & Data Ethics Audit (Clinical Safety Review)", header_title))
    story.append(Paragraph(
        "<b>Student:</b> Muhammad Maheem &nbsp;|&nbsp; <b>ID:</b> SU92-BSAIM-F24-054 &nbsp;|&nbsp; "
        "<b>Course:</b> CDB601220 Data Visualization &nbsp;|&nbsp; <b>Dataset:</b> vitals_10k.csv (Synthetic Clinical Safety Extract)",
        header_meta
    ))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.0, color=colors.HexColor("#0072B2"), spaceAfter=3))

    # -------------------------------------------------------------------------
    # Section 1: Per-Panel Architecture & Channel Rules (6 marks)
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Per-Panel Architecture: Clinical Questions, Chart Choices, and Perceptual Channels (6 Marks)", section_title))
    
    panel_data = [
        [
            Paragraph("<b>Panel 1 (0,0): Distribution of Systolic BP</b>", item_title),
            Paragraph("<b>Question:</b> Does systolic blood pressure follow a unimodal distribution, or does it reveal distinct risk sub-populations?<br/>"
                      "<b>Chart Choice:</b> Frequency histogram with declared bin width (2.5 mmHg, 45 bins).<br/>"
                      "<b>Channel Rule:</b> Position along a common horizontal scale (Cleveland & McGill Rank 1) for magnitude; bar height/area encodes frequency. Avoids the boundary leakage and artificial smoothing of Gaussian KDEs, exposing clinical bimodality (~120 and ~165 mmHg).", body_text)
        ],
        [
            Paragraph("<b>Panel 2 (0,1): Ward Length of Stay Comparison</b>", item_title),
            Paragraph("<b>Question:</b> How does inpatient length of stay (LOS) vary systematically across admitting wards?<br/>"
                      "<b>Chart Choice:</b> Ordered box plot on a log₁₀ scale (sorted by median stay) with explicit fliers displayed.<br/>"
                      "<b>Channel Rule:</b> Spatial position along an aligned vertical scale (Rank 1) encoding median and IQR. Log scaling accommodates severe right skew (0.05 to 274 days) without collapsing boxes, while preserving all outliers (no deceptive <code>showfliers=False</code>).", body_text)
        ],
        [
            Paragraph("<b>Panel 3 (1,0): Hemodynamic BP Coupling Scatter</b>", item_title),
            Paragraph("<b>Question:</b> Do systolic and diastolic pressures correlate tightly, and how do admissions cluster against clinical hypertension cutoffs?<br/>"
                      "<b>Chart Choice:</b> Scatter plot with alpha transparency (α = 0.30, n = 2,500 subsample) and least-squares regression line.<br/>"
                      "<b>Channel Rule:</b> Position in 2D Cartesian space (Rank 1). Alpha blending encodes point density without occlusive ink blobs; color highlight emphasizes the strong physiological coupling (r = 0.89) identified in Panel 4.", body_text)
        ],
        [
            Paragraph("<b>Panel 4 (1,1): Screening Correlation Heatmap</b>", item_title),
            Paragraph("<b>Question:</b> Which physiological vital signs and lab markers exhibit genuine pairwise linear associations across the cohort?<br/>"
                      "<b>Chart Choice:</b> Lower-triangle annotated matrix heatmap using diverging colormap (<code>RdBu_r</code>, range [-1, 1]).<br/>"
                      "<b>Channel Rule:</b> Color saturation and diverging hue centered at 0.0 (Wilke Ch. 4). Upper triangle masked to eliminate 50% duplicate scanning; direct numeric text annotations provide exact lookup without perceptual estimation error.", body_text)
        ],
    ]
    t_panel = Table(panel_data, colWidths=[150, 414])
    t_panel.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DFE6EE")),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F4F7FA")),
        ("TOPPADDING", (0, 0), (-1, -1), 2.0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t_panel)
    story.append(Spacer(1, 3))

    # -------------------------------------------------------------------------
    # Section 2: Defended Parameter Decisions (5 marks)
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Parameter Decisions: Explicit Nominations and Defenses (5 Marks)", section_title))
    
    param_text = (
        "• <b><code>bin_width = 2.5 mmHg</code> (45 bins):</b> Selected to match the natural integer resolution of clinical sphygmomanometers. Prevents the severe oversmoothing of <code>bins=3</code> (which conceals the bimodal peaks) and eliminates the comb aliasing of <code>bins=400</code> (where 74% of bins are empty due to fractional binning on integers).<br/>"
        "• <b><code>order = ['Day Surgery', 'General Medicine', 'Cardiology', 'ICU']</code>:</b> Wards sorted strictly by empirical median stay (0.25d < 1.26d < 1.69d < 3.48d). Eliminates uninformative alphabetical ordering and exposes the 14× acuity progression across services.<br/>"
        "• <b><code>yscale('log')</code> with floor = 0.05d:</b> Length of stay spans four orders of magnitude (0 to 273.7 days). On a linear scale, 75% of data (<2.57d) collapses into a hairline. Log scaling gives equal visual resolution across all IQRs while keeping extreme long-stay outliers visible.<br/>"
        "• <b><code>subsample n = 2,500</code> with <code>alpha = 0.30</code>:</b> 10,000 raw points create an impenetrable black mass. Subsampling 25% with 30% opacity resolves the bivariate density gradient and avoids over-ink saturation while maintaining identical Pearson r (0.89).<br/>"
        "• <b><code>cmap='RdBu_r'</code>, <code>vmin=-1.0</code>, <code>vmax=1.0</code>, <code>center=0.0</code>, <code>mask=upper_tri</code>:</b> Pearson r is a signed metric (-1 to +1). Diverging color with a neutral white midpoint at 0 prevents misreading negative correlations as zero (the fatal flaw of sequential <code>Reds</code>). Upper triangle mask halves visual clutter (190 vs 400 cells)."
    )
    story.append(Paragraph(param_text, body_text))
    story.append(Spacer(1, 3))

    # -------------------------------------------------------------------------
    # Section 3: Data Cleaning Log & Ethics Clause (4 marks)
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Data Cleaning Log, Row Removal Rules, and Ethics Clause (4 Marks)", section_title))
    
    cleaning_table = [
        [
            Paragraph("<b>Target Variable</b>", item_title),
            Paragraph("<b>Data Cleaning Rule & Justification</b>", item_title),
            Paragraph("<b>Count Affected</b>", item_title),
            Paragraph("<b>Before -> After Metric Shift</b>", item_title)
        ],
        [
            Paragraph("<b>Ward Names</b>", body_text),
            Paragraph("Strip whitespace, lowercase, map 12 raw spelling variants to 4 canonical wards (Gen Med, Cardio, Day Surg, ICU).", body_text),
            Paragraph("n = 10,000 conformed (0 dropped)", body_text),
            Paragraph("Wards: 12 variants -> 4 canonical (Gen Med 4,018, Cardio 2,682, Day Surg 1,479, ICU 1,821)", body_text)
        ],
        [
            Paragraph("<b>Admit Dates</b>", body_text),
            Paragraph("Unified 3 conflicting date formats (%Y-%m-%d, %d-%b-%Y, %d/%m/%Y) using sequential fallback parsing.", body_text),
            Paragraph("n = 10,000 parsed (0 dropped)", body_text),
            Paragraph("Dates: 0 unparsed NaNs (ISO: 3,382; Day-Mon-Yr: 3,365; Day/Month/Yr: 3,253)", body_text)
        ],
        [
            Paragraph("<b>BMI Sentinels</b>", body_text),
            Paragraph("Replaced placeholder sentinel values (999.0 missing code and 0.0 entries) with <code>np.nan</code>.", body_text),
            Paragraph("n = 486 set to NaN (402 at 999; 84 at 0)", body_text),
            Paragraph("Mean BMI: <b>66.18 kg/m² -> 27.35 kg/m²</b> (valid n = 9,514)", body_text)
        ],
        [
            Paragraph("<b>Heart Rate Faults</b>", body_text),
            Paragraph("Filtered physiologically impossible telemetry faults outside human survival limits (&lt; 30 bpm or &gt; 250 bpm).", body_text),
            Paragraph("n = 37 rows removed (29 &gt; 250; 8 &lt; 30)", body_text),
            Paragraph("Mean HR: <b>78.83 bpm -> 78.05 bpm</b> (N retained = 9,963)", body_text)
        ],
        [
            Paragraph("<b>Derived Variable</b>", body_text),
            Paragraph("Excluded <code>map_mmhg</code> from correlation matrix (arithmetically computed: [systolic + 2*diastolic]/3).", body_text),
            Paragraph("1 column excluded", body_text),
            Paragraph("Trivial arithmetic correlation (r = 0.96 with systolic) excluded from discovery matrix.", body_text)
        ],
    ]
    t_clean = Table(cleaning_table, colWidths=[80, 220, 110, 154])
    t_clean.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DFE6EE")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4F7FA")),
        ("TOPPADDING", (0, 0), (-1, -1), 1.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(t_clean)
    story.append(Spacer(1, 3))

    # Ethics Clause Callout Box
    ethics_content = [
        [
            Paragraph(
                "<b>The Ethics Clause & Symmetry Test:</b><br/>"
                "Readings above 250 bpm were removed as device faults (n = 29, reaching 415 bpm) alongside 8 readings below 30 bpm / zeros (total device faults n = 37). "
                "Mean heart rate moves from 78.83 to 78.05 bpm (retaining N = 9,963). The figure was also produced without the exclusion; it is in the appendix.<br/>"
                "<b>Symmetry Test:</b> Would this removal be made if it weakened our hypothesis instead of strengthening it? <b>Yes, unconditionally.</b> "
                "Telemetry recordings exceeding 250 bpm or sitting at 0 bpm in hemodynamically stable ward patients reflect sensor dropouts and electronic noise, not human physiology. "
                "Retaining them would inject blatant device artifacts into clinical analytics; excluding them adheres to objective physiological impossibility rather than hypothesis-driven editing.",
                ethics_box
            )
        ]
    ]
    t_ethics = Table(ethics_content, colWidths=[564])
    t_ethics.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F9FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#0072B2")),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_ethics)

    doc.build(story)
    print(f"Successfully generated {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
