#!/usr/bin/env python3
"""Check if there's a new version of KiCanvas available."""

import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen


def get_current_version():
    """Get current KiCanvas version from VERSION file."""
    version_file = Path(__file__).parent.parent / "KICANVAS_VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def get_latest_commit():
    """Get latest commit hash from KiCanvas GitHub repo."""
    url = "https://api.github.com/repos/theacodes/kicanvas/commits/main"
    req = Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")

    try:
        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data["sha"][:7]  # Short hash
    except Exception as e:
        print(f"Error fetching latest version: {e}", file=sys.stderr)
        return None


def main():
    """Check for KiCanvas updates."""
    current = get_current_version()
    latest = get_latest_commit()

    if latest is None:
        print("❌ Could not fetch latest KiCanvas version")
        return 1

    if current is None:
        print(f"⚠️  No version file found. Latest is: {latest}")
        print(f"   Run: echo '{latest}' > KICANVAS_VERSION")
        return 1

    if current != latest:
        print("🔄 KiCanvas update available!")
        print(f"   Current: {current}")
        print(f"   Latest:  {latest}")
        print("   Update: scripts/update_kicanvas.sh")
        return 1

    print(f"✅ KiCanvas is up to date ({current})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
