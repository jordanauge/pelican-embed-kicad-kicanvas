"""Integration tests with a minimal Pelican site."""

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock


class TestPelicanIntegration(unittest.TestCase):
    """Integration tests with full Pelican site generation."""

    def setUp(self):
        """Set up a temporary Pelican test site."""
        self.test_dir = tempfile.mkdtemp()
        self.content_dir = Path(self.test_dir) / "content"
        self.output_dir = Path(self.test_dir) / "output"
        self.content_dir.mkdir()
        self.output_dir.mkdir()

    def tearDown(self):
        """Clean up temporary test site."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_markdown_article_with_kicad_embed(self):
        """Test Markdown article with kicad_schematic gets processed."""
        # Create a test article
        article_path = self.content_dir / "test_article.md"
        article_content = """Title: Test Article
Date: 2025-11-17
Category: Test

This is a test article with a KiCad schematic:

{{ kicad_schematic("amplifier.kicad_sch", style="width: 800px;", controls="full") }}

More text after the schematic.
"""
        article_path.write_text(article_content)

        # Mock Pelican processing
        from pelican_kicad_embed import inject_kicanvas_script
        from pelican_kicad_embed.md_ext import KiCadSchematicPreprocessor

        # Test preprocessor
        preprocessor = KiCadSchematicPreprocessor(None)
        lines = article_content.split("\n")
        processed = preprocessor.run(lines)

        # Verify HTML was generated
        processed_text = "\n".join(processed)
        self.assertIn("<kicanvas-embed", processed_text)
        self.assertIn('src="/static/schematics/amplifier.kicad_sch"', processed_text)
        self.assertIn('style="width: 800px;"', processed_text)
        self.assertIn('controls="full"', processed_text)

        # Test script injection
        content_obj = Mock()
        content_obj._content = article_content
        inject_kicanvas_script(content_obj)

        self.assertTrue(content_obj.kicanvas_embed)
        self.assertIn("https://unpkg.com/kicanvas@latest/dist/kicanvas.js", content_obj.extra_js)

    def test_rst_article_with_kicad_embed(self):
        """Test reStructuredText article with kicad-schematic directive."""
        article_path = self.content_dir / "test_article.rst"
        article_content = """Test Article
============

:date: 2025-11-17
:category: Test

This is a test article with a KiCad schematic:

.. kicad-schematic:: amplifier.kicad_sch
   :style: width: 800px; height: 600px;
   :controls: full

More text after the schematic.
"""
        article_path.write_text(article_content)

        # Test reST processing
        from docutils.core import publish_parts

        from pelican_kicad_embed.rst_directive import register_directive

        register_directive()
        parts = publish_parts(article_content, writer_name="html")
        html = parts.get("body", "")
        if not html:
            self.fail("RST parsing failed: no body returned")

        self.assertIn("<kicanvas-embed", html)
        self.assertIn('src="/static/schematics/amplifier.kicad_sch"', html)
        self.assertIn("style=", html)
        self.assertIn("controls=", html)

        # Test script injection
        from pelican_kicad_embed import inject_kicanvas_script

        content_obj = Mock()
        content_obj._content = article_content
        inject_kicanvas_script(content_obj)

        self.assertTrue(content_obj.kicanvas_embed)
        self.assertIn("https://unpkg.com/kicanvas@latest/dist/kicanvas.js", content_obj.extra_js)

    def test_article_without_kicad_embed(self):
        """Test that articles without kicad_schematic are not affected."""
        article_content = """Title: Normal Article
Date: 2025-11-17

This is a normal article without any KiCad schematics.
Just regular text about electronics and circuits.
"""

        from pelican_kicad_embed import inject_kicanvas_script

        content_obj = Mock()
        content_obj._content = article_content
        delattr(content_obj, "kicanvas_embed")
        delattr(content_obj, "extra_js")

        inject_kicanvas_script(content_obj)

        # Should not inject script
        self.assertFalse(hasattr(content_obj, "kicanvas_embed"))
        self.assertFalse(hasattr(content_obj, "extra_js"))

    def test_multiple_embeds_in_same_article(self):
        """Test article with multiple KiCad schematics."""
        article_content = """Title: Multi-Schematic Article
Date: 2025-11-17

First schematic:

{{ kicad_schematic("amp1.kicad_sch") }}

Second schematic:

