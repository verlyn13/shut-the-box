# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a Shut the Box game simulation project with two main components:
- **Root directory**: Contains project documentation and analysis reports
- **`shut_the_box_sim/`**: Main Python package (`stbsim`) managed by uv

**Always work from `shut_the_box_sim/` directory** for all development commands.

## Core Commands

### Essential Development Workflow
```bash
cd shut_the_box_sim

# Primary commands (use these first)
uv run sh scripts/autofix.sh     # Auto-fix formatting/linting (START HERE)
uv run sh scripts/lint.sh        # Check for remaining issues  
uv run pytest                    # Run test suite
uv run sh scripts/typecheck.sh   # Run mypy type checking

# Coverage and pre-commit
uv run pytest --cov=stbsim --cov-report=html  # Tests with HTML coverage report
uv run pre-commit run --all-files              # Run all pre-commit hooks
```

### Individual Tools
```bash
# Direct tool access
uv run python -m mypy src/stbsim tests/test_core.py tests/__init__.py
uv run ruff check . --force-exclude   # Ruff linting only
uv run black --check .                 # Black format checking only
```

## Architecture Overview

### Core Game Components
- **`core.py`**: `TileRack` class - manages numbered tiles and scoring
- **`game.py`**: `Game` class - orchestrates gameplay between players
- **`player.py`**: `Player` class - represents game participants with strategies
- **`board.py`**: `Board` class - manages game board state
- **`dice.py`**: `DiceManager` class - handles dice rolling mechanics
- **`turn_manager.py`**: `TurnManager` class - manages individual player turns

### Key Design Patterns
- **Strategy Pattern**: Players use pluggable strategies for tile selection
- **Event Logging**: `InMemoryEventLogger` tracks game events for analysis
- **Simulation Framework**: Supports running multiple games with different strategies

### Code Quality Standards
- **Formatting**: Black (88-char line width) + Ruff auto-fixing
- **Type Checking**: MyPy with gradual typing improvements
- **Testing**: Pytest with 80%+ coverage requirement
- **Pre-commit Hooks**: Enforce formatting/linting on commits

## Testing Approach

- **Unit Tests**: `test_core.py`, `test_core_domain.py` for core logic
- **Golden Run Tests**: `test_cli_golden.py` for CLI regression testing
- **Event Logger Tests**: `test_logger_events.py` for logging functionality
- **Coverage Reports**: Generated in `reports/coverage_html/`

## CLI and Analysis

- **CLI Tool**: `uv run python -m stbsim.cli` for running simulations
- **Quarto Reports**: Analysis directory contains strategy comparison reports
- **Golden Run Protection**: CLI outputs are regression-tested against fixtures

## Migration Context

Successfully migrated from Rye to uv package manager. The codebase uses modern Python 3.12+ features and maintains strict code quality standards with uv-managed dependencies.