# Project Roadmap: `stbsim` - MVP v0.1.0

This document outlines Sprint 3, the final sprint for achieving the Minimum Viable Product (MVP) v0.1.0 of `stbsim`. Sprints 0, 1, and 2 have been completed, establishing the project foundation, core game entities, strategies, and basic data collection mechanisms.

**Goal for MVP (v0.1.0) - Reminder:**
A command-line tool (`stbsim.cli`) that can:
1.  Run a specified number of 2-player Shut the Box games.
2.  Allow selection of strategies (Greedy-Max, Min-Tiles) for each player.
3.  Use a specified random seed for reproducibility.
4.  Output summary statistics (win rates, average scores, shut-box frequency).
5.  Optionally save detailed game event logs to a file (e.g., CSV or Parquet).
All built upon a well-tested, pure Python library (`stbsim`), and now also featuring a Quarto document for running and presenting simulations.

---

## Detailed MVP Workflow: `stbsim` Library, CLI & Quarto

**Overall Principles for MVP Sprints (Continued):**
* **Test-Driven:** Write tests *before* or *alongside* implementation.
* **Minimal Viable Functionality:** Only implement what's needed for the *current* sprint's goal.
* **CI Green:** Each sprint should end with all checks passing.
* **AI Leverage:** Use for boilerplate, test cases, config snippets, and explanations. Human reviews, integrates, and tests.

---

### 💻 Sprint 3: CLI, Quarto Document & MVP Release (~1.5 - 2 days)
*Goal: Create a user-friendly CLI, develop a basic Quarto document to run and present simulations, ensure end-to-end functionality, and package the MVP.*

| **Task ID** | **Action** | **Details & Tools** | **"Done" Criteria** | **AI Assist Request Example** |
| :---------- | :----------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S3.1        | **Design & Implement CLI (`typer`)** | In `stbsim/cli.py`, use `typer`. Args: `--n-games` (int), `--p1-strategy` (str, e.g., "greedy_max"), `--p2-strategy` (str), `--seed` (int, optional), `--output-file` (str, optional, for Parquet/CSV). Map strategy strings to functions from `stbsim.strategies`. Utilize `stbsim.Simulation` (S2.5) and `stbsim.stats` (S2.5). Add `typer`, `tqdm` to `pyproject.toml`. Ensure `pandas` (for CSV) or `pyarrow` (for Parquet) is available if chosen for output. | CLI module (`stbsim/cli.py`) created. `python -m stbsim.cli --help` (or `rye run stbsim --help`) works. Runs simulations with specified params. Progress bar shown. Summary stats printed. Optional output file created. `pre-commit` & `nox -s tests lint typecheck` pass. | "Generate `typer` CLI for `stbsim.cli`: args `n_games`, `p1_strategy`, `p2_strategy`, `seed`, `output_file`. Show strategy string mapping to `stbsim.strategies` functions and calling `stbsim.Simulation.run()`. How to use `tqdm`?" |
| S3.2        | **Create Initial Quarto Simulation Document** | Create `analysis/simulation_report.qmd` (or `index.qmd`). Use Python code cells to: 1. Import `stbsim` (e.g., `from stbsim.simulation import Simulation`). 2. Configure and run a simulation using `stbsim.Simulation.run()` or `stbsim.Game` directly. 3. Display input parameters and summary statistics (e.g., from `stbsim.stats`) as tables (Pandas DataFrame `to_markdown()` or Quarto's table rendering). 4. Optionally, a basic plot (e.g., bar chart of win rates) using `matplotlib` or `seaborn` (add to `pyproject.toml` if new). Configure `_quarto.yml` if needed (e.g., project title, Python settings if environment inference isn't straightforward). | A Quarto document (`.qmd`) exists. `quarto render <your_doc>.qmd` (from an activated Rye/Poetry env) succeeds. Rendered HTML shows simulation parameters, results table, and optional plot. `stbsim` library is correctly imported and used. `pre-commit` & `nox` pass. | "Show a `.qmd` (e.g., `analysis/simulation_report.qmd`) that: 1. Imports `stbsim.simulation.Simulation` and `stbsim.stats`. 2. Runs a 100-game sim with 'greedy_max' vs 'min_tiles', seed 42. 3. Displays params and summary stats from `stbsim.stats` as a table. 4. (Optional) Bar chart of win rates using `matplotlib`." |
| S3.3        | **End-to-End Test & Validation (CLI & Quarto)** | **CLI:** Run `stbsim.cli` with ~1k games, various strategies. Check console stats sanity. Verify output file (if used). Create a "golden run" test: fixed params (e.g., 100 games, seed, strategies), save summary stats. Future tests compare against this (e.g., `pytest` fixture). **Quarto:** Manually render `simulation_report.qmd`. Verify: simulation runs, results display correctly, consistent with CLI for similar params. | CLI produces sensible output. Golden run test for CLI stats passes (or fixture created). Quarto doc renders, displays correct and plausible results consistent with parameters. `pre-commit` & `nox` pass. | "Suggest a `pytest` approach for a 'golden run' test of CLI summary statistics (comparing current output to a stored fixture)." "Key items to manually verify in the rendered Quarto HTML for MVP?" |
| S3.4        | **Refine CI & Add Smoke Tests (CLI & Quarto)** | **CLI Smoke Test:** Add GHA step: `rye run python -m stbsim.cli --n-games 10 --seed 123 --p1-strategy greedy_max --p2-strategy min_tiles`. **Quarto Render Test:** Add GHA step: `rye run quarto render analysis/simulation_report.qmd` (or similar, depending on Rye setup for tools). Ensure `pytest --cov` coverage reporting (e.g., Codecov) is working. | CI workflow (GitHub Actions) includes passing CLI smoke test and Quarto rendering step. All CI jobs pass. Coverage reporting active. | "Update GHA workflow (from S0.5) to use Rye: 1. Step for CLI smoke test. 2. Step for `rye run quarto render analysis/simulation_report.qmd`. Ensure Python env is sourced." |
| S3.5        | **Documentation (Docstrings, README & Quarto Intro)** | Ensure public API in `stbsim` (esp. `core.py`, `strategies.py`, `cli.py`, `simulation.py`) has clear docstrings. Update `README.md`: Project description, features. Installation: `stbsim` library (editable via Rye/Poetry), Quarto CLI. CLI Usage: examples (`rye run stbsim ...`). Quarto Analysis: How to render `simulation_report.qmd`, brief on what it shows. Link to rendered Quarto (e.g., GitHub Pages, if set up later). Add basic comments/prose to `simulation_report.qmd` explaining its sections. | `README.md` is comprehensive for MVP. Public API has docstrings. Quarto doc is self-explanatory at a high level. | "Generate `README.md` template: Overview, Features (CLI, Quarto), Installation (Rye for Python lib, Quarto CLI), CLI Usage (`rye run stbsim ...`), Quarto Analysis (how to run/render `simulation_report.qmd`), Contributing." |
| S3.6        | **Tag MVP Release (v0.1.0)** | After all above and CI green on `develop`: 1. Merge `develop` to `main`. 2. Update `pyproject.toml` version to `0.1.0`. Commit. 3. `git tag v0.1.0`. 4. `git push origin v0.1.0 && git push origin main`. 5. (Optional) GitHub Release from tag. | `main` branch has MVP. `pyproject.toml` version is `0.1.0`. Tag `v0.1.0` pushed. GitHub Release drafted (optional). | N/A (Manual git/project admin) |

