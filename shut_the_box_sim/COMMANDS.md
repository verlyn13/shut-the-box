# Development Commands Reference

This document shows the **correct** commands to use for this project.

## ✅ **Working Commands**

### **Main Development Workflow**
```bash
cd shut_the_box_sim

# Test suite
rye run test              # Run all tests  
rye run test-cov          # Run tests with coverage report

# Code quality  
rye run lint              # Run ruff + black checks (via scripts/lint.sh)
rye run typecheck         # Run mypy type checking (via scripts/typecheck.sh)
rye run autofix           # Auto-fix linting issues (via scripts/autofix.sh)
rye run format            # Format code with black + ruff

# Pre-commit hooks
rye run precommit-install # Install pre-commit hooks
rye run precommit-run     # Run pre-commit on all files
```

### **Individual Tool Access**
```bash
# Type checking
rye run python -m mypy src/stbsim tests/test_core.py tests/__init__.py

# Linting & formatting
rye run ruff-check        # Just ruff linting
rye run black-check       # Just black format checking
```

### **Alternative Direct Access** 
These work because the tools are installed in the Rye environment:
```bash
# Via Rye's installed tools (listed in `rye run --list`)
rye run ruff check .
rye run black --check .
rye run pytest
```

## ❌ **Commands That DON'T Work**

These were mentioned in documentation but don't work with the src/ layout:
```bash
# These fail because stbsim is in src/stbsim, not ./stbsim
rye run mypy stbsim       ❌ 
rye run ruff check stbsim ❌
```

## 📋 **Status Summary**

| Tool | Status | Command |
|------|--------|---------|
| **Tests** | ✅ Passing (13/13) | `rye run test` |
| **Linting** | ✅ Passing | `rye run lint` |
| **Type Checking** | ⚠️ 47 type errors | `rye run typecheck` |
| **Formatting** | ✅ Clean | `rye run format` |

## 🎯 **Recommended Workflow**

1. **After any code changes (ALWAYS):**
   ```bash
   rye run autofix         # Auto-fix formatting and linting ← START HERE
   rye run lint            # Check for remaining issues
   rye run test            # Ensure tests pass
   ```

2. **For type checking improvements:**
   ```bash
   rye run typecheck       # See type issues
   # Fix type annotations as needed
   ```

3. **Pre-commit automation:**
   ```bash
   rye run precommit-install  # One-time setup
   # Now hooks run automatically on git commit
   ```

## 🔧 **Configuration Notes**

- **Scripts defined in:** `pyproject.toml` under `[tool.rye.scripts]`
- **Actual implementation:** Scripts in `scripts/` directory (lint.sh, typecheck.sh, etc.)
- **Working directory:** All commands assume you're in `shut_the_box_sim/`
- **Dependencies:** Managed by Rye, installed in `.venv/`

## 📚 **Documentation Alignment**

The DEVELOPMENT_GUIDE.md mentioned some commands that needed fixing:
- ✅ **Fixed:** `rye run lint`, `rye run typecheck` work correctly
- ✅ **Added:** Individual tool access via `rye run ruff-check`, `rye run black-check`  
- ✅ **Clarified:** Direct mypy usage via `rye run python -m mypy ...`
- ✅ **Documented:** What works vs. what doesn't work

This resolves the inconsistency between documentation expectations and actual working commands.