# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is a Shut the Box game simulation project with two main components:
- **Root directory**: Contains project documentation and analysis reports
- **`shut_the_box_sim/`**: Main Python package (`stbsim`) managed by Rye

**Always work from `shut_the_box_sim/` directory** for all development commands.

## Core Commands

### Essential Development Workflow
```bash
cd shut_the_box_sim

# Primary commands (use these first)
rye run autofix      # Auto-fix formatting/linting (START HERE)
rye run lint         # Check for remaining issues  
rye run test         # Run test suite
rye run typecheck    # Run mypy type checking

# Coverage and pre-commit
rye run test-cov     # Tests with HTML coverage report
rye run precommit-run # Run all pre-commit hooks
```

### Individual Tools
```bash
# Direct tool access
rye run python -m mypy src/stbsim tests/test_core.py tests/__init__.py
rye run ruff-check   # Ruff linting only
rye run black-check  # Black format checking only
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

- **CLI Tool**: `python -m stbsim.cli` for running simulations
- **Quarto Reports**: Analysis directory contains strategy comparison reports
- **Golden Run Protection**: CLI outputs are regression-tested against fixtures

## Migration Context

Currently on branch `feat/uv-migration` - migrating from Rye to UV package manager. The codebase uses modern Python 3.12+ features and maintains strict code quality standards.