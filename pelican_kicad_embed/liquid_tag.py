"""Liquid Tag handler for embedding KiCad schematics with KiCanvas.

This module provides Liquid Tag support for the plugin. It is conditionally
imported only if the pelican-liquid-tags plugin is installed.

Usage:
    {% kicad_schematic filename.kicad_sch style="width: 800px;" controls="full" %}
"""

from __future__ import annotations

import re
from typing import Any

from liquid_tags.mdx_liquid_tags import LiquidTags  # type: ignore[import-untyped]


@LiquidTags.register("kicad_schematic")  # type: ignore[misc]
def kicad_schematic_tag(preprocessor: Any, tag: str, markup: str) -> str:
    """Process the kicad_schematic Liquid Tag.

    Args:
        preprocessor: Liquid tag preprocessor instance.
        tag: The tag name ('kicad_schematic').
        markup: The tag content/arguments.

    Returns:
        HTML string for the kicanvas-embed element.
    """
    # Parse the markup: filename followed by style/controls in any order
    # Extract filename first
    filename_match = re.match(r"^\s*(\S+)", markup)
    if not filename_match:
        return f"<!-- Invalid kicad_schematic syntax: {markup} -->"

    filename = filename_match.group(1)

    # Extract style and controls (order-independent)
    style_match = re.search(r'style\s*=\s*["\']([^"\']*)["\']', markup, re.IGNORECASE)
    controls_match = re.search(r'controls\s*=\s*["\']([^"\']*)["\']', markup, re.IGNORECASE)

    style = style_match.group(1) if style_match else ""
    controls = controls_match.group(1) if controls_match else ""

    # Build the HTML attributes
    attrs = [f'src="/static/schematics/{filename}"']

    if controls:
        attrs.append(f'controls="{controls}"')

    if style:
        attrs.append(f'style="{style}"')

    return f"<kicanvas-embed {' '.join(attrs)}></kicanvas-embed>"
