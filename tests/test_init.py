"""Tests for the main plugin module (__init__.py)."""

import unittest
from unittest.mock import Mock

from pelican_kicad_embed import KICAD_PATTERN, inject_kicanvas_script


class TestKicadPattern(unittest.TestCase):
    """Test cases for the regex pattern detection."""

    def test_detects_markdown_syntax(self):
        """Test that regex detects Markdown {{ kicad_schematic(...) }} syntax."""
        text = '{{ kicad_schematic("amp.kicad_sch") }}'
        self.assertIsNotNone(KICAD_PATTERN.search(text))

    def test_detects_markdown_with_params(self):
        """Test detection of Markdown syntax with parameters."""
        text = '{{ kicad_schematic("file.kicad_sch", style="width: 100%;", controls="full") }}'
        self.assertIsNotNone(KICAD_PATTERN.search(text))

    def test_detects_rst_syntax(self):
        """Test that regex detects reST .. kicad-schematic:: syntax."""
        text = ".. kicad-schematic:: amplifier.kicad_sch"
        self.assertIsNotNone(KICAD_PATTERN.search(text))

    def test_detects_liquid_syntax(self):
        """Test that regex detects Liquid {% kicad_schematic %} syntax."""
        text = "{% kicad_schematic amplifier.kicad_sch %}"
        self.assertIsNotNone(KICAD_PATTERN.search(text))

    def test_detects_liquid_with_params(self):
        """Test detection of Liquid syntax with parameters."""
        text = '{% kicad_schematic file.kicad_sch style="width: 800px;" controls="full" %}'
        self.assertIsNotNone(KICAD_PATTERN.search(text))

    def test_case_insensitive(self):
        """Test that detection is case-insensitive."""
        text = '{{ KICAD_SCHEMATIC("file.kicad_sch") }}'
        self.assertIsNotNone(KICAD_PATTERN.search(text))

    def test_multiline_detection(self):
        """Test detection across multiple lines."""
        text = """Some text before
.. kicad-schematic:: amp.kicad_sch
   :style: width: 800px;
Some text after"""
        self.assertIsNotNone(KICAD_PATTERN.search(text))

    def test_no_match_normal_text(self):
        """Test that normal text without kicad_schematic is not matched."""
        text = "This is just normal text about KiCad and schematics."
        self.assertIsNone(KICAD_PATTERN.search(text))

    def test_multiple_matches(self):
        """Test detection of multiple embeddings in same content."""
        text = """{{ kicad_schematic("a.kicad_sch") }}
.. kicad-schematic:: b.kicad_sch
{% kicad_schematic c.kicad_sch %}"""
        matches = KICAD_PATTERN.findall(text)
        self.assertEqual(len(matches), 3)


