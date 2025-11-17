#!/bin/bash
# Update KiCanvas to latest version from GitHub
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_FILE="$REPO_ROOT/content/static/js/kicanvas.js"
VERSION_FILE="$REPO_ROOT/KICANVAS_VERSION"

# Get latest commit hash
echo "🔍 Fetching latest KiCanvas version..."
LATEST_COMMIT=$(curl -s https://api.github.com/repos/theacodes/kicanvas/commits/main | grep -o '"sha": "[^"]*' | head -1 | cut -d'"' -f4 | cut -c1-7)

if [ -z "$LATEST_COMMIT" ]; then
    echo "❌ Failed to fetch latest version"
    exit 1
fi

echo "📥 Downloading KiCanvas ($LATEST_COMMIT)..."

# Create directory if needed
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Download latest kicanvas.js
curl -L -o "$OUTPUT_FILE" "https://kicanvas.org/kicanvas/kicanvas.js"

# Update version file
echo "$LATEST_COMMIT" > "$VERSION_FILE"

echo "✅ KiCanvas updated to $LATEST_COMMIT"
echo "   File: $OUTPUT_FILE ($(du -h "$OUTPUT_FILE" | cut -f1))"
