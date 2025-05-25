#!/usr/bin/env bash
set -euo pipefail

# Navigate to project root
cd "$(dirname "$0")/../.." || exit 1

echo "🚀 Starting rye-to-uv bootstrap migration..."

# 1. Check prerequisites
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found"
    exit 1
fi

# 2. Backup current state
echo "📦 Backing up current pyproject.toml..."
cp pyproject.toml pyproject.toml.backup

# 3. Use sed to rewrite pyproject.toml (simpler approach)
echo "🔧 Rewriting pyproject.toml for uv..."

# Replace [tool.rye] with [tool.uv]
sed -i 's/^\[tool\.rye\]$/[tool.uv]/' pyproject.toml

echo "✅ pyproject.toml updated for uv"

# 4. Remove old lockfiles
echo "🗑️  Removing old Rye lockfiles..."
rm -f requirements*.lock

# 5. Generate new uv.lock
echo "🔄 Generating uv.lock..."
if ! uv sync --dev; then
    echo "❌ uv sync failed. Restoring backup..."
    mv pyproject.toml.backup pyproject.toml
    exit 1
fi

# 6. Stage changes for commit
echo "📋 Staging changes..."
git add pyproject.toml uv.lock
if [ -f requirements.lock ]; then
    git rm requirements.lock || true
fi
if [ -f requirements-dev.lock ]; then
    git rm requirements-dev.lock || true
fi

# 7. Cleanup backup
rm -f pyproject.toml.backup

echo "✅ rye-to-uv bootstrap complete!"
echo ""
echo "Next steps:"
echo "1. Test with: uv run test"
echo "2. Test with: uv run lint"
echo "3. Test with: uv run autofix"
echo "4. Commit changes: git commit -m 'feat: migrate from rye to uv package manager'"