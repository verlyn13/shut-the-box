#!/usr/bin/env bash
# This script runs Ruff linter and Black format checker.
# It's intended to be run from the project root (shut_the_box_sim/)
# typically via `rye run lint`.

set -e

echo "INFO: Running Ruff linter..."
ruff check . --force-exclude

echo "INFO: Running Black format checker..."
black --check .

echo "INFO: All lint checks finished successfully."
