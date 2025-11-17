"""Tests for the reStructuredText directive."""

import unittest

from docutils.core import publish_parts

from pelican_kicad_embed.rst_directive import register_directive


class TestRstDirective(unittest.TestCase):
    """Test cases for reStructuredText directive parsing."""

    @classmethod
    def setUpClass(cls):
        """Register the directive before running tests."""
        register_directive()

    def _parse_rst(self, rst_text):
        """Helper to parse reStructuredText and return HTML body."""
        parts = publish_parts(rst_text, writer_name="html")
        return parts["body"]

    def test_basic_syntax(self):
        """Test basic kicad-schematic directive without options."""
        rst = ".. kicad-schematic:: amplifier.kicad_sch"
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/amplifier.kicad_sch"', html)
        self.assertIn("<kicanvas-embed", html)

    def test_with_style_option(self):
        """Test directive with style option."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :style: width: 800px; height: 500px;"""
        html = self._parse_rst(rst)
        self.assertIn('style="width: 800px; height: 500px;"', html)

    def test_with_controls_option(self):
        """Test directive with controls option."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :controls: full"""
        html = self._parse_rst(rst)
        self.assertIn('controls="full"', html)

    def test_with_all_options(self):
        """Test directive with all options."""
        rst = """.. kicad-schematic:: test.kicad_sch
   :style: width: 100%; height: 600px;
   :controls: minimal"""
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/test.kicad_sch"', html)
        self.assertIn('style="width: 100%; height: 600px;"', html)
        self.assertIn('controls="minimal"', html)

    def test_multiple_directives(self):
        """Test multiple directives in same document."""
        rst = """.. kicad-schematic:: a.kicad_sch

.. kicad-schematic:: b.kicad_sch"""
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/a.kicad_sch"', html)
        self.assertIn('src="/static/schematics/b.kicad_sch"', html)

    def test_embedded_in_document(self):
        """Test directive embedded in larger document."""
        rst = """Test Document
=============

Some text before.

.. kicad-schematic:: amp.kicad_sch

Some text after."""
        html = self._parse_rst(rst)
        self.assertIn("<kicanvas-embed", html)
        self.assertIn("Some text before", html)
        self.assertIn("Some text after", html)


if __name__ == "__main__":
    unittest.main()
