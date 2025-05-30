#!/usr/bin/env bash
# This script runs mypy typechecker.
# It's intended to be run from the project root (shut_the_box_sim/)
# typically via `uv run sh scripts/typecheck.sh`.

set -e

echo "INFO: Running mypy type checker..."
uv run mypy src/stbsim tests/test_core.py tests/__init__.py

echo "INFO: Type checking finished successfully."