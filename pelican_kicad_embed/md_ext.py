"""Markdown extension for embedding KiCad schematics with KiCanvas.

This extension processes {{ kicad_schematic(...) }} syntax in Markdown files
and converts it to <kicanvas-embed> HTML elements.
"""

from __future__ import annotations

import re
from typing import Any, Sequence

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class KiCadSchematicPreprocessor(Preprocessor):
    """Preprocessor to convert {{ kicad_schematic(...) }} to HTML."""

    # Regex pattern to match {{ kicad_schematic(filename, style="...", controls="...") }}
    PATTERN = re.compile(
        r"\{\{\s*kicad_schematic\s*\(\s*"
        r'(?:["\'](?P<quoted_filename>[^"\']+)["\']|(?P<unquoted_filename>\S+))\s*'  # Filename with or without quotes
        r'(?:,\s*style\s*=\s*["\'](?P<style>[^"\']*)["\'])?'  # Allow empty style=""
        r'(?:,\s*controls\s*=\s*["\'](?P<controls>[^"\']*)["\'])?'  # Allow empty controls=""
        r"\s*\)\s*\}\}",
        re.IGNORECASE,
    )

    def run(self, lines: Sequence[str]) -> list[str]:
        """Process lines to replace kicad_schematic syntax with HTML.

        Args:
            lines: Sequence of lines from the Markdown document.

        Returns:
            List of processed lines with kicad_schematic replaced by HTML.
        """
        new_lines: list[str] = []
        for line in lines:
            new_line = self.PATTERN.sub(self._replace_match, line)
            new_lines.append(new_line)
        return new_lines

    def _replace_match(self, match: Any) -> str:
        """Convert a regex match to the <kicanvas-embed> HTML element.

        Args:
            match: Regex match object containing filename, style, and controls.

        Returns:
            HTML string for the kicanvas-embed element.
        """
        # Get filename from either quoted or unquoted group
        filename = match.group("quoted_filename") or match.group("unquoted_filename")
        style = match.group("style") or ""
        controls = match.group("controls") or ""

        # Build the HTML attributes
        attrs = [f'src="/static/schematics/{filename}"']

        if controls:
            attrs.append(f'controls="{controls}"')

        if style:
            attrs.append(f'style="{style}"')

        return f"<kicanvas-embed {' '.join(attrs)}></kicanvas-embed>"


class KiCadSchematicExtension(Extension):
    """Markdown extension to enable KiCad schematic embedding."""

    def extendMarkdown(self, md: Any) -> None:
        """Register the preprocessor with Markdown.

        Args:
            md: Markdown instance to extend.
        """
        md.preprocessors.register(
            KiCadSchematicPreprocessor(md),
            "kicad_schematic",
            priority=175,  # Run before most other preprocessors
        )


def makeExtension(**kwargs: Any) -> KiCadSchematicExtension:
    """Create and return the extension instance.

    This is the standard Markdown extension entry point.

    Args:
        **kwargs: Configuration options (currently unused).

    Returns:
        KiCadSchematicExtension instance.
    """
    return KiCadSchematicExtension(**kwargs)