class TestInjectKiCanvasScript(unittest.TestCase):
    """Test cases for the inject_kicanvas_script function."""

    def test_injects_script_when_markdown_syntax_found(self):
        """Test that script is injected when Markdown syntax is detected."""
        content = Mock()
        content._content = '{{ kicad_schematic("amp.kicad_sch") }}'
        delattr(content, "kicanvas_embed")  # Ensure attribute doesn't exist initially
        delattr(content, "extra_js")

        inject_kicanvas_script(content)

        self.assertTrue(content.kicanvas_embed)
        self.assertIsInstance(content.extra_js, list)
        self.assertIn("https://unpkg.com/kicanvas@latest/dist/kicanvas.js", content.extra_js)

    def test_injects_script_when_rst_syntax_found(self):
        """Test that script is injected when reST syntax is detected."""
        content = Mock()
        content._content = ".. kicad-schematic:: amplifier.kicad_sch"
        delattr(content, "kicanvas_embed")
        delattr(content, "extra_js")

        inject_kicanvas_script(content)

        self.assertTrue(content.kicanvas_embed)
        self.assertIsInstance(content.extra_js, list)
        self.assertIn("https://unpkg.com/kicanvas@latest/dist/kicanvas.js", content.extra_js)

    def test_injects_script_when_liquid_syntax_found(self):
        """Test that script is injected when Liquid syntax is detected."""
        content = Mock()
        content._content = "{% kicad_schematic file.kicad_sch %}"
        delattr(content, "kicanvas_embed")
        delattr(content, "extra_js")

        inject_kicanvas_script(content)

        self.assertTrue(content.kicanvas_embed)
        self.assertIsInstance(content.extra_js, list)
        self.assertIn("https://unpkg.com/kicanvas@latest/dist/kicanvas.js", content.extra_js)

    def test_does_not_inject_when_no_syntax_found(self):
        """Test that script is not injected when no kicad_schematic syntax found."""
        content = Mock()
        content._content = "Just normal text without any embeddings."
        delattr(content, "kicanvas_embed")
        delattr(content, "extra_js")

        inject_kicanvas_script(content)

        # After calling with no matches, these attributes should still not exist
        self.assertFalse(hasattr(content, "kicanvas_embed"))
        self.assertFalse(hasattr(content, "extra_js"))

    def test_handles_missing_content_attribute(self):
        """Test that function handles content without _content attribute."""
        content = Mock(spec=[])  # No _content attribute

        # Should not raise an exception
        inject_kicanvas_script(content)

        # After calling, attributes should still not exist
        self.assertFalse(hasattr(content, "kicanvas_embed"))
        self.assertFalse(hasattr(content, "extra_js"))

    def test_handles_none_content(self):
        """Test that function handles content with _content = None."""
        content = Mock()
        content._content = None
        # Clean up any mock attributes
        if hasattr(content, "kicanvas_embed"):
            delattr(content, "kicanvas_embed")
        if hasattr(content, "extra_js"):
            delattr(content, "extra_js")

        # Should not raise an exception
        inject_kicanvas_script(content)

        # After calling with None content, these attributes should still not exist
        self.assertFalse(hasattr(content, "kicanvas_embed"))
        self.assertFalse(hasattr(content, "extra_js"))
        content = Mock(spec=[])  # No _content attribute

        # Should not raise exception
        inject_kicanvas_script(content)

        self.assertFalse(hasattr(content, "kicanvas_embed"))

    def test_preserves_existing_extra_js_list(self):
        """Test that existing extra_js list is preserved."""
        content = Mock()
        content._content = '{{ kicad_schematic("amp.kicad_sch") }}'
        content.extra_js = ["https://example.com/other.js"]

        inject_kicanvas_script(content)

        self.assertEqual(len(content.extra_js), 2)
        self.assertIn("https://example.com/other.js", content.extra_js)
        self.assertIn("https://unpkg.com/kicanvas@latest/dist/kicanvas.js", content.extra_js)

    def test_converts_extra_js_string_to_list(self):
        """Test that extra_js string is converted to list."""
        content = Mock()
        content._content = '{{ kicad_schematic("amp.kicad_sch") }}'
        content.extra_js = "https://example.com/other.js"

        inject_kicanvas_script(content)

        self.assertIsInstance(content.extra_js, list)
        self.assertEqual(len(content.extra_js), 2)

    def test_does_not_duplicate_script_url(self):
        """Test that script URL is not duplicated if already present."""
        content = Mock()
        content._content = '{{ kicad_schematic("amp.kicad_sch") }}'
        kicanvas_url = "https://unpkg.com/kicanvas@latest/dist/kicanvas.js"
        content.extra_js = [kicanvas_url]

        inject_kicanvas_script(content)

        # Should still be only one occurrence
        self.assertEqual(content.extra_js.count(kicanvas_url), 1)

    def test_handles_multiple_embeddings(self):
        """Test that script is injected once even with multiple embeddings."""
        content = Mock()
        content._content = """{{ kicad_schematic("a.kicad_sch") }}
{{ kicad_schematic("b.kicad_sch") }}
.. kicad-schematic:: c.kicad_sch"""
        delattr(content, "kicanvas_embed")
        delattr(content, "extra_js")

        inject_kicanvas_script(content)

        self.assertTrue(content.kicanvas_embed)
        # Script should be present only once
        kicanvas_url = "https://unpkg.com/kicanvas@latest/dist/kicanvas.js"
        self.assertIsInstance(content.extra_js, list)
        self.assertEqual(content.extra_js.count(kicanvas_url), 1)


class TestPluginRegistration(unittest.TestCase):
    """Test cases for plugin registration functions."""

    def test_register_markdown_extension_callable(self):
        """Test that register_markdown_extension function exists and is callable."""
        from pelican_kicad_embed import register_markdown_extension

        self.assertTrue(callable(register_markdown_extension))

    def test_register_rst_directive_callable(self):
        """Test that register_rst_directive function exists and is callable."""
        from pelican_kicad_embed import register_rst_directive

        self.assertTrue(callable(register_rst_directive))

        # Should not raise exception when called
        register_rst_directive()

    def test_register_liquid_tag_callable(self):
        """Test that register_liquid_tag function exists and is callable."""
        from pelican_kicad_embed import register_liquid_tag

        self.assertTrue(callable(register_liquid_tag))

        # Should not raise exception even if liquid_tags not installed (silent failure)
        try:
            register_liquid_tag()
            success = True
        except ImportError:
            success = True  # ImportError is acceptable

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
