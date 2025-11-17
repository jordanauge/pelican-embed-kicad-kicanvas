"""Integration tests for Jinja2 compatibility.

Tests the kicad_schematic function when used within Jinja2 templates,
specifically for compatibility with pelican-jinja2content plugin.
"""

import unittest
from unittest.mock import Mock

from jinja2 import Environment


class TestJinja2Integration(unittest.TestCase):
    """Test Jinja2 template integration."""

    def setUp(self):
        """Set up test fixtures."""
        # Import the function
        from pelican_kicad_embed import kicad_schematic

        # Create a Jinja2 environment
        self.env = Environment()

        # Register the function as a global (as the plugin does)
        self.env.globals["kicad_schematic"] = kicad_schematic

    def test_function_available_in_template(self):
        """Test that kicad_schematic is accessible in Jinja2 templates."""
        template = self.env.from_string("{{ kicad_schematic }}")
        result = template.render()
        self.assertIn("function", result.lower())

    def test_basic_call_in_template(self):
        """Test basic function call from Jinja2 template."""
        template = self.env.from_string('{{ kicad_schematic("test.kicad_sch") }}')
        result = template.render()

        self.assertIn("<kicanvas-embed", result)
        self.assertIn('src="test.kicad_sch"', result)
        self.assertIn('controls="all"', result)
        self.assertIn('style="width: 100%; height: 600px;"', result)

    def test_with_parameters_in_template(self):
        """Test function call with parameters from Jinja2 template."""
        template = self.env.from_string(
            '{{ kicad_schematic("amp.kicad_sch", style="width: 800px;", controls="zoom") }}'
        )
        result = template.render()

        self.assertIn('src="amp.kicad_sch"', result)
        self.assertIn('style="width: 800px;"', result)
        self.assertIn('controls="zoom"', result)

    def test_multiple_calls_in_template(self):
        """Test multiple function calls in same template."""
        template_str = """
        {{ kicad_schematic("amp1.kicad_sch") }}
        Some text in between
        {{ kicad_schematic("amp2.kicad_sch", style="width: 500px;") }}
        """
        template = self.env.from_string(template_str)
        result = template.render()

        self.assertIn('src="amp1.kicad_sch"', result)
        self.assertIn('src="amp2.kicad_sch"', result)
        self.assertIn("width: 500px;", result)

    def test_with_jinja2_variables(self):
        """Test function call with Jinja2 variables."""
        template = self.env.from_string("{{ kicad_schematic(filename, style=custom_style) }}")
        result = template.render(
            filename="variable.kicad_sch", custom_style="width: 1000px; height: 800px;"
        )

        self.assertIn('src="variable.kicad_sch"', result)
        self.assertIn("width: 1000px; height: 800px;", result)

    def test_in_jinja2_loop(self):
        """Test function call within Jinja2 for loop."""
        template_str = """
        {% for schematic in schematics %}
        {{ kicad_schematic(schematic) }}
        {% endfor %}
        """
        template = self.env.from_string(template_str)
        result = template.render(schematics=["amp1.kicad_sch", "amp2.kicad_sch", "amp3.kicad_sch"])

        self.assertIn('src="amp1.kicad_sch"', result)
        self.assertIn('src="amp2.kicad_sch"', result)
        self.assertIn('src="amp3.kicad_sch"', result)
        self.assertEqual(result.count("<kicanvas-embed"), 3)

    def test_with_jinja2_conditionals(self):
        """Test function call within Jinja2 conditionals."""
        template_str = """
        {% if show_schematic %}
        {{ kicad_schematic(filename) }}
        {% endif %}
        """
        template = self.env.from_string(template_str)

        # Test with condition True
        result = template.render(show_schematic=True, filename="test.kicad_sch")
        self.assertIn("<kicanvas-embed", result)

        # Test with condition False
        result = template.render(show_schematic=False, filename="test.kicad_sch")
        self.assertNotIn("<kicanvas-embed", result)

    def test_with_default_parameters(self):
        """Test that default parameters work in Jinja2."""
        template = self.env.from_string('{{ kicad_schematic("test.kicad_sch", "", "") }}')
        result = template.render()

        # Empty strings should trigger defaults
        self.assertIn('style="width: 100%; height: 600px;"', result)
        self.assertIn('controls="all"', result)

    def test_html_escaping(self):
        """Test that HTML in output is not escaped by Jinja2."""
        template = self.env.from_string('{{ kicad_schematic("test.kicad_sch") }}')
        result = template.render()

        # Should contain actual HTML tags, not escaped
        self.assertIn("<kicanvas-embed", result)
        self.assertNotIn("&lt;kicanvas-embed", result)


