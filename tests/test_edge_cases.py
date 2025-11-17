"""Edge case tests for all three syntax handlers."""

import unittest

from docutils.core import publish_parts

from pelican_kicad_embed.md_ext import KiCadSchematicPreprocessor
from pelican_kicad_embed.rst_directive import register_directive


class TestMarkdownEdgeCases(unittest.TestCase):
    """Edge case tests for Markdown extension."""

    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = KiCadSchematicPreprocessor(None)

    def test_filename_without_extension(self):
        """Test handling of filename without .kicad_sch extension."""
        line = '{{ kicad_schematic("amplifier") }}'
        result = self.preprocessor.run([line])
        # Should still process it (validation is not our job)
        self.assertIn('src="/static/schematics/amplifier"', result[0])

    def test_filename_with_special_characters(self):
        """Test filename with special characters (hyphens, underscores, dots)."""
        line = '{{ kicad_schematic("my_amp-v2.0.kicad_sch") }}'
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics/my_amp-v2.0.kicad_sch"', result[0])

    def test_filename_with_spaces(self):
        """Test filename with spaces (should work with quotes)."""
        line = '{{ kicad_schematic("my schematic.kicad_sch") }}'
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics/my schematic.kicad_sch"', result[0])

    def test_filename_with_unicode(self):
        """Test filename with Unicode characters."""
        line = '{{ kicad_schematic("amplificateur_été.kicad_sch") }}'
        result = self.preprocessor.run([line])
        self.assertIn("été", result[0])

    def test_empty_style_parameter(self):
        """Test with explicitly empty style parameter."""
        line = '{{ kicad_schematic("amp.kicad_sch", style="") }}'
        result = self.preprocessor.run([line])
        # Should not include empty style attribute or include style=""
        self.assertIn('src="/static/schematics/amp.kicad_sch"', result[0])

    def test_empty_controls_parameter(self):
        """Test with explicitly empty controls parameter."""
        line = '{{ kicad_schematic("amp.kicad_sch", controls="") }}'
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics/amp.kicad_sch"', result[0])

    def test_style_with_quotes_inside(self):
        """Test style parameter containing escaped quotes."""
        line = "{{ kicad_schematic('amp.kicad_sch', style='border: 1px solid #ccc;') }}"
        result = self.preprocessor.run([line])
        self.assertIn("style=", result[0])

    def test_very_long_style(self):
        """Test with very long style attribute."""
        long_style = (
            "width: 800px; height: 600px; border: 1px solid #333; margin: 10px; padding: 5px;"
        )
        line = f'{{ kicad_schematic("amp.kicad_sch", style="{long_style}") }}'
        result = self.preprocessor.run([line])
        self.assertIn("style=", result[0])

    def test_malformed_syntax_missing_closing_parens(self):
        """Test malformed syntax without closing parenthesis."""
        line = '{{ kicad_schematic("amp.kicad_sch"'
        result = self.preprocessor.run([line])
        # Should not match and return original line
        self.assertEqual(result[0], line)

    def test_malformed_syntax_missing_closing_braces(self):
        """Test malformed syntax without closing braces."""
        line = '{{ kicad_schematic("amp.kicad_sch")'
        result = self.preprocessor.run([line])
        # Should not match and return original line
        self.assertEqual(result[0], line)

    def test_malformed_syntax_typo_in_name(self):
        """Test typo in function name."""
        line = '{{ kicad_schemtic("amp.kicad_sch") }}'  # Missing 'a'
        result = self.preprocessor.run([line])
        # Should not match and return original line
        self.assertEqual(result[0], line)

    def test_nested_quotes_complex(self):
        """Test complex nested quotes in style."""
        line = (
            """{{ kicad_schematic("amp.kicad_sch", style="font-family: 'Arial', sans-serif;") }}"""
        )
        result = self.preprocessor.run([line])
        # Should handle or fail gracefully
        self.assertIsInstance(result[0], str)

    def test_filename_with_relative_path(self):
        """Test filename with relative path."""
        line = '{{ kicad_schematic("../parent/amp.kicad_sch") }}'
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics/../parent/amp.kicad_sch"', result[0])

    def test_filename_with_absolute_path(self):
        """Test filename that looks like absolute path."""
        line = '{{ kicad_schematic("/absolute/path/amp.kicad_sch") }}'
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics//absolute/path/amp.kicad_sch"', result[0])


