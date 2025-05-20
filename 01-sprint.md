Okay, this is an excellent and well-structured roadmap! Let's break this down into a highly focused, sprint-based workflow aiming for that initial MVP: **a robust, test-covered simulation library (`stbsim`) and a functional CLI.**

We'll prioritize getting the core simulation engine working and verifiable before even thinking about web layers. The user's "First-pass build-out workflow" is a great skeleton. We'll flesh that out with more granularity, especially for the initial MVP sprints.

**Goal for MVP (v0.1.0):**
A command-line tool (`stbsim.cli`) that can:
1.  Run a specified number of 2-player Shut the Box games.
2.  Allow selection of strategies (Greedy-Max, Min-Tiles) for each player.
3.  Use a specified random seed for reproducibility.
4.  Output summary statistics (win rates, average scores, shut-box frequency).
5.  Optionally save detailed game event logs to a file (e.g., CSV or Parquet).
All built upon a well-tested, pure Python library.

---

## Detailed MVP Workflow: `stbsim` Library & CLI

**Overall Principles for MVP Sprints:**
*   **Strictly Sequential for Core:** Build foundational pieces first.
*   **Test-Driven:** Write tests *before* or *alongside* implementation. Doctests for simple cases, `pytest` for complex logic and parametrization.
*   **Minimal Viable Functionality:** Only implement what's needed for the *current* sprint's goal. Defer optimizations and advanced features.
*   **CI Green:** Each sprint (or even sub-task) should ideally end with all checks passing.
*   **AI Leverage:** Ask for code snippets, test cases, boilerplate, CI config snippets, and explanations. You (the human) review, integrate, and test.

---

### 🏁 Sprint 0: Project Setup & Foundation (~0.5 - 1 day)
*Goal: A functional Python project with basic dev tooling and CI.*

| **Task ID** | **Action**                                       | **Details & Tools**                                                                                                   | **"Done" Criteria**                                                                                                                               | **AI Assist Request Example**                                                                                                 |
| :---------- | :----------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------- |
| S0.1        | **Initialize Git Repository**                    | Create `shut_the_box_sim` on GitHub. MIT License. `main` branch, `develop` branch (protected). `.gitignore` for Python. | Repo exists on GitHub. `develop` branch created from `main`. `.gitignore` committed.                                                          | "Generate a standard Python `.gitignore` file."                                                                               |
| S0.2        | **Bootstrap Python Project**                     | Use `rye init shut_the_box_sim` (or `poetry new shut_the_box_sim`). Configure `pyproject.toml`: name, version, authors, Python version (e.g., `^3.11`). Add `stbsim` as a package. | `pyproject.toml` configured. `stbsim/__init__.py` exists. `rye sync` (or `poetry install`) works.                                      | "Show me a minimal `pyproject.toml` using Rye for a package named `stbsim` supporting Python 3.11+, with `pytest` as a dev dep." |
| S0.3        | **Setup Linting & Formatting**                 | `rye add --dev ruff black mypy pytest pytest-cov`. Configure `pre-commit` with hooks for `ruff`, `black`, `mypy`.           | `pre-commit install` done. `pre-commit run --all-files` passes. `ruff.toml` or `pyproject.toml [tool.ruff]` configured. `mypy.ini` basic setup. | "Generate a `pre-commit-config.yaml` with `ruff`, `black`, and `mypy`." "Suggest a basic `mypy.ini` configuration."         |
| S0.4        | **Setup Task Runner (`nox`)**                    | Create `noxfile.py`. Define sessions for: `lint` (ruff, black check), `typecheck` (mypy), `tests` (pytest --cov).       | `nox -s lint typecheck tests` all pass (tests will fail initially as there are no tests/code).                                               | "Generate a basic `noxfile.py` with sessions for `lint` (ruff, black), `typecheck` (mypy), and `tests` (pytest)."                 |
| S0.5        | **Basic CI Pipeline (GitHub Actions)**           | Workflow file: triggers on push/PR to `develop`/`main`. Matrix for Python 3.11, 3.12. Steps: checkout, setup Python (Rye), run `nox -s lint typecheck tests`. | CI workflow YAML committed. A push to `develop` triggers the workflow, and it passes (once initial dummy tests are added or it handles no tests). | "Generate a GitHub Actions workflow YAML for a Rye-based Python project, running `nox` sessions on Python 3.11 and 3.12."        |

---

### 🧱 Sprint 1: Core Game Entities & Logic (~1.5 - 2 days)
*Goal: Implement and thoroughly test the fundamental game objects: `TileRack`, `Dice`, `Move`, `Player` (structure), `Turn`, `Game` (core mechanics).*