---

**Post-MVP Sprints (Brief Outline - Retaining User's Roadmap Items):**

*   **Sprint 4: Advanced Stats, Performance & Quarto Enhancements**
    *   Implement more aggregators (user's §2.3) into `stbsim.stats`.
    *   Profile/optimize `stbsim` (Phase 5). Add perf-budget test.
    *   Richer `Game.summarize()` for CLI/Quarto.
    *   More advanced Quarto docs: parameterization, deeper analysis, more plots.
*   **Sprint 5: FastAPI Service** (Phase 6)
*   **Sprint 6: SvelteKit UI Prototype** (Phase 8)
*   **Further Sprints:** Task Queue, DB Persistence, UI Polish, New Strategies, etc.

---

**How You and AI Collaborate in this Workflow (Sprint 3 Focus):**

1.  **You (Developer):**
    *   Focus on one Task ID. Understand goal and "Done" criteria.
    *   Prompt AI for `typer` CLI code, Quarto Python chunks, test ideas, `README.md` sections, GHA snippets.
    *   **Critically review AI output:** Correctness for `stbsim`, style, integration.
    *   **Integrate & Adapt:** Fit AI code into `stbsim`, add error handling, refine.
    *   **Test:** Ensure CLI, library, and Quarto rendering (with library calls) work.
    *   Commit to `develop`, push, ensure CI passes (including Quarto render).

2.  **AI (Your Assistant):**
    *   Provides boilerplate for `typer` CLI, Quarto Python cells, `pytest` cases.
    *   Generates config snippets (`pyproject.toml` additions, `_quarto.yml` ideas, GHA workflow updates).
    *   Suggests test cases for CLI args, Quarto output verification points.
    *   Helps draft `README.md` and docstrings.

*(Error Handling & Guardrails section remains largely the same as your previous draft, just ensure it's applied to Quarto-specific queries too.)*
