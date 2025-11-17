"""Tests for the Liquid Tag handler."""

import sys
import unittest
from unittest.mock import MagicMock


class TestLiquidTag(unittest.TestCase):
    """Test cases for Liquid Tag syntax parsing."""

    @classmethod
    def setUpClass(cls):
        """Mock liquid_tags module before importing liquid_tag."""
        # Create mock modules
        mock_liquid_tags = MagicMock()
        mock_mdx = MagicMock()
        mock_liquid_tags_class = MagicMock()
        mock_mdx.LiquidTags = mock_liquid_tags_class

        # Setup register decorator mock
        cls.registered_tags = {}

        def register_decorator(tag_name):
            def decorator(func):
                cls.registered_tags[tag_name] = func
                return func

            return decorator

        mock_liquid_tags_class.register = register_decorator

        sys.modules["liquid_tags"] = mock_liquid_tags
        sys.modules["liquid_tags.mdx_liquid_tags"] = mock_mdx

        # Now import the module
        from pelican_kicad_embed import liquid_tag

        cls.liquid_tag_module = liquid_tag

    def setUp(self):
        """Set up per-test fixtures."""
        # Get the registered function as an instance variable
        self.kicad_schematic_tag = self.__class__.registered_tags.get("kicad_schematic")

    @classmethod
    def tearDownClass(cls):
        """Clean up mocks."""
        if "liquid_tags" in sys.modules:
            del sys.modules["liquid_tags"]
        if "liquid_tags.mdx_liquid_tags" in sys.modules:
            del sys.modules["liquid_tags.mdx_liquid_tags"]

    def test_basic_syntax(self):
        """Test basic kicad_schematic Liquid Tag without options."""
        markup = "amplifier.kicad_sch"
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('src="/static/schematics/amplifier.kicad_sch"', result)
        self.assertIn("<kicanvas-embed", result)

    def test_with_style(self):
        """Test Liquid Tag with style parameter."""
        markup = 'amp.kicad_sch style="width: 800px; height: 500px;"'
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('style="width: 800px; height: 500px;"', result)
        self.assertIn('src="/static/schematics/amp.kicad_sch"', result)

    def test_with_controls(self):
        """Test Liquid Tag with controls parameter."""
        markup = 'amp.kicad_sch controls="full"'
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('controls="full"', result)
        self.assertIn('src="/static/schematics/amp.kicad_sch"', result)

    def test_with_all_parameters(self):
        """Test Liquid Tag with all parameters."""
        markup = 'test.kicad_sch style="width: 100%;" controls="minimal"'
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('src="/static/schematics/test.kicad_sch"', result)
        self.assertIn('style="width: 100%;"', result)
        self.assertIn('controls="minimal"', result)

    def test_with_single_quotes(self):
        """Test Liquid Tag with single quotes around parameters."""
        markup = "amp.kicad_sch style='width: 800px;' controls='full'"
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('style="width: 800px;"', result)
        self.assertIn('controls="full"', result)

    def test_parameters_order_flexible(self):
        """Test that parameter order doesn't matter."""
        markup1 = 'file.kicad_sch style="width: 100%;" controls="full"'
        markup2 = 'file.kicad_sch controls="full" style="width: 100%;"'

        result1 = self.kicad_schematic_tag(None, "kicad_schematic", markup1)
        result2 = self.kicad_schematic_tag(None, "kicad_schematic", markup2)

        # Both should contain all attributes (order may vary)
        for result in [result1, result2]:
            self.assertIn('src="/static/schematics/file.kicad_sch"', result)
            self.assertIn('style="width: 100%;"', result)
            self.assertIn('controls="full"', result)

    def test_whitespace_handling(self):
        """Test that extra whitespace is handled correctly."""
        markup = '  amplifier.kicad_sch   style="width: 800px;"   controls="full"  '
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('src="/static/schematics/amplifier.kicad_sch"', result)
        self.assertIn('style="width: 800px;"', result)
        self.assertIn('controls="full"', result)

    def test_filename_with_path(self):
        """Test filename with subdirectory path."""
        markup = "subdir/amplifier.kicad_sch"
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('src="/static/schematics/subdir/amplifier.kicad_sch"', result)

    def test_invalid_syntax_returns_comment(self):
        """Test that invalid syntax returns an HTML comment."""
        markup = ""  # Empty markup
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn("<!--", result)
        self.assertIn("Invalid", result)

    def test_malformed_parameters(self):
        """Test handling of malformed parameters."""
        # Missing closing quote
        markup = 'file.kicad_sch style="width: 800px;'
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        # Should still process the filename
        self.assertIn('src="/static/schematics/file.kicad_sch', result)

    def test_case_insensitive(self):
        """Test that parameter names are case-insensitive."""
        markup = 'file.kicad_sch STYLE="width: 100%;" CONTROLS="full"'
        result = self.kicad_schematic_tag(None, "kicad_schematic", markup)

        self.assertIn('style="width: 100%;"', result)
        self.assertIn('controls="full"', result)


class TestLiquidTagIntegration(unittest.TestCase):
    """Integration tests for Liquid Tag module loading."""

    def test_module_not_imported_without_liquid_tags(self):
        """Test that liquid_tag module fails gracefully without liquid_tags."""
        # Remove liquid_tags from sys.modules if present
        if "liquid_tags" in sys.modules:
            del sys.modules["liquid_tags"]
        if "pelican_kicad_embed.liquid_tag" in sys.modules:
            del sys.modules["pelican_kicad_embed.liquid_tag"]

        # Try importing the main module - should work even without liquid_tags
        try:
            from pelican_kicad_embed import register_liquid_tag

            register_liquid_tag()
            success = True
        except ImportError:
            success = False

        # Should succeed or fail silently
        self.assertTrue(success)

    def test_liquid_tag_imported_when_available(self):
        """Test that liquid_tag is imported when liquid_tags is available."""
        from pelican_kicad_embed import register_liquid_tag

        # Should not raise exception
        register_liquid_tag()

        self.assertTrue(True)  # If no exception, test passes


if __name__ == "__main__":
    unittest.main()
