# Shut-the-Box Analysis with Quarto

This directory contains Quarto documents for analyzing Shut-the-Box simulation results.

## Setup Requirements

### 1. Project Dependencies
The analysis requires the stbsim package and its dependencies. From the project root:

```bash
cd ../shut_the_box_sim
# Activate the project virtual environment
source .venv/bin/activate
# Install dependencies if needed
pip install pandas matplotlib seaborn
```

### 2. Jupyter Dependencies for Quarto
Quarto needs Jupyter to execute Python code chunks:

```bash
# While in the activated environment
pip install jupyter nbformat ipython
```

### 3. Running Reports
To render the reports using the Rye environment:

```bash
cd analysis
QUARTO_PYTHON=../shut_the_box_sim/.venv/bin/python quarto render strategy_comparison_basic.qmd
QUARTO_PYTHON=../shut_the_box_sim/.venv/bin/python quarto render strategy_comparison.qmd
```

Or use the provided script:
```bash
./render_reports.sh
```

## Available Reports

### strategy_comparison_basic.qmd
A basic strategy comparison report that:
- Compares greedy_max vs min_tiles strategies
- Runs 100 games per strategy
- Provides summary statistics and detailed analysis
- Works with minimal dependencies (just pandas)

### strategy_comparison.qmd (Full Version)
Enhanced version with visualizations (requires matplotlib + seaborn):
- Interactive charts and plots
- Score distribution analysis
- Visual comparison of strategy performance

## MVP Implementation Status

✅ Basic project structure
✅ Quarto configuration  
✅ Strategy comparison logic
✅ Statistical analysis
✅ Visualization dependencies (matplotlib/seaborn added to project)
✅ Successful rendering (all dependencies working)
✅ Both basic and full reports rendering successfully

## Generated Reports

After running `./render_reports.sh`:
- `_output/strategy_comparison_basic.html` - Text-based analysis
- `_output/strategy_comparison.html` - Full analysis with visualizations

## Next Steps

1. ✅ ~~Add visualization dependencies~~ (Completed)
2. ✅ ~~Test report rendering~~ (Completed) 
3. Add parameterized reports (dynamic strategy/game selection)
4. Set up CI integration for automated reporting
5. Add more advanced analysis (turn-by-turn, head-to-head strategies)