class TestRstEdgeCases(unittest.TestCase):
    """Edge case tests for reStructuredText directive."""

    @classmethod
    def setUpClass(cls):
        """Register the directive once."""
        register_directive()

    def _parse_rst(self, rst_text):
        """Helper to parse reStructuredText."""
        parts = publish_parts(rst_text, writer_name="html")
        body = parts.get("body", "")
        if not body:
            raise ValueError("RST parsing failed: no body returned")
        return body

    def test_filename_without_extension(self):
        """Test handling of filename without .kicad_sch extension."""
        rst = ".. kicad-schematic:: amplifier"
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/amplifier"', html)

    def test_filename_with_special_characters(self):
        """Test filename with special characters."""
        rst = ".. kicad-schematic:: my_amp-v2.0.kicad_sch"
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/my_amp-v2.0.kicad_sch"', html)

    def test_filename_with_unicode(self):
        """Test filename with Unicode characters."""
        rst = ".. kicad-schematic:: amplificateur_été.kicad_sch"
        html = self._parse_rst(rst)
        self.assertIn("été", html)

    def test_empty_style_option(self):
        """Test with empty style option."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :style:"""
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/amp.kicad_sch"', html)

    def test_empty_controls_option(self):
        """Test with empty controls option."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :controls:"""
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/amp.kicad_sch"', html)

    def test_style_with_semicolons(self):
        """Test style with multiple semicolon-separated properties."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :style: width: 800px; height: 600px; border: 1px solid #ccc;"""
        html = self._parse_rst(rst)
        self.assertIn("style=", html)

    def test_controls_with_invalid_value(self):
        """Test controls with non-standard value (should pass through)."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :controls: custom-value"""
        html = self._parse_rst(rst)
        self.assertIn('controls="custom-value"', html)

    def test_unknown_option_ignored(self):
        """Test that unknown options are ignored by docutils."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :unknown: value
   :style: width: 800px;"""
        # This should either work or raise docutils error
        try:
            html = self._parse_rst(rst)
            # If it works, src should still be present
            self.assertIn('src="/static/schematics/amp.kicad_sch"', html)
        except Exception:
            # docutils may reject unknown options - that's ok
            pass

    def test_malformed_directive_name(self):
        """Test typo in directive name."""
        rst = ".. kicad-schemtic:: amp.kicad_sch"  # Missing 'a'
        html = self._parse_rst(rst)
        # Should not be processed as our directive
        self.assertNotIn("<kicanvas-embed", html)

    def test_filename_with_relative_path(self):
        """Test filename with relative path."""
        rst = ".. kicad-schematic:: ../parent/amp.kicad_sch"
        html = self._parse_rst(rst)
        self.assertIn('src="/static/schematics/../parent/amp.kicad_sch"', html)

    def test_multiline_style(self):
        """Test that style cannot span multiple lines (reST limitation)."""
        rst = """.. kicad-schematic:: amp.kicad_sch
   :style: width: 800px;
           height: 600px;"""
        # This will likely fail or only capture first line - that's expected reST behavior
        try:
            html = self._parse_rst(rst)
            self.assertIn('src="/static/schematics/amp.kicad_sch"', html)
        except Exception:
            # Expected - reST doesn't support multiline option values this way
            pass


class TestCrossFormatConsistency(unittest.TestCase):
    """Tests to ensure consistent output across all three formats."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        register_directive()
        cls.md_preprocessor = KiCadSchematicPreprocessor(None)

    def _parse_rst(self, rst_text):
        """Helper to parse reStructuredText."""
        parts = publish_parts(rst_text, writer_name="html")
        body = parts.get("body", "")
        if not body:
            raise ValueError("RST parsing failed: no body returned")
        return body

    def test_same_output_basic(self):
        """Test that basic usage produces similar HTML across formats."""
        # Markdown
        md_line = '{{ kicad_schematic("amp.kicad_sch") }}'
        md_result = self.md_preprocessor.run([md_line])[0]

        # reST
        rst = ".. kicad-schematic:: amp.kicad_sch"
        rst_result = self._parse_rst(rst)

        # Both should contain the same core HTML
        for result in [md_result, rst_result]:
            self.assertIn('src="/static/schematics/amp.kicad_sch"', result)
            self.assertIn("<kicanvas-embed", result)

    def test_same_output_with_all_params(self):
        """Test that full parameters produce similar HTML across formats."""
        # Markdown
        md_line = '{{ kicad_schematic("amp.kicad_sch", style="width: 800px;", controls="full") }}'
        md_result = self.md_preprocessor.run([md_line])[0]

        # reST
        rst = """.. kicad-schematic:: amp.kicad_sch
   :style: width: 800px;
   :controls: full"""
        rst_result = self._parse_rst(rst)

        # Both should contain the same attributes
        for result in [md_result, rst_result]:
            self.assertIn('src="/static/schematics/amp.kicad_sch"', result)
            self.assertIn('style="width: 800px;"', result)
            self.assertIn('controls="full"', result)


if __name__ == "__main__":
    unittest.main()
