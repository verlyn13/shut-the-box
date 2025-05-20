#!/usr/bin/env bash
# This script applies Ruff auto-fixes and then formats with Black.
# It's intended to be run from the shut_the_box_sim/ project root

echo "INFO: Applying Ruff auto-fixes..."
ruff check . --fix --force-exclude
echo "INFO: Formatting with Black..."
black .
echo "INFO: Autofix script finished."
