"""Pelican plugin for embedding KiCad schematics using KiCanvas.

This plugin enables three syntax options for embedding interactive KiCad schematics:
1. Markdown Extension: {{ kicad_schematic(filename, style="...", controls="...") }}
2. reStructuredText Directive: .. kicad-schematic:: filename
3. Liquid Tag (optional): {% kicad_schematic filename style="..." controls="..." %}

The plugin automatically loads the KiCanvas JavaScript library when needed.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from jinja2 import pass_context
from pelican import signals

if TYPE_CHECKING:
    from pelican import Pelican
    from pelican.contents import Content

from .__about__ import __author__, __license__, __version__

__all__ = ["register", "kicad_schematic", "__version__", "__author__", "__license__"]

# Global reference to Pelican settings (populated during initialization)
_pelican_settings = None

# Flag to track if we've already injected the KiCanvas script
_kicanvas_loaded = False

# Regex pattern to detect any kicad_schematic usage in content
KICAD_PATTERN = re.compile(
    r"(\{\{\s*kicad_schematic\s*\(|"
    r"\.\.\s+kicad-schematic::|"
    r"\{%\s*kicad_schematic\s+)",
    re.IGNORECASE | re.MULTILINE,
)


def resolve_schematic_path(
    filename: str,
    content_source_path: str | None = None,
    article_url: str | None = None,
) -> str:
    """Resolve the path to a KiCad schematic file.

    Search order:
    1. If filename is absolute URL (starts with / or http), use it as-is
    2. Relative to the article's output URL directory (preferred for articles)
    3. Relative to the content source file (article .md directory, fallback)
    4. Relative to KICAD_SCHEMATICS_PATH (if configured)

    Args:
        filename: Requested schematic filename (can be relative or absolute)
        content_source_path: Absolute path to the content source file (.md)
        article_url: Article's output URL (e.g., 'blog/2025/11/kicad-sample/')

    Returns:
        URL path from site root (e.g., /blog/2025/11/kicad-sample/file.kicad_sch).
    """
    global _pelican_settings

    # If absolute URL, use as-is
    if filename.startswith("/") or filename.startswith("http"):
        return filename

    # Get Pelican settings
    settings = _pelican_settings or {}
    content_path = settings.get("PATH", "content")
    output_path = settings.get("OUTPUT_PATH", "output")

    # Strategy 1: Use article URL to construct output path (for articles)
    if article_url and content_source_path:
        # Remove trailing slash and convert to path
        url_path = article_url.rstrip("/")
        # Build expected output location: output/{article_url}/{filename}
        expected_output = Path(output_path) / url_path / filename

        if expected_output.exists():
            # Return as absolute URL from site root
            return f"/{url_path}/{filename}"

        # Also check if schematic is in source directory
        # (Pelican may copy it preserving source structure)
        source_dir = Path(content_source_path).parent
        schematic_source = source_dir / filename

        if schematic_source.exists():
            # File exists in source, will be copied to output
            # Use article URL as base
            return f"/{url_path}/{filename}"

    # Strategy 2: Try to resolve relative to content source file
    if content_source_path:
        source_dir = Path(content_source_path).parent
        schematic_path = source_dir / filename

        if schematic_path.exists():
            # Calculate relative path from content root to schematic
            try:
                content_root = Path(content_path).resolve()
                rel_path = schematic_path.resolve().relative_to(content_root)
                # Return as absolute URL from site root
                # Pelican copies files preserving directory structure
                return "/" + str(rel_path).replace("\\", "/")
            except ValueError:
                # If not under content root, cannot resolve
                pass

    # Strategy 3: Try KICAD_SCHEMATICS_PATH if configured
    kicad_path = settings.get("KICAD_SCHEMATICS_PATH")
    if kicad_path:
        schematic_path = Path(content_path) / kicad_path / filename
        if schematic_path.exists():
            return f"/{kicad_path}/{filename}"

    # Fallback: return as relative path (may not work in all contexts)
    return filename


def inject_kicanvas_script(content: Any) -> None:
    """Check if content uses kicad_schematic and inject KiCanvas script if needed.

    This function is called for each content object (article/page) and checks
    if it contains any of the three kicad_schematic syntax variants. If found,
    it directly injects the KiCanvas JavaScript into the HTML content, making
    the plugin self-contained and independent of theme support.

    Args:
        content: Pelican content object (article or page).
    """
    # Check if content has the _content attribute (raw source) and it's not None
    if not hasattr(content, "_content") or content._content is None:
        return

    # Check if any kicad_schematic syntax is present
    if KICAD_PATTERN.search(content._content):
        # Mark content as having kicanvas embed
        content.kicanvas_embed = True


def inject_kicanvas_script_into_html(content: Any) -> None:
    """Inject the KiCanvas script directly into rendered HTML content.

    This is called after content rendering to inject the <script> tag directly
    into the HTML, making the plugin theme-independent.

    Args:
        content: Pelican content object with rendered HTML.
    """
    if not getattr(content, "kicanvas_embed", False):
        return

    if content.status != "published":
        return

    # Only inject once
    if hasattr(content, "_kicanvas_script_injected"):
        return
    content._kicanvas_script_injected = True

    # Check if content has rendered HTML
    if not hasattr(content, "_content") or not content._content:
        return

    # Use local version by default, fallback to CDN if configured
    global _pelican_settings
    settings = _pelican_settings or {}

    use_cdn = settings.get("KICANVAS_USE_CDN", False)

    if use_cdn:
        kicanvas_url = "https://kicanvas.org/kicanvas/kicanvas.js"
    else:
        kicanvas_url = "/static/js/kicanvas.js"

    # Create script tag
    script_tag = f'<script type="module" src="{kicanvas_url}"></script>\n'

    html = content._content

    # Check if script is already injected (avoid duplicates)
    if kicanvas_url in html:
        return

    # Try to inject before </head>
    if "</head>" in html:
        content._content = html.replace("</head>", f"{script_tag}</head>", 1)
    # Otherwise inject at start of <body>
    elif "<body" in html:
        body_pos = html.find(">", html.find("<body")) + 1
        content._content = html[:body_pos] + "\n" + script_tag + html[body_pos:]
    # Last resort: prepend to content
    else:
        content._content = script_tag + html


def register_markdown_extension(pelican_object: Any) -> None:
    """Register the Markdown extension with Pelican's Markdown processor.

    Args:
        pelican_object: Pelican instance.
    """
    from .md_ext import KiCadSchematicExtension

    # Get Pelican's Markdown extensions configuration
    md_extensions = pelican_object.settings.get("MARKDOWN", {})

    if "extensions" not in md_extensions:
        md_extensions["extensions"] = []
    elif not isinstance(md_extensions["extensions"], list):
        md_extensions["extensions"] = [md_extensions["extensions"]]

    # Add our extension if not already present
    ext_instance = KiCadSchematicExtension()
    if ext_instance not in md_extensions["extensions"]:
        md_extensions["extensions"].append(ext_instance)

    pelican_object.settings["MARKDOWN"] = md_extensions


def register_rst_directive() -> None:
    """Register the reStructuredText directive.

    This always succeeds as docutils is a core Pelican dependency.
    """
    from .rst_directive import register_directive

    register_directive()


def register_liquid_tag() -> None:
    """Attempt to register the Liquid Tag handler (optional).

    This function tries to import and register the Liquid Tag handler.
    If liquid_tags is not installed, it silently fails.
    """
    try:
        from . import liquid_tag  # Will be created if liquid_tags available
        # If import succeeds, the tag is registered automatically
    except ImportError:
        # liquid_tags plugin not installed - skip silently
        pass


@pass_context
def kicad_schematic(context: dict, filename: str, style: str = "", controls: str = "") -> str:
    """Generate KiCanvas embed HTML for use in Jinja2 templates.

    This function can be called from Jinja2 templates (e.g., when using
    pelican-jinja2content plugin) to embed KiCad schematics.

    The function automatically resolves schematic paths in this order:
    1. If filename is absolute, use it as-is
    2. Relative to the current article's directory (same folder as .md file)
    3. Relative to KICAD_SCHEMATICS_PATH (if configured in pelicanconf.py)
    4. Fallback to filename as-is

    Args:
        context: Jinja2 context (automatically passed by @pass_context decorator)
        filename: Path to the KiCad schematic file (.kicad_sch)
        style: CSS style attributes (default: 'width: 100%; height: 600px;')
        controls: Control buttons to show (default: 'all')

    Returns:
        HTML string with kicanvas-embed element.

    Example:
        {{ kicad_schematic('MOSFET.kicad_sch', style='width: 800px; height: 500px;') }}
    """
    # Set defaults
    if not style:
        style = "width: 100%; height: 600px;"
    if not controls:
        controls = "all"

    # Try to get source path and article URL from Jinja2 context
    content_source_path = None
    article_url = None

    # Priority 1: __source_path__ and __article_url__ (injected by our jinja2content patch)
    if "__source_path__" in context:
        content_source_path = context["__source_path__"]
    if "__article_url__" in context:
        article_url = context["__article_url__"]

    # Priority 2: article context (when called from article template)
    if "article" in context:
        article = context["article"]
        if hasattr(article, "source_path") and not content_source_path:
            content_source_path = article.source_path
        # Get article URL (without leading /)
        if hasattr(article, "url") and not article_url:
            article_url = article.url

    # Priority 3: page.source_path (when called from page template)
    elif "page" in context and hasattr(context["page"], "source_path"):
        page = context["page"]
        if not content_source_path:
            content_source_path = page.source_path
        # Get page URL
        if hasattr(page, "url") and not article_url:
            article_url = page.url

    # Resolve the schematic path
    resolved_path = resolve_schematic_path(filename, content_source_path, article_url)

    # Generate HTML
    return f'<kicanvas-embed src="{resolved_path}" controls="{controls}" style="{style}"></kicanvas-embed>'


def add_jinja2_globals(pelican_object: Any) -> None:
    """Add kicad_schematic function to Jinja2 global context.

    This makes kicad_schematic available in all Jinja2 templates,
    including when pelican-jinja2content processes article content.

    Args:
        pelican_object: Pelican instance or Readers instance.
    """
    global _pelican_settings

    # Store settings globally for path resolution
    if hasattr(pelican_object, "settings"):
        _pelican_settings = pelican_object.settings

    # Add to Pelican's main env (for direct templates)
    if hasattr(pelican_object, "env") and pelican_object.env is not None:
        pelican_object.env.globals["kicad_schematic"] = kicad_schematic

    # Add to settings JINJA_GLOBALS (for pelican-jinja2content plugin)
    # This is CRITICAL because jinja2content creates its own Environment
    # and only reads from settings["JINJA_GLOBALS"] during __init__
    if hasattr(pelican_object, "settings"):
        if "JINJA_GLOBALS" not in pelican_object.settings:
            pelican_object.settings["JINJA_GLOBALS"] = {}
        pelican_object.settings["JINJA_GLOBALS"]["kicad_schematic"] = kicad_schematic


def patch_jinja2content_reader(readers: Any) -> None:
    """Monkey-patch pelican-jinja2content to inject source_path into render context.

    This is necessary because jinja2content calls render() without any context,
    making it impossible to access article.source_path during template processing.

    Args:
        readers: Pelican Readers instance.
    """
    try:
        from pelican.plugins.jinja2content.jinja2content import JinjaContentMixin
    except ImportError:
        # jinja2content not installed, skip
        return

    def patched_read(self, source_path: str) -> tuple[str, dict]:
        """Patched read method that injects source_path and article URL into Jinja2 context."""
        from tempfile import NamedTemporaryFile

        from pelican.utils import pelican_open

        # First, read the file to extract metadata
        for base in self.__class__.__bases__:
            if base is not JinjaContentMixin and hasattr(base, "read"):
                _, metadata = base.read(self, source_path)
                break

        # Calculate article URL from metadata
        article_url = None
        if metadata:
            try:
                from datetime import datetime

                global _pelican_settings
                settings = _pelican_settings or {}
                article_url_pattern = settings.get("ARTICLE_URL", "blog/{slug}/")

                # Get date and slug from metadata
                date_str = metadata.get("date")
                slug = metadata.get("slug")

                if date_str and slug:
                    # Parse date
                    if isinstance(date_str, str):
                        date = datetime.fromisoformat(date_str)
                    else:
                        date = date_str

                    # Format URL
                    article_url = article_url_pattern.format(
                        slug=slug,
                        date=date,
                        year=date.year,
                        month=f"{date.month:02d}",
                        day=f"{date.day:02d}",
                    )
            except Exception:
                # If anything fails, continue without article URL
                pass

        # Now render with context
        with pelican_open(source_path) as text:
            # Inject source_path and article_url into the Jinja2 rendering context
            context = {
                "__source_path__": source_path,
                "__article_url__": article_url,
            }
            text = self.env.from_string(text).render(**context)

        with NamedTemporaryFile(delete=False) as f:
            f.write(text.encode())
            f.close()
            # Call the original parent class's read method
            # We need to get the proper parent (MarkdownReader, RstReader, etc.)
            for base in self.__class__.__bases__:
                if base is not JinjaContentMixin and hasattr(base, "read"):
                    content, metadata = base.read(self, f.name)
                    break
            os.unlink(f.name)
            return content, metadata

    # Apply the patch
    JinjaContentMixin.read = patched_read


def register() -> None:
    """Main plugin registration function.

    This function is called by Pelican during plugin initialization.
    It registers all three syntax handlers (conditionally for Liquid Tag)
    and sets up the signal listener for automatic KiCanvas script injection.
    """
    # Always register Markdown and reST (core dependencies)
    signals.initialized.connect(register_markdown_extension)
    register_rst_directive()

    # Conditionally register Liquid Tag (only if available)
    register_liquid_tag()

    # Add kicad_schematic to Jinja2 globals VERY EARLY
    # CRITICAL: Must use readers_init signal which fires BEFORE readers are created
    # This ensures settings["JINJA_GLOBALS"] is populated before pelican-jinja2content
    # creates its own Environment in JinjaContentMixin.__init__
    signals.readers_init.connect(add_jinja2_globals)

    # Patch jinja2content to inject source_path into context
    signals.readers_init.connect(patch_jinja2content_reader)

    # Also connect to initialized for main Pelican env (direct templates)
    signals.initialized.connect(add_jinja2_globals)

    # Register signal listener to detect KiCanvas usage when content is initialized
    signals.content_object_init.connect(inject_kicanvas_script)

    # Inject script into HTML after content is fully rendered (before writing)
    from pelican import signals as pelican_signals

    def inject_scripts_before_write(generator):
        """Inject scripts into all articles before they're written."""
        for article in generator.articles:
            inject_kicanvas_script_into_html(article)
        for draft in generator.drafts:
            inject_kicanvas_script_into_html(draft)

    pelican_signals.article_generator_finalized.connect(inject_scripts_before_write)

    # Copy .kicad_sch files from source to article output directory
    signals.article_writer_finalized.connect(copy_kicad_schematics)


def copy_kicad_schematics(article_generator: Any, writer: Any) -> None:
    """Copy .kicad_sch files from article source dir to output dir.

    This ensures schematic files are accessible at the same URL path as the article.

    Args:
        article_generator: ArticlesGenerator instance
        writer: Writer instance
    """
    import shutil

    settings = article_generator.settings
    output_path = settings.get("OUTPUT_PATH", "output")

    for article in article_generator.articles + article_generator.drafts:
        if not hasattr(article, "source_path") or not hasattr(article, "save_as"):
            continue

        # Get source directory (where .md file is)
        source_dir = Path(article.source_path).parent

        # Get output directory (where index.html will be)
        article_output_dir = Path(output_path) / Path(article.save_as).parent

        # Find all .kicad_sch files in source directory
        for schematic in source_dir.glob("*.kicad_sch"):
            dest = article_output_dir / schematic.name

            # Create output directory if needed
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Copy schematic file
            shutil.copy2(schematic, dest)
