Below is a **disciplined research roadmap** that will surface every fact we still need before we touch a line of YAML or TOML.  Treat it as a checklist: the next person who claims “we’re blocked” should be able to point to the exact unanswered item in this list.

---

## 0  Scope & Success Criteria (define first)

| Item                       | Target                                                                                                                                                                                                                                                                    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Primary goal**           | Ship a *green‑CI* migration from Rye → uv without breaking local dev or release packaging.                                                                                                                                                                                |
| **Secondary goals**        | • Keep ability to pin **one** Python for reproducibility **or** run a version matrix.<br>• Keep all current scripts, lint/type/test targets, pre‑commit, Nox.<br>• Maintain “single‑command onboarding” for newcomers (`uv sync --dev && uv run autofix && uv run test`). |
| **Out‑of‑scope** (for now) | Dropping/adding features (e.g. Poetry‑style publishing), rewriting simulation code, re‑structuring monorepo.                                                                                                                                                              |

Any later arguments (“but feature X was nice!”) are settled by referencing the table above.

---

## 1  Inventory the Current State (fact gathering)

| Sub‑task                       | Command / artefact                                     | Deliverable                                                                                          |
| ------------------------------ | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **1.1 Repo tree**              | `tree -L 2` at repo root                               | Diagram of directories; mark where `pyproject.toml`, lockfiles, `noxfile.py`, GitHub workflows live. |
| **1.2 Rye artefacts search**   | `git grep -n -e 'rye ' -e '\[tool\.rye'`               | List of files that will break if Rye disappears.                                                     |
| **1.3 CI pipelines**           | Open every `.github/workflows/*.yml`                   | Extract: job names, steps that call Rye, Python‑matrix definitions, cache keys.                      |
| **1.4 Local tooling**          | `rye show config` and `.rye/` dir listing (if present) | Document any non‑default config (e.g. behaviour.use‑uv flag).                                        |
| **1.5 Scripts & entry points** | Parse `[tool.rye.scripts]` and any Makefile            | Table of dev commands that must keep working (lint, typecheck, docs, release).                       |
| **1.6 Packaging**              | `grep -n 'build-backend' pyproject.toml`               | Record current backend (Hatchling) and wheel settings.                                               |
| **1.7 Publish flow**           | Search workflows for `twine`/`publish`                 | Note if trusted‑publishing, API tokens, or manual upload is used.                                    |
| **1.8 OS support**             | Ask team: “any Windows devs? any ARM Macs?”            | Decide if uv’s platform coverage suffices.                                                           |

---

## 2  Stakeholder Requirements Elicitation

| Question                                                                                                | Who owns the answer? | Why it matters                                                             |
| ------------------------------------------------------------------------------------------------------- | -------------------- | -------------------------------------------------------------------------- |
| A. Do we **need** multiple Python versions in CI, or is single‑pin okay?                                | Tech lead / QA       | Decides whether we keep `.python-version` or generate it per‑job.          |
| B. Are there **Rye‑specific niceties** people rely on (e.g. `rye self add`, `rye publish`, workspaces)? | Each developer       | We must map them 1‑to‑1 (tool.uv, uv workspaces) or document replacements. |
| C. Are release wheels **signed / built** in CI?                                                         | Release manager      | uv can build & publish, but workflow must be ported.                       |
| D. **Security / reproducibility** bar?                                                                  | DevOps / security    | Determines if we use `uv sync --locked` + checksums in CI.                 |
| E. **Timeline / freeze dates**?                                                                         | PM                   | Controls whether we migrate on mainline or a long‑running branch.          |

Document answers in a living “Migration‑FAQ.md”.

---

## 3  External Landscape Research

| Topic                          | Activity                                                                                                         | Sources                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **3.1 uv feature map**         | Build table “Rye X → uv Y” (scripts, python pin, lock, publish).                                                 | Official docs ([Astral Docs][1]), migration discussion ([GitHub][2])     |
| **3.2 setup‑uv action**        | Prototype a minimal workflow that:<br>• installs Python<br>• caches global uv cache<br>• runs `uv sync --locked` | `astral-sh/setup-uv` README ([GitHub][3], [GitHub][4])                   |
| **3.3 Known migration issues** | Read open uv issues labelled *migration* or *rye*; skim blog post “Rye grows with uv”.                           | GitHub issues; Lucumr blog ([Armin Ronacher's Thoughts and Writings][5]) |
| **3.4 Third‑party helpers**    | Evaluate `rye-uv` CLI converter ([GitHub][6]) – is it mature enough to start?                                    |                                                                          |

Record take‑aways in a short memo “external‑findings.md”.

---

## 4  Spike / Proof‑of‑Concept (branch‑only)

1. **Create branch** `spike/uv-migration`.
2. Run `uv init --lock` inside `shut_the_box_sim/`; commit `uv.lock`.
3. Manually translate one script (`lint`) to `[tool.uv.scripts]`.
4. Replace Rye steps in *one* GitHub workflow with `setup-uv`.
5. Push; observe CI times & failures; capture logs.

Success = tests & lint pass in < 10 min.
Failure modes collected here feed back into requirements.

---

## 5  Risk Register & Decision Matrix

For each open question (e.g. “drop `.python-version`?”) create:

| Decision | Options | Pros | Cons | Data still needed |
| -------- | ------- | ---- | ---- | ----------------- |

Populate after Spike.  Example entry:

\| Keep `.python-version` | ✅ single reproducible env | ❌ can’t matrix‑test 3.11 | How many prod users run 3.11? |

---

## 6  Deliverables & Timeline

| Day        | Output                                               |
| ---------- | ---------------------------------------------------- |
| **D + 2**  | Sections 1–3 complete; Migration‑FAQ drafted.        |
| **D + 4**  | Spike branch + CI logs; preliminary decision matrix. |
| **D + 5**  | Go/No‑go meeting; assign refactor tasks.             |
| **D + 10** | Draft PR with full migration; reviewers sign off.    |
| **D + 12** | Merge to `develop`; monitor green CI for 3 days.     |

---

### Checklist review gate

Before coding the **real** refactor, confirm every box below is ticked:

* [ ] Current Rye footprint fully inventoried (1.1–1.8).
* [ ] Stakeholder answers recorded (Section 2).
* [ ] External limitations acknowledged (3.1–3.4).
* [ ] Spike proves uv works with tests + lint.
* [ ] Risk matrix shows no red “unknowns”.

Only then do we schedule the full rewrite.

---

By following this research plan you’ll turn “unknown unknowns” into explicit, trackable tasks, and make the eventual `uv` migration almost a formality rather than another round of firefighting.

[1]: https://docs.astral.sh/uv/?utm_source=chatgpt.com "uv - Astral Docs"
[2]: https://github.com/astral-sh/rye/discussions/1342?utm_source=chatgpt.com "Rye and uv · astral-sh rye · Discussion #1342 - GitHub"
[3]: https://github.com/astral-sh/setup-uv?utm_source=chatgpt.com "astral-sh/setup-uv: Set up your GitHub Actions workflow ... - GitHub"
[4]: https://github.com/marketplace/actions/astral-sh-setup-uv?utm_source=chatgpt.com "astral-sh/setup-uv · Actions · GitHub Marketplace"
[5]: https://lucumr.pocoo.org/2024/2/15/rye-grows-with-uv/?utm_source=chatgpt.com "Rye Grows With UV | Armin Ronacher's Thoughts and Writings"
[6]: https://github.com/lucianosrp/rye-uv?utm_source=chatgpt.com "Simple CLI tool to migrate from Rye to Uv - GitHub"

