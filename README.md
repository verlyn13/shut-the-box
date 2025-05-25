# Shut the Box

A comprehensive Shut the Box game simulation and strategy analysis project.

## Project Structure

This repository contains:

- **`shut_the_box_sim/`** - Main Python simulation package (`stbsim`) with CLI tools
- **`analysis/`** - Quarto-based strategy comparison reports and data analysis
- **`.github/workflows/`** - CI/CD pipeline for automated testing and validation

## Features

- 🎲 **Fast, deterministic simulations** with pluggable strategy support
- 📊 **Statistical analysis** with win rates, scores, and "shut-the-box" frequency tracking
- 🤖 **Multiple AI strategies** for automated gameplay analysis
- 📄 **Automated reporting** with Quarto-generated HTML analysis reports
- 🚦 **Golden-run testing** for CLI regression protection
- 🔁 **Full CI/CD** with comprehensive linting, type checking, and test coverage

## Quick Start

### Prerequisites
- Python 3.12.9+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation & Usage

```bash
# Clone the repository
git clone https://github.com/verlyn13/shut-the-box.git
cd shut-the-box/shut_the_box_sim

# Install dependencies
uv sync --dev

# Run simulations
uv run python -m stbsim.cli --n-games 100 --p1-strategy greedy_max --p2-strategy min_tiles --seed 42

# Run tests
uv run pytest

# Generate analysis reports
cd ../analysis
./render_reports.sh
```

## Development

See [`shut_the_box_sim/README.md`](shut_the_box_sim/README.md) for detailed development instructions.

Essential development commands:
```bash
cd shut_the_box_sim
uv run sh scripts/autofix.sh     # Auto-fix formatting/linting
uv run sh scripts/lint.sh        # Check code quality  
uv run pytest                    # Run test suite
uv run sh scripts/typecheck.sh   # Type checking
```

## License

MIT License - see individual project files for details.