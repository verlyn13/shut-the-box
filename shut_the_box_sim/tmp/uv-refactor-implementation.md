Below is an **end‑to‑end implementation strategy** that turns the migration report into concrete, ticket‑sized work.  It is written so you can drop each numbered item directly into your task‑tracker (Jira, GitHub Projects, Linear, etc.) and run the migration with zero guesswork.

---

## 0  Pre‑flight Gate (½ day)

| Check              | Command / Action                    | Pass Criterion                       |
| ------------------ | ----------------------------------- | ------------------------------------ |
| **Green baseline** | `rye sync --dev && rye run test`    | All tests + coverage pass on `main`. |
| **Lock freeze**    | Commit fresh `requirements*.lock`   | Shas on lockfiles match CI.          |
| **Branch cut**     | `git checkout -b feat/uv-migration` | Spike branch created.                |

---

## 1  Automated Script: “rye‑to‑uv bootstrap” (1 day)

> A one‑off helper that rewrites config, regenerates the lockfile, and stages deletions.
> Keeps the manual work predictable and repeatable for later projects.

```bash
#!/usr/bin/env bash
set -euo pipefail
cd shut_the_box_sim

# 1. Rename config block --------------------------------------------
tomlq -r 'del(.["tool"]["rye"])                                     |
          .["tool"]["uv"] = {managed:true, dev-dependencies:.tool.rye["dev-dependencies"]}' \
      pyproject.toml > pyproject.toml.tmp
mv pyproject.toml.tmp pyproject.toml

# 2. Regenerate lockfile --------------------------------------------
rm -f requirements*.lock
uv sync --dev  # creates uv.lock

# 3. Rewrite script namespace ---------------------------------------
tomlq -r '.["tool"]["uv"]["scripts"] = .tool.uv.scripts //
          (.tool.rye.scripts // {})' pyproject.toml > pyproject.toml.tmp
mv pyproject.toml.tmp pyproject.toml

# 4. Commit helper artifacts ----------------------------------------
git add pyproject.toml uv.lock
git rm requirements*.lock
echo "✅ rye‑to‑uv bootstrap complete."
```

> **Deliverable**: `scripts/dev/bootstrap_uv.sh` committed and executable.

---

## 2  Local Dev Parity (½ day)

1. **Install & pin uv**

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv self pin 0.5.x        # Same binary for every dev
   ```
2. **Run migrated scripts**

   ```bash
   uv sync --dev
   uv run autofix
   uv run lint
   uv run typecheck
   uv run test
   ```
3. **Fix any script‑path differences** (e.g., `pwd` expectations, `.venv` activation).

> **Deliverable**: “Local parity checklist” markdown in PR description.

---

## 3  CI Pipeline Swap (1 day)

### 3.1 Replace setup step

```yaml
# .github/workflows/ci.yml
- uses: eifinger/setup-rye@v3
+ uses: astral-sh/setup-uv@v6
  with:
+   python-version-file: shut_the_box_sim/.python-version   # single version
+   enable-cache: true      # use global uv cache
```

### 3.2 Replace every Rye command

| Before                   | After           |
| ------------------------ | --------------- |
| `rye sync --dev`         | `uv sync --dev` |
| `rye run lint`           | `uv run lint`   |
| `rye run test`           | `uv run test`   |
| `rye pin …` (none in CI) | *(no change)*   |

> **Tip**: run `git grep -n "rye "` and patch each line.

### 3.3 Cache hot‑path

Add:

```yaml
- name: Restore uv cache
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('shut_the_box_sim/uv.lock') }}
```

> **Deliverable**: Green CI on the branch.

---

## 4  Developer Tooling (1 day)

| File                                | Change                                                              |
| ----------------------------------- | ------------------------------------------------------------------- |
| **`.pre-commit-config.yaml`**       | Replace any `rye run` hooks with `uv run`.                          |
| **`noxfile.py`**                    | `python\nsession.run(\"uv\", \"sync\", \"--dev\", external=True)\n` |
| **`Makefile` / local helpers**      | Replace rye calls.                                                  |
| **VS Code `.vscode/settings.json`** | Update onboarding comment: “Run `uv sync --dev` the first time”.    |

---

## 5  Documentation Sweeps (1 day)

1. **Global find‑replace**

   * `rye sync` → `uv sync`
   * `rye run` → `uv run`
   * “Rye” section headings → “uv”.
2. **Update quick‑start snippet**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
cd shut_the_box_sim
uv sync --dev
uv run test
```

3. **Send Docs PR for review** (*non‑blocking on code merge*).

> **Deliverable**: Updated `README.md`, `DEVELOPMENT_GUIDE.md`, `CODE_STANDARDS.md`.

---

## 6  Validation Gate (½ day)

| Scenario            | How to run                                 | Pass           |
| ------------------- | ------------------------------------------ | -------------- |
| **Full test suite** | `uv run test`                              | 100 % green    |
| **Coverage report** | open `reports/coverage_html/index.html`    | Must generate  |
| **Quarto build**    | `uv run quarto render analysis`            | No errors      |
| **CLI smoke**       | `uv run python -m stbsim.cli --n-games 10` | Returns exit 0 |

If any fail, fix before merge.

---

## 7  Merge & Monitor (½ day)

1. **Squash‑merge** `feat/uv-migration` into `develop`.
2. Tag `v0.1.0‑uv` for historical marker.
3. **Watch CI** on `develop` and first `main` merge.

Rollback = `git revert` of merge commit + restore Rye lockfiles (30 min).

---

## 8  Post‑migration Clean‑up Tickets (optional)

| Ticket                                              | Rationale                                                  |
| --------------------------------------------------- | ---------------------------------------------------------- |
| **Enable multi‑version matrix**                     | Drop `.python-version`, add strategy matrix (3.11 + 3.12). |
| **Adopt `uv publish`**                              | If/when PyPI release is desired.                           |
| **Switch to `[project.optional-dependencies.dev]`** | Standard PEP 621 over uv custom block, if preferred.       |

---

## Estimated Timeline (working days)

| Day | Milestone                       |
| --- | ------------------------------- |
| 0   | Pre‑flight gate passes          |
| 1   | Bootstrap script + local parity |
| 2   | CI passes                       |
| 3   | Tooling & docs updated          |
| 4   | Validation gate, code review    |
| 5   | Merge to `develop`              |
| 6   | Promote to `main`, monitor      |

*Total effort*: **\~5 full dev‑days** plus review time.

---

### Success Checklist

* [ ] **uv.lock** committed, Rye lockfiles deleted.
* [ ] **pyproject.toml** contains `[tool.uv]` only.
* [ ] **CI green** on lint, type, test, docs.
* [ ] **README / Guides** mention only uv commands.
* [ ] **Local `uv run autofix && uv run test`** works on macOS, Linux, Windows (if supported).

Once every box is ticked, Rye can be removed from developer machines and the repo’s history marks the end of circular versioning issues.