{{ kicad_schematic("amp2.kicad_sch", style="width: 600px;") }}

Third schematic:

.. kicad-schematic:: amp3.kicad_sch
   :controls: minimal
"""

        from pelican_kicad_embed.md_ext import KiCadSchematicPreprocessor

        # Test Markdown processing
        preprocessor = KiCadSchematicPreprocessor(None)
        lines = article_content.split("\n")
        processed = preprocessor.run(lines)
        processed_text = "\n".join(processed)

        # All three should be present
        self.assertIn('src="/static/schematics/amp1.kicad_sch"', processed_text)
        self.assertIn('src="/static/schematics/amp2.kicad_sch"', processed_text)
        # amp3 won't be processed by Markdown preprocessor (it's reST)

        # Test script injection (should be added only once)
        from pelican_kicad_embed import inject_kicanvas_script

        content_obj = Mock()
        content_obj._content = article_content
        inject_kicanvas_script(content_obj)

        self.assertTrue(content_obj.kicanvas_embed)
        kicanvas_url = "https://unpkg.com/kicanvas@latest/dist/kicanvas.js"
        self.assertEqual(content_obj.extra_js.count(kicanvas_url), 1)

    def test_mixed_markdown_and_rst_in_article(self):
        """Test article with both Markdown and reST syntax (theoretical)."""
        # In practice, Pelican articles are either .md or .rst, but test detection
        article_content = """Title: Mixed Article
Date: 2025-11-17

Markdown style:
{{ kicad_schematic("amp1.kicad_sch") }}

reST style:
.. kicad-schematic:: amp2.kicad_sch

Liquid style:
{% kicad_schematic amp3.kicad_sch %}
"""

        from pelican_kicad_embed import KICAD_PATTERN

        # All three patterns should be detected
        matches = KICAD_PATTERN.findall(article_content)
        self.assertEqual(len(matches), 3)

        # Script should be injected
        from pelican_kicad_embed import inject_kicanvas_script

        content_obj = Mock()
        content_obj._content = article_content
        inject_kicanvas_script(content_obj)

        self.assertTrue(content_obj.kicanvas_embed)

    def test_script_injection_with_existing_extra_js(self):
        """Test that script injection preserves existing extra_js."""
        article_content = '{{ kicad_schematic("amp.kicad_sch") }}'

        from pelican_kicad_embed import inject_kicanvas_script

        # Test with list
        content_obj = Mock()
        content_obj._content = article_content
        content_obj.extra_js = ["https://example.com/script1.js", "https://example.com/script2.js"]
        inject_kicanvas_script(content_obj)

        self.assertEqual(len(content_obj.extra_js), 3)
        self.assertIn("https://example.com/script1.js", content_obj.extra_js)
        self.assertIn("https://example.com/script2.js", content_obj.extra_js)
        self.assertIn("https://unpkg.com/kicanvas@latest/dist/kicanvas.js", content_obj.extra_js)

    def test_script_not_duplicated_on_multiple_calls(self):
        """Test that calling inject_kicanvas_script multiple times doesn't duplicate script."""
        article_content = '{{ kicad_schematic("amp.kicad_sch") }}'

        from pelican_kicad_embed import inject_kicanvas_script

        content_obj = Mock()
        content_obj._content = article_content

        # Call multiple times
        inject_kicanvas_script(content_obj)
        inject_kicanvas_script(content_obj)
        inject_kicanvas_script(content_obj)

        # Script should only appear once
        kicanvas_url = "https://unpkg.com/kicanvas@latest/dist/kicanvas.js"
        self.assertEqual(content_obj.extra_js.count(kicanvas_url), 1)


class TestPluginRegistration(unittest.TestCase):
    """Test plugin registration with Pelican."""

    def test_register_function_exists(self):
        """Test that register() function exists and is callable."""
        from pelican_kicad_embed import register

        self.assertTrue(callable(register))

    def test_all_exports(self):
        """Test that __all__ exports are defined."""
        from pelican_kicad_embed import __all__

        self.assertIn("register", __all__)
        self.assertIn("__version__", __all__)

    def test_version_defined(self):
        """Test that version is defined."""
        from pelican_kicad_embed import __version__

        self.assertIsInstance(__version__, str)
        self.assertRegex(__version__, r"\d+\.\d+\.\d+")


if __name__ == "__main__":
    unittest.main()
