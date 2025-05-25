# Development Commands Reference

This document shows the **correct** commands to use for this project.

## ✅ **Working Commands**

### **Main Development Workflow**
```bash
cd shut_the_box_sim

# Test suite
uv run pytest                                      # Run all tests  
uv run pytest --cov=stbsim --cov-report=html       # Run tests with coverage report

# Code quality  
uv run sh scripts/lint.sh                          # Run ruff + black checks
uv run sh scripts/typecheck.sh                     # Run mypy type checking
uv run sh scripts/autofix.sh                       # Auto-fix linting issues
uv run black . && uv run ruff format .             # Format code with black + ruff

# Pre-commit hooks
uv run pre-commit install                          # Install pre-commit hooks
uv run pre-commit run --all-files                  # Run pre-commit on all files
```

### **Individual Tool Access**
```bash
# Type checking
uv run python -m mypy src/stbsim tests/test_core.py tests/__init__.py

# Linting & formatting
uv run ruff check . --force-exclude               # Just ruff linting
uv run black --check .                             # Just black format checking
```

### **Alternative Direct Access** 
These work because the tools are installed in the uv environment:
```bash
# Via uv's installed tools
uv run ruff check .
uv run black --check .
uv run pytest
```

## ❌ **Commands That DON'T Work**

These were mentioned in documentation but don't work with the src/ layout:
```bash
# These fail because stbsim is in src/stbsim, not ./stbsim
uv run mypy stbsim       ❌ 
uv run ruff check stbsim ❌
```

## 📋 **Status Summary**

| Tool | Status | Command |
|------|--------|---------|
| **Tests** | ✅ Passing (14/14) | `uv run pytest` |
| **Linting** | ✅ Passing | `uv run sh scripts/lint.sh` |
| **Type Checking** | ✅ Clean | `uv run sh scripts/typecheck.sh` |
| **Formatting** | ✅ Clean | `uv run sh scripts/autofix.sh` |

## 🎯 **Recommended Workflow**

1. **After any code changes (ALWAYS):**
   ```bash
   uv run sh scripts/autofix.sh   # Auto-fix formatting and linting ← START HERE
   uv run sh scripts/lint.sh      # Check for remaining issues
   uv run pytest                  # Ensure tests pass
   ```

2. **For type checking improvements:**
   ```bash
   uv run sh scripts/typecheck.sh # See type issues
   # Fix type annotations as needed
   ```

3. **Pre-commit automation:**
   ```bash
   uv run pre-commit install  # One-time setup
   # Now hooks run automatically on git commit
   ```

## 🔧 **Configuration Notes**

- **Scripts defined in:** `pyproject.toml` under `[tool.rye.scripts]`
- **Actual implementation:** Scripts in `scripts/` directory (lint.sh, typecheck.sh, etc.)
- **Working directory:** All commands assume you're in `shut_the_box_sim/`
- **Dependencies:** Managed by uv, installed in `.venv/`

## 📚 **Documentation Alignment**

The DEVELOPMENT_GUIDE.md mentioned some commands that needed fixing:
- ✅ **Fixed:** `uv run sh scripts/lint.sh`, `uv run sh scripts/typecheck.sh` work correctly
- ✅ **Added:** Individual tool access via direct uv commands  
- ✅ **Clarified:** Direct mypy usage via `uv run python -m mypy ...`
- ✅ **Documented:** What works vs. what doesn't work

This resolves the inconsistency between documentation expectations and actual working commands.