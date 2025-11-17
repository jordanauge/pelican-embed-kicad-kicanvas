"""Tests for Jinja2 template function."""

import unittest

from pelican_kicad_embed import kicad_schematic


class TestJinja2Function(unittest.TestCase):
    """Test the kicad_schematic function for Jinja2 templates."""

    def test_basic_call(self):
        """Test basic function call with just filename."""
        # Pass empty context dict (mimics Jinja2 @pass_context behavior)
        result = kicad_schematic({}, "test.kicad_sch")
        self.assertIn("kicanvas-embed", result)
        self.assertIn('src="test.kicad_sch"', result)
        self.assertIn('controls="all"', result)
        self.assertIn('style="width: 100%; height: 600px;"', result)

    def test_with_custom_style(self):
        """Test with custom style parameter."""
        result = kicad_schematic({}, "test.kicad_sch", style="width: 800px; height: 400px;")
        self.assertIn('style="width: 800px; height: 400px;"', result)

    def test_with_custom_controls(self):
        """Test with custom controls parameter."""
        result = kicad_schematic({}, "test.kicad_sch", controls="zoom,pan")
        self.assertIn('controls="zoom,pan"', result)

    def test_with_all_parameters(self):
        """Test with all parameters specified."""
        result = kicad_schematic(
            {},  # context
            "path/to/schematic.kicad_sch",
            style="width: 1000px; height: 800px;",
            controls="zoom,pan,theme",
        )
        self.assertIn('src="path/to/schematic.kicad_sch"', result)
        self.assertIn('style="width: 1000px; height: 800px;"', result)
        self.assertIn('controls="zoom,pan,theme"', result)

    def test_empty_strings_use_defaults(self):
        """Test that empty strings trigger default values."""
        result = kicad_schematic({}, "test.kicad_sch", style="", controls="")
        self.assertIn('style="width: 100%; height: 600px;"', result)
        self.assertIn('controls="all"', result)

    def test_returns_string(self):
        """Test that function returns a string."""
        result = kicad_schematic({}, "test.kicad_sch")
        self.assertIsInstance(result, str)

    def test_html_structure(self):
        """Test that returned HTML has correct structure."""
        result = kicad_schematic({}, "test.kicad_sch")
        self.assertTrue(result.startswith("<kicanvas-embed"))
        self.assertTrue(result.endswith("</kicanvas-embed>"))


if __name__ == "__main__":
    unittest.main()
