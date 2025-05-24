# shut-the-box-sim (stbsim)
A reproducible Shut the Box game simulator & strategy evaluator — with CLI, stats, golden-run tests, and Quarto reports.

## Features
- 🧮 Fast, deterministic simulations (CLI: Typer, Python)
- 🤖 Pluggable strategy support
- 📊 Summary stats: win rates, scores, shut-the-box
- 📄 Automated Quarto reports with charts
- 🚦 Golden-run CLI regression protection
- 🔁 Full CI/CD (lint, type, test, CLI & docs)

## Quickstart

### 1. **Clone & Install (with Rye)**
```sh
git clone <your-repo-url>
cd shut_the_box_sim
rye sync
```

### 2. **Run Simulations (CLI)**
```sh
rye run python -m stbsim.cli --n-games 100 --p1-strategy greedy_max --p2-strategy min_tiles --seed 42
```

### 3. **Build Reports (Quarto)**
```sh
cd analysis
QUARTO_PYTHON=../shut_the_box_sim/.venv/bin/python rye run quarto render strategy_comparison_basic.qmd
# Or: ./render_reports.sh
```
HTML output appears in `analysis/_output/`.

## Development Workflow

**Essential commands (run after any code changes):**
- **Auto-fix:** `rye run autofix` ← **Start here!**
- **Check:** `rye run lint`
- **Test:** `rye run test`
- **Typecheck:** `rye run typecheck`

📖 **See `CODE_STANDARDS.md` for complete formatting and linting standards.**
- Update CLI golden run:
    ```sh
    rye run python -m stbsim.cli --n-games 100 --p1-strategy greedy_max --p2-strategy min_tiles --seed 42 \
      | grep -A 10 '==== Summary Stats ====' > tests/fixtures/cli_golden_run_output.txt
    rye run pytest tests/test_cli_golden.py
    ```

## Contributing & License

Feedback and improvements welcome!
MIT License.
