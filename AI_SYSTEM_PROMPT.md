# 🤖 AI System Instructions: Code Quality Standards

## CRITICAL: Code Formatting and Linting Protocol

**For any AI system working on this codebase:**

### 1. ✅ TOOL CONFIGURATION IS COMPLETE

This project has **FULLY CONFIGURED** code quality tools:
- **Black** (88-char line length)  
- **Ruff 0.11.11** (latest stable, modern `[tool.ruff.lint]` syntax)
- **Pre-commit hooks** (version-pinned and enforced)

**→ Configuration is in `pyproject.toml` and `.pre-commit-config.yaml`**

### 2. 🚫 DO NOT MANUALLY FIX LINE LENGTH ISSUES

**NEVER manually break long lines or edit formatting.** Instead:

1. **Always use the auto-fixer first:** `rye run autofix`
2. **Then check status:** `rye run lint`
3. **Only commit when clean**

### 3. ✅ STANDARD WORKFLOW FOR ANY CODE CHANGES

```bash
# After writing/editing ANY code:
rye run autofix    # Fixes formatting, imports, line length automatically
rye run lint       # Checks for remaining issues  
rye run test       # Validates functionality
```

### 4. 📖 REFERENCE DOCUMENTATION

- **Primary:** `CODE_STANDARDS.md` - Complete formatting standards
- **Commands:** `COMMANDS.md` - All available development commands  
- **Setup:** `DEVELOPMENT_GUIDE.md` - Full development environment setup

### 5. 🎯 KEY PRINCIPLES

1. **Tools handle formatting** - Never manually format code
2. **Configuration exists** - Don't suggest adding Black/Ruff config
3. **Use `rye run autofix`** - This solves 95% of style issues
4. **Pre-commit enforces** - Same rules in dev, CI, and reviews

### Historical Context

**May 2025:** This project initially lacked tool configuration, causing line-length issues. Now fully resolved with modern Ruff 0.11.11 + Black setup. **These problems will not recur** because the configuration is complete and enforced.

---

**→ When helping with this codebase, refer users to run `rye run autofix` for any formatting issues rather than manually editing code.**