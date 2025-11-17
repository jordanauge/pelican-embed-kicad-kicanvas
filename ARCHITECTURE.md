# Architecture

This document explains the internal architecture of the `pelican-embed-kicad-kicanvas` plugin.

## Overview

The plugin consists of four main components:

```
pelican_kicad_embed/
├── __init__.py          # Main registration & signal handling
├── md_ext.py            # Markdown extension (preprocessor)
├── rst_directive.py     # reStructuredText directive
└── liquid_tag.py        # Liquid Tag handler (optional)
```

## Component Responsibilities

### 1. Main Module (`__init__.py`)

**Purpose**: Plugin initialization, registration, and automatic script injection.

**Key Functions**:
- `register()`: Main entry point called by Pelican during plugin loading
- `register_markdown_extension()`: Registers Markdown preprocessor with Pelican's Markdown instance
- `register_rst_directive()`: Registers reST directive with docutils
- `register_liquid_tag()`: Conditionally imports Liquid Tag handler (fails silently if unavailable)
- `inject_kicanvas_script()`: Signal handler that detects schematic embeds and injects JavaScript

**Pelican Signals Used**:
- `signals.initialized`: Triggered when Pelican initializes (for Markdown extension registration)
- `signals.content_object_init`: Triggered for each content object (article/page) to inject scripts

**Conditional Import Logic**:
```python
try:
    from . import liquid_tag  # Imports only if liquid_tags is installed
except ImportError:
    pass  # Silently skip if not available
```

### 2. Markdown Extension (`md_ext.py`)

**Purpose**: Parse `{{ kicad_schematic(...) }}` syntax in Markdown files.

**Implementation**:
- Extends `markdown.preprocessors.Preprocessor`
- Uses regex pattern matching to find syntax in document lines
- Runs before Markdown parsing (as preprocessor, not inline processor)
- Priority: 175 (runs early in preprocessing chain)

**Regex Pattern**:
```python
r'\{\{\s*kicad_schematic\s*\(\s*'
r'["\']?(?P<filename>[^"\')\s]+)["\']?\s*'
r'(?:,\s*style\s*=\s*["\'](?P<style>[^"\']+)["\'])?'
r'(?:,\s*controls\s*=\s*["\'](?P<controls>[^"\']+)["\'])?'
r'\s*\)\s*\}\}'
```

**Processing Flow**:
1. Preprocessor scans each line of Markdown source
2. Regex matches `{{ kicad_schematic(...) }}` patterns
3. Extracts filename, style, and controls parameters
4. Replaces matched text with `<kicanvas-embed>` HTML
5. Returns modified lines to Markdown parser

### 3. reStructuredText Directive (`rst_directive.py`)

**Purpose**: Parse `.. kicad-schematic::` directive in reST files.

**Implementation**:
- Extends `docutils.parsers.rst.Directive`
- Uses docutils' native argument/option parsing
- Returns `nodes.raw()` HTML node

**Directive Specification**:
```python
required_arguments = 1          # filename
optional_arguments = 0
has_content = False             # No body content allowed
option_spec = {
    'style': directives.unchanged,
    'controls': directives.unchanged,
}
```

**Processing Flow**:
1. docutils parses directive during reST processing
2. `run()` method extracts arguments and options
3. Builds `<kicanvas-embed>` HTML string
4. Wraps in `nodes.raw()` for HTML passthrough
5. Returns node list to docutils

### 4. Liquid Tag Handler (`liquid_tag.py`)

**Purpose**: Parse `{% kicad_schematic ... %}` syntax (optional).

**Implementation**:
- Requires `liquid_tags` plugin installed
- Registers with `@LiquidTags.register()` decorator
- Uses regex to parse tag arguments

**Processing Flow**:
1. `liquid_tags` detects `{% kicad_schematic ... %}` syntax
2. Calls registered handler function
3. Regex extracts filename, style, controls from markup
4. Returns `<kicanvas-embed>` HTML string
5. `liquid_tags` inserts HTML into document

