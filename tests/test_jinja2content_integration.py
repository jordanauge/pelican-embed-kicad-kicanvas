"""Integration tests with pelican-jinja2content plugin.

This module tests the signal timing to ensure kicad_schematic()
function is available when templates are processed.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock

from jinja2 import Environment

from pelican_kicad_embed import add_jinja2_globals, kicad_schematic


class TestJinja2ContentIntegration:
    """Test integration with pelican-jinja2content plugin."""

    def test_add_jinja2_globals_registers_function(self) -> None:
        """Test that add_jinja2_globals adds kicad_schematic to env.globals and settings."""
        env = Environment()
        mock_pelican = Mock()
        mock_pelican.env = env
        mock_pelican.settings = {}

        # Call our registration function
        add_jinja2_globals(mock_pelican)

        # Check function was added to env.globals
        assert "kicad_schematic" in env.globals
        assert env.globals["kicad_schematic"] == kicad_schematic

        # Check function was added to settings JINJA_GLOBALS
        assert "JINJA_GLOBALS" in mock_pelican.settings
        assert "kicad_schematic" in mock_pelican.settings["JINJA_GLOBALS"]
        assert mock_pelican.settings["JINJA_GLOBALS"]["kicad_schematic"] == kicad_schematic

    def test_function_works_in_jinja2_template(self) -> None:
        """Test that kicad_schematic() can be called from Jinja2 template."""
        env = Environment()
        env.globals["kicad_schematic"] = kicad_schematic

        # Render a template using the function
        template_str = '{{ kicad_schematic("test.kicad_sch") }}'
        result = env.from_string(template_str).render()

        # Check output
        assert "kicanvas-embed" in result
        assert 'src="test.kicad_sch"' in result

    def test_signal_connection_with_initialized(self) -> None:
        """Test that function is registered when initialized signal fires."""
        from pelican import signals

        env = Environment()
        mock_pelican = Mock()
        mock_pelican.env = env
        mock_pelican.settings = {}

        # Connect our function to initialized signal
        signals.initialized.connect(add_jinja2_globals)

        try:
            # Fire signal
            signals.initialized.send(mock_pelican)

            # Check function was registered in env.globals
            assert "kicad_schematic" in env.globals
            # Check function was registered in settings
            assert "kicad_schematic" in mock_pelican.settings["JINJA_GLOBALS"]
        finally:
            # Cleanup
            signals.initialized.disconnect(add_jinja2_globals)

    def test_signal_connection_with_get_generators(self) -> None:
        """Test that function is registered when get_generators signal fires."""
        from pelican import signals

        env = Environment()
        mock_pelican = Mock()
        mock_pelican.env = env
        mock_pelican.settings = {}

        # Connect our function to get_generators signal (same as register() does)
        def handler(sender: Any) -> None:
            add_jinja2_globals(sender)

        signals.get_generators.connect(handler)

        try:
            # Fire signal - sender is the first argument
            signals.get_generators.send(mock_pelican)

            # Check function was registered
            assert "kicad_schematic" in env.globals
            assert "kicad_schematic" in mock_pelican.settings["JINJA_GLOBALS"]
        finally:
            signals.get_generators.disconnect(handler)

    def test_both_signals_register_function(self) -> None:
        """Test that function works with both initialized and get_generators."""
        from pelican import signals

        env = Environment()
        mock_pelican = Mock()
        mock_pelican.env = env
        mock_pelican.settings = {}

        # Connect to both signals (like register() does)
        signals.initialized.connect(add_jinja2_globals)
        handler = lambda p: add_jinja2_globals(p)  # noqa: E731
        signals.get_generators.connect(handler)

        try:
            # Fire initialized first
            signals.initialized.send(mock_pelican)
            assert "kicad_schematic" in env.globals
            assert "kicad_schematic" in mock_pelican.settings["JINJA_GLOBALS"]

            # Reset to test get_generators independently
            del env.globals["kicad_schematic"]
            del mock_pelican.settings["JINJA_GLOBALS"]["kicad_schematic"]

            # Fire get_generators
            signals.get_generators.send(mock_pelican)
            assert "kicad_schematic" in env.globals
            assert "kicad_schematic" in mock_pelican.settings["JINJA_GLOBALS"]
        finally:
            signals.initialized.disconnect(add_jinja2_globals)
            # Can't disconnect lambda easily

    def test_readers_init_signal_for_jinja2content(self) -> None:
        """Test that readers_init signal is used to populate settings before jinja2content init.

        This is CRITICAL for pelican-jinja2content compatibility.
        The jinja2content plugin creates its own Environment in __init__ and reads
        from settings["JINJA_GLOBALS"]. We must populate this BEFORE readers are created.
        """
        from pelican import signals

        mock_pelican = Mock()
        mock_pelican.settings = {}
        # NOTE: env may not exist yet at readers_init time
        mock_pelican.env = None

        # Connect to readers_init (fires BEFORE readers are created)
        signals.readers_init.connect(add_jinja2_globals)

        try:
            # Fire readers_init signal
            signals.readers_init.send(mock_pelican)

            # Check that settings were populated (even if env doesn't exist yet)
            assert "JINJA_GLOBALS" in mock_pelican.settings
            assert "kicad_schematic" in mock_pelican.settings["JINJA_GLOBALS"]
            assert mock_pelican.settings["JINJA_GLOBALS"]["kicad_schematic"] == kicad_schematic
        finally:
            signals.readers_init.disconnect(add_jinja2_globals)