class TestPelicanJinja2ContentSimulation(unittest.TestCase):
    """Simulate how pelican-jinja2content would use the function."""

    def test_simulated_article_processing(self):
        """Simulate processing an article with pelican-jinja2content."""
        from pelican_kicad_embed import kicad_schematic

        # Simulate article content
        article_content = """
        # My Electronics Project

        Here's the amplifier schematic:
        {{ kicad_schematic("amplifier.kicad_sch", style="width: 800px; height: 600px;", controls="full") }}

        And the power supply:
        {{ kicad_schematic("power_supply.kicad_sch") }}
        """

        # Create Jinja2 environment (as pelican-jinja2content does)
        env = Environment()
        env.globals["kicad_schematic"] = kicad_schematic

        # Render the template
        template = env.from_string(article_content)
        rendered = template.render()

        # Verify both schematics are rendered
        self.assertIn('src="amplifier.kicad_sch"', rendered)
        self.assertIn('src="power_supply.kicad_sch"', rendered)
        self.assertIn("width: 800px; height: 600px;", rendered)
        self.assertIn('controls="full"', rendered)
        self.assertEqual(rendered.count("<kicanvas-embed"), 2)

    def test_with_pelican_like_metadata(self):
        """Test with metadata variables like Pelican would provide."""
        from pelican_kicad_embed import kicad_schematic

        article_content = """
        Title: {{ title }}
        Date: {{ date }}

        {{ kicad_schematic(schematic_path) }}
        """

        env = Environment()
        env.globals["kicad_schematic"] = kicad_schematic

        template = env.from_string(article_content)
        rendered = template.render(
            title="My Project", date="2025-11-17", schematic_path="project.kicad_sch"
        )

        self.assertIn("Title: My Project", rendered)
        self.assertIn("Date: 2025-11-17", rendered)
        self.assertIn('src="project.kicad_sch"', rendered)


class TestPluginRegistration(unittest.TestCase):
    """Test that the plugin properly registers the Jinja2 global."""

    def test_add_jinja2_globals_function(self):
        """Test the add_jinja2_globals function."""
        from pelican_kicad_embed import add_jinja2_globals, kicad_schematic

        # Create a mock Pelican object
        mock_pelican = Mock()
        mock_pelican.env = Mock()
        mock_pelican.env.globals = {}
        mock_pelican.settings = {}

        # Call the registration function
        add_jinja2_globals(mock_pelican)

        # Verify the function was registered in env
        self.assertIn("kicad_schematic", mock_pelican.env.globals)
        self.assertEqual(mock_pelican.env.globals["kicad_schematic"], kicad_schematic)
        # Verify the function was registered in settings
        self.assertIn("JINJA_GLOBALS", mock_pelican.settings)
        self.assertIn("kicad_schematic", mock_pelican.settings["JINJA_GLOBALS"])

    def test_add_jinja2_globals_with_none_env(self):
        """Test add_jinja2_globals handles None env gracefully."""
        from pelican_kicad_embed import add_jinja2_globals

        # Create a mock Pelican object with None env
        mock_pelican = Mock()
        mock_pelican.env = None
        mock_pelican.settings = {}

        # Should not raise an exception
        add_jinja2_globals(mock_pelican)

        # Should still populate settings
        self.assertIn("JINJA_GLOBALS", mock_pelican.settings)
        self.assertIn("kicad_schematic", mock_pelican.settings["JINJA_GLOBALS"])

    def test_add_jinja2_globals_without_env_attribute(self):
        """Test add_jinja2_globals handles missing env attribute gracefully."""
        from pelican_kicad_embed import add_jinja2_globals

        # Create a mock Pelican object without env attribute
        mock_pelican = Mock(spec=[])

        # Should not raise an exception
        add_jinja2_globals(mock_pelican)

    def test_register_function_calls_add_jinja2_globals(self):
        """Test that register() connects add_jinja2_globals to the signal."""
        from unittest.mock import patch

        from pelican import signals

        from pelican_kicad_embed import register

        # Mock the signal.connect method
        with patch.object(signals.initialized, "connect") as mock_connect:
            register()

            # Check that add_jinja2_globals was connected
            calls = [call[0][0].__name__ for call in mock_connect.call_args_list]
            self.assertIn("add_jinja2_globals", calls)


if __name__ == "__main__":
    unittest.main()
