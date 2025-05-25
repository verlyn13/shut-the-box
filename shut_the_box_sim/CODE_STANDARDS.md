# 🛠️ Code Formatting & Linting — Project Standards and Workflow

## Single Source of Truth: How We Handle Linting and Auto-formatting

### 1. Tooling & Config:

* **Black:** Official formatter; enforces 88-character line width and style rules.
* **Ruff:** Linter and autofixer—Ruff v0.11.11+ is required (config: `[tool.ruff]`/`[tool.ruff.lint]` in `pyproject.toml`).
* **Pre-commit hooks:** Configured via `.pre-commit-config.yaml` to use these exact versions.
  **Every dev/CI run uses the same versions and rules.**

### 2. Configuration

* **`pyproject.toml`** now includes:
  ```toml
  [tool.black]
  line-length = 88

  [tool.ruff]
  line-length = 88
  target-version = "py311"

  [tool.ruff.lint]
  select = ["E", "W", "F", "I", "B", "C4", "UP"]
  ignore = ["E501"]  # line too long, handled by black
  fixable = ["ALL"]
  ```
* **`.pre-commit-config.yaml`** pins Ruff/Black versions to ensure consistency across dev machines and CI.

### 3. Workflow & Automation

#### New and Updated Files

* **Always run the auto-fixer before staging code or opening a PR.**
* Adopt the following workflow for every code/documentation change:
  ```bash
  uv run sh scripts/autofix.sh     # Runs auto-fixers (Black/Ruff) over the codebase
  uv run sh scripts/lint.sh        # Checks for any remaining linting issues
  uv run sh scripts/typecheck.sh   # For type/check compliance
  uv run pytest                    # For correctness (pytest/golden run)
  ```
* This applies to *all new files as well as edits to existing modules,* especially after writing code or applying patches.

#### On commit/PR:

* **Pre-commit hooks are enforced!**
  * If anything fails or is auto-fixed, repeat above commands until clean (tools won't let you commit out-of-style code).

#### In CI:

* **CI pipeline re-validates:**
  * Auto-formatting, lint, typecheck, and tests.
  * Configuration in `pyproject.toml` and `.pre-commit-config.yaml` keeps dev, CI, and PRs 100% consistent.

### 4. Best Practice:

**Habit:**
Always run the auto-fix (`uv run sh scripts/autofix.sh`) immediately after writing or patching any new/updated file. Do not continue unless formatting and lint all pass cleanly.

---

### Why Is This Important?

* Ensures professional, readable, and diff-friendly codebase
* Smooth contributor onboarding—nobody fights over style
* Enforces a "one and only one standard" across all local dev, CI, and reviews

### Historical Note:

The line-length/linter issues in spring 2025 arose because the project initially lacked a unified configuration. Now, with modern `[tool.black]`, `[tool.ruff]`, and pre-commit alignment, these problems are gone for good.

---

## Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `uv run sh scripts/autofix.sh` | **Auto-fix all formatting and linting issues** |
| `uv run sh scripts/lint.sh` | Check for remaining linting issues |
| `uv run black . && uv run ruff format .` | Run Black + Ruff formatting |
| `uv run sh scripts/typecheck.sh` | Run mypy type checking |
| `uv run pytest` | Run test suite |
| `uv run pre-commit run --all-files` | Run all pre-commit hooks manually |

## Tool Versions (As of May 2025)

* **Ruff:** 0.11.11 (latest stable)
* **Black:** 24.3.0
* **Python:** 3.11+
* **Pre-commit:** Uses exact same versions via `.pre-commit-config.yaml`

**→ This ensures 100% consistency between local development, CI, and code reviews.**