"""reStructuredText directive for embedding KiCad schematics with KiCanvas.

This directive processes .. kicad-schematic:: syntax in reST files
and converts it to <kicanvas-embed> HTML elements.
"""

from docutils import nodes
from docutils.parsers.rst import Directive, directives


class KiCadSchematicDirective(Directive):
    """Directive to embed KiCad schematics using KiCanvas.

    Usage:
        .. kicad-schematic:: filename.kicad_sch
           :style: width: 800px; height: 500px;
           :controls: full

    The directive generates a <kicanvas-embed> HTML element.
    """

    required_arguments = 1  # filename is required
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False

    option_spec = {
        "style": directives.unchanged,
        "controls": directives.unchanged,
    }

    def run(self):
        """Generate the HTML node for the KiCad schematic.

        Returns:
            List containing a single raw HTML node.
        """
        filename = self.arguments[0]
        style = self.options.get("style", "")
        controls = self.options.get("controls", "")

        # Build the HTML attributes
        attrs = [f'src="/static/schematics/{filename}"']

        if controls:
            attrs.append(f'controls="{controls}"')

        if style:
            attrs.append(f'style="{style}"')

        # Create the HTML element
        html = f"<kicanvas-embed {' '.join(attrs)}></kicanvas-embed>"

        # Return as a raw HTML node
        raw_node = nodes.raw("", html, format="html")
        return [raw_node]


def register_directive():
    """Register the directive with docutils.

    This function should be called during plugin initialization.
    """
    directives.register_directive("kicad-schematic", KiCadSchematicDirective)
