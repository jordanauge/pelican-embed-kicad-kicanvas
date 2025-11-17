#!/bin/bash
# Run type checker
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔍 Running type checker..."

# Check if pyright is available
if ! command -v pyright &> /dev/null; then
    echo "⚠️  pyright not found, installing..."
    npm install -g pyright
fi

echo "🔍 Type checking pelican_kicad_embed..."
pyright pelican_kicad_embed/

echo "✅ Type checking passed!"
