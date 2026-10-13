#!/usr/bin/env bash
# =============================================================================
# Automated execution script for Week 3 Data Visualization assignment
# Runs all parts in order and reproduces all figures and PDFs from clean inputs.
# =============================================================================
set -e

PYTHON_CMD="python3"
if [ -d ".venv" ] && [ -f ".venv/bin/python" ]; then
    PYTHON_CMD=".venv/bin/python"
fi

echo "================================================================="
echo "  Week 3: Matplotlib & Seaborn — Complete Execution Pipeline"
echo "  Using Python interpreter: $($PYTHON_CMD --version)"
echo "================================================================="

echo ""
echo "[Step 1/7] Running vizlib self-check..."
$PYTHON_CMD vizlib.py

echo ""
echo "[Step 2/7] Generating Part A: Rebuilding 9 claims & 9 redesigns..."
$PYTHON_CMD partA_charts.py
$PYTHON_CMD generate_partA_pdf.py

echo ""
echo "[Step 3/7] Generating Part B: Computing Lie Factor audits..."
$PYTHON_CMD partB_lie_factor.py | tee partB_output.txt

echo ""
echo "[Step 4/7] Generating Part C: Palette CVD simulation & audit..."
$PYTHON_CMD partC_palette.py

echo ""
echo "[Step 5/7] Generating Part D: Cleaning data & building clinical review figure..."
$PYTHON_CMD partD_figure.py

echo ""
echo "[Step 6/7] Generating Part E: Compiling strictly 1-page justification PDF..."
$PYTHON_CMD generate_partE_pdf.py

echo ""
echo "[Step 7/7] Generating Bonus: Running preattentive visual search experiment..."
$PYTHON_CMD popout_experiment.py

echo ""
echo "================================================================="
echo "  SUCCESS: All figures, tables, scripts, and PDFs generated!"
echo "================================================================="
