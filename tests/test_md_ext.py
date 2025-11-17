"""Tests for the Markdown extension."""

import unittest

from pelican_kicad_embed.md_ext import KiCadSchematicPreprocessor


class TestMarkdownExtension(unittest.TestCase):
    """Test cases for Markdown extension parsing."""

    def setUp(self):
        """Set up test fixtures."""
        self.preprocessor = KiCadSchematicPreprocessor(None)

    def test_basic_syntax(self):
        """Test basic kicad_schematic syntax without options."""
        line = '{{ kicad_schematic("amplifier.kicad_sch") }}'
        result = self.preprocessor.run([line])
        expected = '<kicanvas-embed src="/static/schematics/amplifier.kicad_sch"></kicanvas-embed>'
        self.assertEqual(result[0], expected)

    def test_with_style(self):
        """Test kicad_schematic with style parameter."""
        line = '{{ kicad_schematic("amp.kicad_sch", style="width: 800px;") }}'
        result = self.preprocessor.run([line])
        self.assertIn('style="width: 800px;"', result[0])
        self.assertIn('src="/static/schematics/amp.kicad_sch"', result[0])

    def test_with_controls(self):
        """Test kicad_schematic with controls parameter."""
        line = '{{ kicad_schematic("amp.kicad_sch", controls="full") }}'
        result = self.preprocessor.run([line])
        self.assertIn('controls="full"', result[0])

    def test_with_all_parameters(self):
        """Test kicad_schematic with all parameters."""
        line = '{{ kicad_schematic("test.kicad_sch", style="width: 100%;", controls="minimal") }}'
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics/test.kicad_sch"', result[0])
        self.assertIn('style="width: 100%;"', result[0])
        self.assertIn('controls="minimal"', result[0])

    def test_no_quotes(self):
        """Test syntax without quotes around filename."""
        line = "{{ kicad_schematic(test.kicad_sch) }}"
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics/test.kicad_sch"', result[0])

    def test_multiple_on_same_line(self):
        """Test multiple embeddings on the same line."""
        line = '{{ kicad_schematic("a.kicad_sch") }} and {{ kicad_schematic("b.kicad_sch") }}'
        result = self.preprocessor.run([line])
        self.assertIn('src="/static/schematics/a.kicad_sch"', result[0])
        self.assertIn('src="/static/schematics/b.kicad_sch"', result[0])

    def test_preserves_other_content(self):
        """Test that non-matching content is preserved."""
        lines = ["Some text before", '{{ kicad_schematic("amp.kicad_sch") }}', "Some text after"]
        result = self.preprocessor.run(lines)
        self.assertEqual(result[0], "Some text before")
        self.assertIn("<kicanvas-embed", result[1])
        self.assertEqual(result[2], "Some text after")


if __name__ == "__main__":
    unittest.main()
