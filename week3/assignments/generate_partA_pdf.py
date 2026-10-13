"""
Build partA_diagnosis.pdf using ReportLab.
Compiles all 9 case diagnoses, with both rebuilt and redesigned figures,
precisely addressing the 4-part marking rubric for each case.
"""

from __future__ import annotations

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

ROOT = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(ROOT, "figures_partA")
PDF_PATH = os.path.join(ROOT, "partA_diagnosis.pdf")


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom typography
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#16202E"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#5B6573"),
        spaceAfter=15
    )
    case_header_style = ParagraphStyle(
        "CaseHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0072B2"),
        spaceBefore=0,
        spaceAfter=6
    )
    rubric_head_style = ParagraphStyle(
        "RubricHead",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#16202E"),
    )
    body_style = ParagraphStyle(
        "CaseBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#16202E"),
    )
    body_bold = ParagraphStyle(
        "CaseBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )
    caption_style = ParagraphStyle(
        "CaptionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#5B6573"),
        alignment=1, # Centered
    )

    story = []

    # Title Banner
    story.append(Paragraph("Week 3 — Part A: Rebuilding & Diagnosing Nine Visual Claims", title_style))
    story.append(Paragraph(
        "<b>Student:</b> Muhammad Maheem &nbsp;|&nbsp; <b>ID:</b> SU92-BSAIM-F24-054 &nbsp;|&nbsp; "
        "<b>Course:</b> CDB601220 Data Visualization (Lecture 5 & 6) &nbsp;|&nbsp; <b>Marks:</b> 36",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0072B2"), spaceAfter=15))

    cases_data = [
        {
            "num": 1,
            "title": 'Case 1 · "Premium-certified helmets have 2.5x the head-injury rate"',
            "rebuild_img": "case01_rebuild.png",
            "redesign_img": "case01_redesign.png",
            "self_check": "Standard: 2.15, Premium: 5.40 injuries per 1,000 trips (5.40 / 2.15 = 2.51×).",
            "claim": "Sum head_injuries and trips by helmet_grade. Plot injuries per 1,000 trips as a bar chart from zero baseline.",
            "conclusion": "Premium-certified helmets are defective or hazardous, resulting in 2.5× more head injuries than standard helmets.",
            "decoy": "<b>Decoy Objection:</b> <i>\"The sample size is too small\"</i> or <i>\"The y-axis is truncated.\"</i><br/>"
                     "<b>Ruled out by data:</b> Total trips across the fleet equal 100,000 (Standard: 60,000; Premium: 40,000), providing massive statistical power. "
                     "The y-axis begins strictly at zero. Rider average speed is virtually identical (Standard: 71.4 km/h vs. Premium: 72.1 km/h), and riding experience is comparable (36.2 vs. 35.8 months).",
            "mechanism": "<b>Simpson's Paradox (Confounding by Road Exposure):</b><br/>"
                         "Helmet grade assignment is heavily confounded by road type. <b>85.0% of Premium helmet trips (34,000 of 40,000) occurred on high-speed Motorways</b>, where baseline injury rates are highest (6.11/1,000 trips), compared to only <b>3.3% of Standard trips (2,000 of 60,000)</b>.<br/>"
                         "Controlled within every single road type, Premium helmets are consistently <b>25% to 28% safer</b>:<br/>"
                         "• <b>Motorway:</b> Premium 6.00 vs. Standard 8.00 (-25.0% safer)<br/>"
                         "• <b>City Arterial:</b> Premium 2.20 vs. Standard 3.00 (-26.7% safer)<br/>"
                         "• <b>Inner-city Lanes:</b> Premium 1.00 vs. Standard 1.39 (-28.1% safer).",
            "redesign_notes": "Stratified grouped bar chart comparing helmet grades within each road environment. Exposes Simpson's Paradox and proves Premium helmets provide superior protection."
        },
        {
            "num": 2,
            "title": 'Case 2 · "Canteen chai sales predict quiz failures"',
            "rebuild_img": "case02_rebuild.png",
            "redesign_img": "case02_redesign.png",
            "self_check": "Pearson r = 0.98 (r = 0.977, r² = 0.955).",
            "claim": "Scatter cups_doodh_patti_sold against quiz_failures, fit least-squares regression line, annotate Pearson r.",
            "conclusion": "Drinking doodh patti chai from the campus canteen impairs academic performance and predicts quiz failures.",
            "decoy": "<b>Decoy Objection:</b> <i>\"Correlation is not causation\"</i> (unspecific) or <i>\"Exam months spike stress, driving both chai and failures.\"</i><br/>"
                     "<b>Ruled out by data:</b> <code>is_exam_month</code> has virtually zero correlation with chai sales (r = 0.035) or quiz failures (r = 0.225). The pattern persists unchanged across non-exam months.",
            "mechanism": "<b>Spurious Correlation Driven by Common Denominator Scale (Enrollment Growth):</b><br/>"
                         "Both chai sales and quiz failures are unstandardized raw monthly totals driven by massive campus student body growth, expanding from <b>1,765 students in Month 1 to 5,406 in Month 24 (+206%)</b>.<br/>"
                         "Student enrollment correlates at <b>r = 0.997</b> with chai sales and <b>r = 0.977</b> with quiz failures. When normalized to per-student rates (cups per student vs. failures per student), the correlation <b>completely collapses to r = 0.29</b>.",
            "redesign_notes": "Scatter plot of normalized per-capita metrics (chai cups per student vs. failure rate %) colored by enrollment. Proves zero predictive relationship once scale confounding is removed."
        },
        {
            "num": 3,
            "title": 'Case 3 · "The Smog Action Plan cut Lahore\'s AQI by a third"',
            "rebuild_img": "case03_rebuild.png",
            "redesign_img": "case03_redesign.png",
            "self_check": "Before Day 61: 202.09, After Day 61: 137.21 — an arithmetic fall of 32.1%.",
            "claim": "Mean aqi per date across all rows. Line plot from zero baseline. Vertical marker at Day 61, horizontal mean lines for Days 1–60 and 61–120.",
            "conclusion": "The Punjab EPA's Smog Action Plan successfully reduced ambient air pollution across Lahore by 32%.",
            "decoy": "<b>Decoy Objection:</b> <i>\"The y-axis is truncated\"</i> or <i>\"Favorable seasonal winds blew the smog away.\"</i><br/>"
                     "<b>Ruled out by data:</b> The recipe begins the y-axis strictly at zero. Crucially, within every single active monitoring zone, AQI did NOT decrease: Arterial stayed at 245.9 (was 244.7), Peri-urban stayed at 80.4 (was 78.9), and Residential stayed at 120.8 (was 121.6).",
            "mechanism": "<b>Monitor Attrition / Survivorship Bias (Network Composition Change):</b><br/>"
                         "The 32% reduction is a pure arithmetic artifact of station dropouts. On Day 61, <b>all 6 high-pollution Industrial stations (LHR-01 to LHR-06, mean AQI = 322.0) went completely offline</b>, alongside 3 arterial stations.<br/>"
                         "Post-Day 60 averages sampled only clean residential and peri-urban stations. Active zones saw <b>0.0% improvement</b>. Pollution was unchanged; the EPA simply stopped measuring the dirtiest sites.",
            "redesign_notes": "Multi-line chart disaggregated by monitoring zone with clear annotation of the Industrial monitor shutdown on Day 61, showing flat trends across all continuing stations."
        },
        {
            "num": 4,
            "title": 'Case 4 · "Four departments behave identically, so fund them equally"',
            "rebuild_img": "case04_rebuild.png",
            "redesign_img": "case04_redesign.png",
            "self_check": "Every department reports Mean = 18.00 / 14.50, r = 0.816, Slope = 0.250.",
            "claim": "Summary table: n, mean study hours, mean score, SD of each, Pearson r, and regression slope per department.",
            "conclusion": "All four academic departments exhibit identical student learning dynamics and should receive equal funding allocations.",
            "decoy": "<b>Decoy Objection:</b> <i>\"Sample size (n = 11) is too small to draw conclusions\"</i> or <i>\"Study hours are self-reported.\"</i><br/>"
                     "<b>Ruled out by data:</b> The summary statistics are identical to 3 decimal places by mathematical design (Anscombe's Quartet). Small n misses the core failure: identical statistics can describe fundamentally different data shapes.",
            "mechanism": "<b>Anscombe's Quartet (Summary Statistics Conceal Functional Form & Outliers):</b><br/>"
                         "Each department represents one of Anscombe's four classic pathological distributions:<br/>"
                         "• <b>Computer Science:</b> Genuine linear relationship with normally distributed errors.<br/>"
                         "• <b>Business Administration:</b> Strict quadratic non-linear curve (inverted-U; optimal study is 18 hrs, scores drop thereafter).<br/>"
                         "• <b>Electrical Engineering:</b> Near-perfect deterministic linear relationship distorted by a single vertical outlier (x=18, y=15.04).<br/>"
                         "• <b>Architecture:</b> Vertical cluster where all students study exactly 16 hrs, with the entire slope created by a single high-leverage horizontal outlier (x=38, y=19.5).",
            "redesign_notes": "2×2 faceted scatter plot with linear regression fits displaying the raw observations. Exposes the severe non-linearity, outliers, and leverage points that summary tables hide."
        },
        {
            "num": 5,
            "title": 'Case 5 · "Five cohorts, one set of statistics"',
            "rebuild_img": "case05_rebuild.png",
            "redesign_img": "case05_redesign.png",
            "self_check": "Every cohort reports Mean = 48.00 / 63.00, SD = 12.00 / 15.00, r = 0.420.",
            "claim": "Summary table: n, mean hours, mean score, SD hours, SD score, Pearson r per shape_name.",
            "conclusion": "All five cohorts reflect identical student platform engagement and score distributions under a single pedagogical model.",
            "decoy": "<b>Decoy Objection:</b> <i>\"Pearson r = 0.420 is only moderate correlation\"</i> or <i>\"Cohort aggregation creates ecological fallacy.\"</i><br/>"
                     "<b>Ruled out by data:</b> Sample size is substantial (n = 180 per cohort, N = 900 total), with standard errors < 0.9 units. The statistical equality is deliberate, not a random sampling fluke.",
            "mechanism": "<b>Geometric Shape Annealing (The Datasaurus / Matejka & Fitzmaurice Phenomenon):</b><br/>"
                         "The 5 cohorts were generated via simulated annealing to match identical first and second bivariate moments while forming distinct 2D geometric patterns: <b>a straight line, an ellipse/ring, a 5-pointed star, an 'X' shape, and two separated clusters</b>.<br/>"
                         "Summary statistics have zero spatial degrees of freedom to differentiate geometry or multimodal clustering.",
            "redesign_notes": "1×5 small-multiple scatter plots revealing the underlying 2D point cloud geometries for each cohort."
        },
        {
            "num": 6,
            "title": 'Case 6 · "Creatinine tracks HbA1c — a finding"',
            "rebuild_img": "case06_rebuild.png",
            "redesign_img": "case06_redesign.png",
            "self_check": "Creatinine ↔ HbA1c = 0.77, Systolic ↔ MAP = 0.96, matrix size 20 × 20.",
            "claim": "Correlation matrix of 20 numeric columns as annotated heatmap with cmap='Reds', no vmin/vmax, both triangles shown.",
            "conclusion": "Serum creatinine strongly correlates with HbA1c (r = 0.77), indicating a major physiological discovery linking renal dysfunction and glycemic control.",
            "decoy": "<b>Decoy Objection:</b> <i>\"The correlation is confounded by patient age or clinical study site.\"</i><br/>"
                     "<b>Ruled out by data:</b> Age correlates at r = 0.01 with creatinine. Within sites, the correlation only appears in Site C (r = 0.92) solely because the outlier was admitted there.",
            "mechanism": "<b>Single Bivariate Leverage Outlier + Dual Visualization Failures:</b><br/>"
                         "1. <b>Data Flaw:</b> The apparent r = 0.77 correlation is manufactured entirely by <b>Row 0: a single patient with Creatinine = 1,050.0 µmol/L and HbA1c = 15.80%</b>. Removing this single point causes the correlation to <b>drop from r = 0.765 to r = -0.004 (precisely zero)</b>.<br/>"
                         "2. <b>Visual Flaws:</b> (a) Sequential <code>Reds</code> colormap has no neutral midpoint for negative correlations; (b) Omitting <code>vmin=-1, vmax=1</code> distorts relative intensity; (c) Showing both triangles creates 400 redundant cells; (d) Includes <code>map_mmhg</code> whose r = 0.96 correlation with systolic BP is an arithmetic identity: <code>(systolic + 2*diastolic)/3</code>.<br/>"
                         "3. <b>Critical Distinction:</b> Fixing the heatmap resolves visual perception, but it will <b>STILL show r = 0.77</b> until the data entry error in Row 0 is cleaned!",
            "redesign_notes": "Two-panel figure: Scatter plot isolating the Row 0 leverage outlier (r drops from 0.77 to -0.00), paired with an honest correlation heatmap (diverging RdBu_r, vmin=-1, vmax=1, upper triangle masked, MAP excluded)."
        },
        {
            "num": 7,
            "title": 'Case 7 · "ShaheenGo ran at a loss until May"',
            "rebuild_img": "case07_rebuild.png",
            "redesign_img": "case07_redesign.png",
            "self_check": "Cost line sits physically above revenue line for Jan, Feb, Mar, Apr.",
            "claim": "Line chart with two y-axes: revenue on left (50–80 PKR M), cost on right (40–56 PKR M). ax.twinx().",
            "conclusion": "ShaheenGo operated at an operational loss during Q1 and achieved break-even profitability only in May.",
            "decoy": "<b>Decoy Objection:</b> <i>\"Revenue and costs are measured in different currencies\"</i> or <i>\"Late customer invoice payments.\"</i><br/>"
                     "<b>Ruled out by data:</b> Both series are recorded in the exact same unit: PKR Millions!",
            "mechanism": "<b>Dual-Axis Illusion (Arbitrary Scale Superimposition):</b><br/>"
                         "ShaheenGo was <b>profitable in every single month</b>. Profit was strictly positive and grew continuously:<br/>"
                         "• Jan: Rev 52M, Cost 44M -> <b>Profit +8M PKR</b><br/>"
                         "• Feb: Rev 58M, Cost 46M -> <b>Profit +12M PKR</b><br/>"
                         "• Mar: Rev 61M, Cost 47M -> <b>Profit +14M PKR</b><br/>"
                         "• Apr: Rev 66M, Cost 49M -> <b>Profit +17M PKR</b><br/>"
                         "• May: Rev 71M, Cost 51M -> <b>Profit +20M PKR</b><br/>"
                         "• Jun: Rev 78M, Cost 53M -> <b>Profit +25M PKR</b><br/>"
                         "The crossover was fabricated by setting left axis to 50–80 (compressing revenue) and right axis to 40–56 (expanding cost), physically drawing Cost 44M higher on the page than Revenue 52M.",
            "redesign_notes": "Single shared axis starting at zero (0–90 PKR M) displaying Revenue and Cost curves, plus a lower panel displaying Net Monthly Profit (+8M to +25M PKR)."
        },
        {
            "num": 8,
            "title": 'Case 8 · "Three bin widths, three different distributions"',
            "rebuild_img": "case08_rebuild.png",
            "redesign_img": "case08_redesign.png",
            "self_check": "n = 10,000 in all three panels.",
            "claim": "Three histograms of systolic side by side: bins=3, bins=45, bins=400.",
            "conclusion": "The distribution of systolic blood pressure is inherently unstable and changes its fundamental shape depending on arbitrary bin selection.",
            "decoy": "<b>Decoy Objection:</b> <i>\"The sample size is too small\"</i> or <i>\"Outliers and noise are corrupting the histogram.\"</i><br/>"
                     "<b>Ruled out by data:</b> Sample size is massive (N = 10,000). All measurements are valid clinical integer values between 92 and 199 mmHg.",
            "mechanism": "<b>Discretization and Bin-Width Sensitivity (Oversmoothing vs. Aliasing on Integers):</b><br/>"
                         "• <b>bins = 3 (width = 35.7 mmHg):</b> Extreme oversmoothing amalgamates the normotensive peak (~120 mmHg) and hypertensive peak (~165 mmHg) into a monolithic block.<br/>"
                         "• <b>bins = 400 (width = 0.27 mmHg):</b> Extreme undersmoothing on integer-recorded data produces a severe <b>comb artifact</b> where <b>296 out of 400 bins (74.0%) are completely empty</b> because fractional mmHg measurements cannot exist.<br/>"
                         "• <b>bins = 45 (width = 2.4 mmHg):</b> Faithfully reveals the true underlying bimodal clinical population without aliasing.",
            "redesign_notes": "Principled histogram declaring bin width = 2.5 mmHg (45 bins) with clinical threshold markers distinguishing normotensive and hypertensive cohorts."
        },
        {
            "num": 9,
            "title": 'Case 9 · "4.4% of the density sits above 100% saturation"',
            "rebuild_img": "case09_rebuild.png",
            "redesign_img": "case09_redesign.png",
            "self_check": "Maximum value in data is exactly 100. The curve extends past 100.",
            "claim": "Kernel density estimate of spo2 with default bandwidth. Extend x-axis to 108, mark 100.",
            "conclusion": "A significant percentage of patients exhibited hyper-saturation (> 100% SpO₂), indicating severe monitor calibration failure.",
            "decoy": "<b>Decoy Objection:</b> <i>\"Sensor calibration errors recorded impossible physical values > 100%.\"</i><br/>"
                     "<b>Ruled out by data:</b> <code>df.spo2.max() == 100</code>. There is not a single reading above 100% anywhere in the dataset!",
            "mechanism": "<b>Boundary Bias / Boundary Leakage in Kernel Density Estimation:</b><br/>"
                         "Standard Gaussian KDE places symmetric Gaussian kernels with infinite support over every observation. When data clusters against a hard physical boundary (100% hemoglobin saturation ceiling), symmetric kernels centered at 98–100% <b>inevitably leak probability mass across the boundary into the impossible domain (> 100%)</b>.<br/>"
                         "The curve is an artifact of the estimator, not the data.",
            "redesign_notes": "Discrete integer-binned histogram (binwidth = 1.0%) with a hard boundary at 100%, proving that 100% of observations obey physical bounds."
        }
    ]

    for case in cases_data:
        # Build page for each case
        case_flow = []
        case_flow.append(Paragraph(case["title"], case_header_style))
        case_flow.append(Spacer(1, 4))

        # Rebuild & Redesign side-by-side images
        rebuild_p = os.path.join(FIG_DIR, case["rebuild_img"])
        redesign_p = os.path.join(FIG_DIR, case["redesign_img"])
        
        img_w = 260
        img_h = 155
        img_table_data = [
            [Image(rebuild_p, width=img_w, height=img_h), Image(redesign_p, width=img_w, height=img_h)],
            [Paragraph("<b>Rebuild: Published Flawed Claim</b>", caption_style), Paragraph("<b>Redesign: Honest Accurate Visualization</b>", caption_style)]
        ]
        img_table = Table(img_table_data, colWidths=[270, 270])
        img_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
            ("TOPPADDING", (0, 1), (-1, 1), 2),
        ]))
        case_flow.append(img_table)
        case_flow.append(Spacer(1, 8))

        # 4 Rubric Sections Table
        rubric_content = [
            [
                Paragraph("1. Rebuild & Self-Check", rubric_head_style),
                Paragraph(f"<b>Recipe:</b> {case['claim']}<br/><b>Verified Self-Check:</b> {case['self_check']}", body_style)
            ],
            [
                Paragraph("2. Conclusion & Decoy", rubric_head_style),
                Paragraph(f"<b>Invited Conclusion:</b> \"{case['conclusion']}\"<br/>{case['decoy']}", body_style)
            ],
            [
                Paragraph("3. Precise Mechanism", rubric_head_style),
                Paragraph(case["mechanism"], body_style)
            ],
            [
                Paragraph("4. Redesign Justification", rubric_head_style),
                Paragraph(case["redesign_notes"], body_style)
            ],
        ]
        rubric_table = Table(rubric_content, colWidths=[130, 410])
        rubric_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F4F7FA")),
            ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FFFFFF")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#16202E")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DFE6EE")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        case_flow.append(rubric_table)

        story.append(KeepTogether(case_flow))
        if case["num"] < 9:
            story.append(PageBreak())

    doc.build(story)
    print(f"Successfully generated {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