| **Task ID** | **Action**                                  | **Details & Tools**                                                                                                                                                                                                                                                                                          | **"Done" Criteria**                                                                                                                                                                                            | **AI Assist Request Example**                                                                                                                               |
| :---------- | :------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S1.1        | **Implement `TileRack`**                    | `stbsim/core.py`. `tiles_up: set[int]`. Methods: `flip_tiles(combo: tuple[int,...])`, `is_ комбина_valid(combo, roll_total)`, `score()`, `is_shut()`.  Docstrings & doctests. Unit tests (`tests/test_core.py`) using `pytest.mark.parametrize`. `to_dict()` method. | All methods implemented & tested. 100% test coverage for `TileRack`. `to_dict()` serializes state. `pre-commit` & `nox` pass.                                                                            | "Generate Python code for the `TileRack` class as described in the roadmap, including a `to_dict` method. Provide doctest examples for its methods."            |
| S1.2        | **Implement `Dice`**                        | `stbsim/core.py`. `n_dice: int`, `rng: random.Random`. Method: `roll() -> tuple[int, ...]`. Inject `rng` via constructor. Docstrings & doctests. Unit tests. `to_dict()` (e.g., for `n_dice`).                                                                      | Implemented & tested. `rng` can be seeded for deterministic rolls in tests. `to_dict()` works. `pre-commit` & `nox` pass.                                                                                      | "Generate Python code for the `Dice` class, ensuring the random number generator is injectable. Include `to_dict`."                                            |
| S1.3        | **Implement `Move`**                        | `stbsim/core.py`. Dataclass/attrs for `roll: tuple[int,...]`, `combo: tuple[int,...]`, `valid: bool`, `timestamp: datetime`. `to_dict()` method. Basic unit tests for instantiation and `to_dict`.                                                                                 | Implemented & tested. `to_dict()` works. `pre-commit` & `nox` pass.                                                                                                                                          | "Generate a Python dataclass for `Move` with the specified fields and a `to_dict` method."                                                                    |
| S1.4        | **Implement `Player` (Structure & Strategy Stub)** | `stbsim/core.py` (Player), `stbsim/strategies.py` (strategy function). `Player`: `name: str`, `strategy_fn`. `choose_combo(roll_total: int, tiles_up: set[int]) -> tuple[int, ...] | Player class defined. `strategy_fn` placeholder exists. Basic unit tests for Player instantiation. `to_dict()` for Player. `pre-commit` & `nox` pass.                                                  | "Define the `Player` class structure. Define the function signature for `choose_combo` in `strategies.py`."                                                  |
| S1.5        | **Implement `Turn`**                        | `stbsim/core.py`. `player_id: str`, `moves: list[Move]`, `end_state` (e.g., score, shut_box_bool). Method: `play_turn(player_strategy_fn, tile_rack, dice)`. Handles game loop within a turn until no valid move. Unit tests for turn logic. `to_dict()` method. | Implemented & tested. Turn proceeds until bust or shut box. `to_dict()` works. `pre-commit` & `nox` pass.                                                                                                      | "Outline the logic for the `Turn.play_turn()` method. How should it interact with `Dice`, `TileRack`, and player strategy? Generate `Turn.to_dict()`."        |
| S1.6        | **Implement `Game` (Core Mechanics)**       | `stbsim/core.py`. `players: list[Player]`, `tile_racks: dict[str, TileRack]`, `turn_log: list[Turn]`, `rng_seed: int`. Methods: `play_game()`, `is_over()`, `get_winner()`, `summarize()` (basic version for now). Inject `random.Random` instance based on `rng_seed`. `to_dict()`. | Game can be initialized. `play_game()` orchestrates turns. `is_over()` detects end. Basic summary. `to_dict()` works. Unit tests for game flow. `pre-commit` & `nox` pass. Coverage target (e.g., 90%) met for `core.py`. | "Outline `Game.play_game()` method. How does it manage turns between players and check for game over? Generate `Game.to_dict()`."                           |

---

### 🧠 Sprint 2: Strategies & Basic Data Collection (~1 - 1.5 days)
*Goal: Implement the two baseline AI strategies and a simple in-memory data logger that outputs to a Pandas DataFrame.*

| **Task ID** | **Action**                                   | **Details & Tools**                                                                                                                                                                                                                           | **"Done" Criteria**                                                                                                                                                                                                                         | **AI Assist Request Example**                                                                                                                                  |
| :---------- | :------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S2.1        | **Implement `Greedy-Max` Strategy**          | `stbsim/strategies.py`. `def greedy_max_strategy(roll_total: int, tiles_up: set[int]) -> tuple[int, ...]`. Test with various `roll_total` and `tiles_up` states, including edge cases (no valid move). Use `pytest.mark.parametrize`.           | Strategy function implemented and thoroughly tested. Handles cases where no single largest tile fits, then tries highest multi-tile. Returns empty tuple if no move. `pre-commit` & `nox` pass.                                                     | "Generate the `greedy_max_strategy` function. Provide pytest `parametrize` examples for testing it, including edge cases."                                       |
| S2.2        | **Implement `Min-Tiles` Strategy**           | `stbsim/strategies.py`. `def min_tiles_strategy(roll_total: int, tiles_up: set[int]) -> tuple[int, ...]`. Test thoroughly, similar to Greedy-Max.                                                                                               | Strategy function implemented and thoroughly tested. Returns empty tuple if no move. `pre-commit` & `nox` pass.                                                                                                                          | "Generate the `min_tiles_strategy` function. Provide pytest `parametrize` examples for testing it."                                                            |
| S2.3        | **Define Event Schema & Logger**             | `stbsim/loggers.py`. Define the flat event schema as a TypedDict or Pydantic model for clarity. Create `InMemoryEventLogger` class: `log_event(...)` appends dict to `self.events: list[dict]`. Method `get_events_dataframe() -> pd.DataFrame`. | Event schema documented. Logger class can store events and convert to DataFrame. Add `pandas` to `pyproject.toml`. Unit tests for logger. `pre-commit` & `nox` pass.                                                                           | "Define a Python TypedDict or Pydantic model for the event schema. Create an `InMemoryEventLogger` class that collects these events and can convert them to a Pandas DataFrame." |
| S2.4        | **Integrate Logging into `Game`/`Turn`**     | Pass logger instance to `Game`, then to `Turn`. `Turn` logs each `Move` (or attempted move). `Game` logs turn summaries or game-level events. Ensure `sim_id`, `game_id`, etc., are populated.                                                      | Events are logged for each move within a game. DataFrame can be generated at end of game containing all moves with correct fields. `pre-commit` & `nox` pass.                                                                             | "Show how to modify the `Turn.play_turn()` and `Game.play_game()` methods to accept and use the `InMemoryEventLogger`."                                          |
| S2.5        | **Implement Basic `Simulation` & Aggregators** | `stbsim/core.py` (or `stbsim/simulation.py`). `Simulation` class: `run(n_games, p1_strat, p2_strat, seed_start)`. Iterates `Game` N times. `stbsim/stats.py`: Basic aggregators for DataFrame: `calculate_win_rates(df)`, `average_scores(df)`. | `Simulation` can run multiple games. Basic stats functions can process the DataFrame from logged events to produce win rates, avg scores. Unit tests for aggregators. `pre-commit` & `nox` pass.                                           | "Design a simple `Simulation` class to run N games. Write a `stats.py` function to calculate player win rates from a game events DataFrame."                     |

---

### 💻 Sprint 3: CLI & MVP Release (~1 day)
*Goal: Create a user-friendly CLI, ensure end-to-end functionality, and package the MVP.*

| **Task ID** | **Action**                                       | **Details & Tools**                                                                                                                                                                                                                                                                                                                            | **"Done" Criteria**                                                                                                                                                                                                                                  | **AI Assist Request Example**                                                                                                                                                                                          |
| :---------- | :----------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| S3.1        | **Design & Implement CLI (`typer`)**             | `stbsim/cli.py`. Use `typer`. Args: `--n-games`, `--p1-strategy`, `--p2-strategy`, `--seed`, `--output-file` (optional, for Parquet/CSV). Implement strategy selection mapping string names to functions. Add `typer` and `tqdm` (for progress bar), `pyarrow` (for Parquet) to `pyproject.toml`.                                     | CLI module created. `python -m stbsim.cli --help` works. CLI runs a simulation with specified params. Progress bar shown. Summary stats printed. If `--output-file` given, Parquet/CSV file is created. `pre-commit` & `nox` pass.                      | "Generate a `typer` CLI structure for `stbsim.cli` with the specified arguments. Show how to map strategy strings to the actual strategy functions."                                                                     |
| S3.2        | **End-to-End Test & Validation**                 | Run CLI with 1k-10k games. Check output stats for sanity (e.g., scores are reasonable, win rates add up). Verify output file format and content. Create a "golden run" test: run 100 games with fixed seed, strategies, save output stats. Future test runs compare against these golden stats (within a tolerance).                            | CLI produces expected output. Golden run output matches fixture. `pre-commit` & `nox` pass.                                                                                                                                                          | "Suggest a way to implement a 'golden run' test for the CLI output (summary stats)."                                                                                                                                 |
| S3.3        | **Refine CI & Add Smoke Test**                   | Add a CI job step that runs the CLI with a small number of games (e.g., 100) to act as a smoke test. Ensure coverage is reported (e.g., Codecov/Coveralls badge).                                                                                                                                                                               | CI includes a CLI smoke test. Coverage badge is configured if desired. All CI jobs pass.                                                                                                                                                           | "Add a step to the GitHub Actions workflow to run `python -m stbsim.cli --n-games 10 --seed 42 --p1 greedy_max --p2 min_tiles`."                                                                                     |
| S3.4        | **Documentation (Docstrings & README)**          | Ensure all public functions/classes have clear docstrings. Update `README.md` with project description, installation (editable install via `pipx install -e .` or `rye run python -m stbsim.cli`), and basic CLI usage examples.                                                                                                                     | `README.md` is comprehensive for MVP. Docstrings are complete for public API.                                                                                                                                                                      | "Generate a template for `README.md` covering installation with Rye/Poetry and basic CLI usage."                                                                                                                      |
| S3.5        | **Tag MVP Release (v0.1.0)**                     | Create a git tag `v0.1.0`. Update version in `pyproject.toml`.                                                                                                                                                                                                                                                                                  | `v0.1.0` tag exists. Version in `pyproject.toml` matches.                                                                                                                                                                            | N/A (Manual git task)                                                                                                                                                                                                  |

---

**Post-MVP Sprints (Brief Outline - Following User's Roadmap):**

*   **Sprint 4: Advanced Stats & Performance**
    *   Implement more aggregators from §2.3 (temporal, per-series).
    *   Address Phase 5: Profile, optimize if needed. Add perf-budget test.
    *   Refine `Game.summarize()` to produce richer game summaries.
*   **Sprint 5: FastAPI Service**
    *   Implement Phase 6: FastAPI endpoints (`/simulate`, `/strategies`).
    *   Dockerize the application.
*   **Sprint 6: SvelteKit UI Prototype**
    *   Implement Phase 8: Basic SvelteKit app fetching from FastAPI.
    *   Render initial charts.
*   **Further Sprints:** Task Queue, Persistence, UI Polish, New Strategies, etc.

---

**How You and AI Collaborate in this Workflow:**

1.  **You (Developer):**
    *   Take one Task ID at a time.
    *   Understand its goal and "Done" criteria.
    *   Formulate specific questions or code generation requests for the AI based on the "AI Assist Request Example" or your own needs.
    *   **Critically review AI-generated code/config:** Check for correctness, style, and completeness.
    *   **Integrate and adapt:** AI code is a starting point. You'll need to fit it into the project, add error handling, and refine it.
    *   **Write/Run Tests:** Ensure the code behaves as expected and meets coverage goals.
    *   Commit frequently with meaningful messages.
    *   Push to `develop` and ensure CI passes.

2.  **AI (Your Assistant):**
    *   Provides boilerplate code for classes, functions, tests based on your prompts.
    *   Generates configuration files (e.g., `pyproject.toml` snippets, `noxfile.py`, CI YAML).
    *   Suggests test cases, especially for edge conditions.
    *   Explains concepts or alternative approaches if you're stuck.
    *   Helps draft documentation.

**Error Handling & Guardrails (AI Interaction):**
*   **"The AI's solution doesn't fit / seems wrong":**
    1.  **Re-prompt:** Be more specific. Provide context (e.g., existing code, the exact error message).
    2.  **Ask for alternatives:** "Can you show me another way to do X?"
    3.  **Break it down:** Ask for smaller pieces of the solution.
    4.  **Fallback:** If the AI is stuck or consistently wrong for a specific sub-task, note it, and you'll need to implement that part manually. This is valuable feedback for understanding AI limitations.
*   **"The AI went in a different direction":**
    1.  Clearly state: "This is not what I asked for. I need X, adhering to constraints Y and Z. Please regenerate focusing on these."
    2.  Provide the "road-map-level design" or specific sprint task details again as context.
*   **Quality Control:**
    *   **Your review is paramount.** Don't blindly trust AI code.
    *   **Linters/Type Checkers:** These are your first line of defense against subtle AI errors.
    *   **Tests:** These are your ultimate guardrail. If AI code breaks tests or doesn't meet test requirements, it's not accepted.

This detailed plan should allow you to sprint effectively towards your CLI MVP. Start with Sprint 0, Task S0.1! Let me know when you're ready to "pick a Phase" (or rather, a Task ID from a Sprint) and we can dive into specifics.
