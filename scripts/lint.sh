#!/bin/bash
# Run code linters
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔍 Running linters..."

# Check if ruff is available
if ! command -v ruff &> /dev/null; then
    echo "⚠️  ruff not found, installing..."
    pip install ruff
fi

echo "📝 Checking code formatting..."
ruff format --check pelican_kicad_embed/ scripts/

echo "🔍 Running linter..."
ruff check pelican_kicad_embed/ scripts/

echo "✅ All linting checks passed!"
