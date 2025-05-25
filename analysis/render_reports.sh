#!/bin/bash
# Render Quarto reports using the uv Python environment

set -e

PYTHON_ENV="../shut_the_box_sim/.venv/bin/python"

echo "🔄 Rendering Shut-the-Box Analysis Reports..."
echo "Using Python: $PYTHON_ENV"
echo ""

echo "📊 Rendering basic strategy comparison report..."
QUARTO_PYTHON="$PYTHON_ENV" quarto render strategy_comparison_basic.qmd
echo "✅ Basic report completed: _output/strategy_comparison_basic.html"
echo ""

echo "📈 Rendering full strategy comparison report with visualizations..."
QUARTO_PYTHON="$PYTHON_ENV" quarto render strategy_comparison.qmd  
echo "✅ Full report completed: _output/strategy_comparison.html"
echo ""

echo "🎉 All reports rendered successfully!"
echo "📁 Output files are in the _output/ directory"