## HTML Output

All three syntax handlers generate identical HTML:

```html
<kicanvas-embed 
    src="/static/schematics/filename.kicad_sch" 
    controls="full" 
    style="width: 800px; height: 500px;">
</kicanvas-embed>
```

## Automatic Script Injection

**Problem**: The `<kicanvas-embed>` custom element requires the KiCanvas JavaScript library.

**Solution**: Signal-based detection and metadata injection.

**Flow**:
1. Pelican processes each content file (article/page)
2. `signals.content_object_init` fires for each object
3. `inject_kicanvas_script()` checks raw content (`_content`) for any syntax variant
4. If found, adds KiCanvas URL to `content.extra_js` list
5. Pelican theme template includes scripts from `extra_js` metadata

**Detection Pattern**:
```python
KICAD_PATTERN = re.compile(
    r'(\{\{\s*kicad_schematic\s*\(|'      # Markdown
    r'\.\.\s+kicad-schematic::|'          # reST
    r'\{%\s*kicad_schematic\s+)',         # Liquid
    re.IGNORECASE | re.MULTILINE
)
```

**Note**: This approach assumes the theme uses `extra_js` metadata. If not, users must manually add the script to their theme template.

## Design Decisions

### Why Three Syntax Options?

- **Markdown**: Most common Pelican format, function-call syntax is intuitive
- **reStructuredText**: Used for technical documentation, directive syntax is idiomatic
- **Liquid Tag**: Compatibility with existing `liquid_tags` users

### Why Preprocessor vs Inline Processor (Markdown)?

- **Preprocessor**: Runs before Markdown parsing, simple regex replacement
- **Inline Processor**: Would require pattern integration with Markdown's parsing tree
- **Trade-off**: Preprocessor is simpler but less context-aware

### Why Conditional Import for Liquid Tags?

- Avoids hard dependency on `liquid_tags` plugin
- Users without Liquid Tags don't need it installed
- Markdown and reST work independently

### Why Signal-Based Script Injection?

- Automatic: No manual `<script>` tag insertion required
- Per-content: Only loads KiCanvas on pages that need it
- Theme-agnostic: Works with any theme using `extra_js` metadata pattern

## Extension Points

Future enhancements could include:

1. **Custom KiCanvas Options**: Support for theme, layer visibility, initial zoom
2. **Multiple CDN Sources**: Fallback URLs or local hosting option
3. **Caching**: Pre-render or cache schematic thumbnails
4. **Validation**: Check if `.kicad_sch` files exist during build
5. **Gallery Mode**: Auto-generate schematic galleries from directories

## Testing Strategy

Recommended test coverage:

1. **Unit Tests**:
   - Regex pattern matching (all three syntaxes)
   - HTML output generation
   - Parameter parsing (style, controls)

2. **Integration Tests**:
   - Pelican build with sample content
   - Verify HTML output in generated pages
   - Check script injection in HTML head

3. **End-to-End Tests**:
   - Browser-based tests with Selenium
   - Verify KiCanvas loads and renders
   - Test interactive controls (pan, zoom)

## Dependencies

```
Required:
- pelican (≥4.5)      # Core framework
- markdown (≥3.2)     # Markdown processing
- docutils (≥0.16)    # reStructuredText processing

Optional:
- pelican-liquid-tags (≥1.0.0)  # Liquid Tag syntax

Runtime (CDN):
- kicanvas (latest)   # Interactive viewer
```

## Performance Considerations

- **Build Time**: Minimal impact (simple regex/parsing, no rendering)
- **Page Load**: ~100KB JavaScript from CDN (first load, then cached)
- **Runtime**: Depends on schematic complexity and browser

## Security Considerations

- **XSS Prevention**: All parameters are HTML-escaped/quoted
- **Path Traversal**: Filename restricted to static directory via Pelican's `STATIC_PATHS`
- **CDN Trust**: Requires trust in unpkg.com CDN (users can self-host if preferred)
