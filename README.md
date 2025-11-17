# pelican-embed-kicad-kicanvas

A Pelican plugin for embedding interactive KiCad schematics using the [KiCanvas](https://github.com/theacodes/kicanvas) JavaScript library. This plugin supports three different syntax options to maximize compatibility with your existing Pelican workflow.

## Features

- 🎨 **Interactive schematics**: Embed fully interactive KiCad schematics that users can pan, zoom, and explore
- 📝 **Multiple syntax options**: Choose from Markdown, reStructuredText, or Liquid Tag syntax
- 🔌 **Automatic script loading**: KiCanvas JavaScript library loads automatically when needed
- ⚙️ **Customizable**: Control display size, styling, and viewer controls
- 🪶 **Lightweight**: No server-side processing required - uses CDN for KiCanvas library

## Installation

### 1. Install the plugin

#### From PyPI (when available)

```bash
# Using pip
pip install pelican-embed-kicad-kicanvas

# Or using uv (faster)
uv pip install pelican-embed-kicad-kicanvas
```

#### From GitHub (current release)

```bash
# Install directly from GitHub tag
pip install git+https://github.com/jordanauge/pelican-embed-kicad-kicanvas.git@v0.1.0

# Or download and install the wheel from GitHub Releases
# Visit: https://github.com/jordanauge/pelican-embed-kicad-kicanvas/releases/tag/v0.1.0
# Download pelican_embed_kicad_kicanvas-0.1.0-py3-none-any.whl
pip install pelican_embed_kicad_kicanvas-0.1.0-py3-none-any.whl
```

### 2. Enable in your Pelican configuration

Add the plugin to your `pelicanconf.py`:

```python
PLUGINS = [
    'pelican_kicad_embed',
    # ... other plugins
]
```

### 3. Configure schematic file paths (Optional)

The plugin automatically finds schematic files in multiple locations. **No configuration is required** if you place your `.kicad_sch` files alongside your article Markdown files.

#### Option A: Place schematics with articles (Recommended)

For maximum flexibility, place your schematic files in the same directory as your article:

```text
content/
├── blog/
│   └── my-article/
│       ├── index.md              # Your article
│       └── amplifier.kicad_sch   # Schematic file
```

Then reference it simply by filename:

```markdown
{{ kicad_schematic("amplifier.kicad_sch") }}
```

Pelican will automatically copy the schematic file alongside your article's HTML output.

#### Option B: Use a global schematics directory

If you prefer to store all schematics in one location, configure a default path in `pelicanconf.py`:

```python
# Optional: Default directory for schematic files
KICAD_SCHEMATICS_PATH = 'static/schematics'

# Ensure it's included in static paths
STATIC_PATHS = [
    'images',
    'static/schematics',
    # ... other static paths
]
```

Create the directory:

```bash
mkdir -p content/static/schematics
```

Place your `.kicad_sch` files in `content/static/schematics/`, and reference them by filename:

```markdown
{{ kicad_schematic("amplifier.kicad_sch") }}
```

#### Path Resolution Order

The plugin searches for schematics in this order:

1. **Absolute paths**: If you provide an absolute path, it's used as-is
2. **Relative to article**: Looks in the same directory as the `.md` file
3. **KICAD_SCHEMATICS_PATH**: Uses the configured default directory (if set)
4. **Fallback**: Uses the filename as-is (relative to output root)

## Usage

The plugin provides three syntax options. All produce the same output - choose the one that best fits your workflow.

### Option 1: Markdown Syntax (Recommended)

Use this syntax in `.md` files:

```markdown
{{ kicad_schematic("amplifier.kicad_sch", style="width: 800px; height: 500px;", controls="full") }}
```

**Minimal example** (with defaults):

```markdown
{{ kicad_schematic("amplifier.kicad_sch") }}
```

### Option 2: reStructuredText Syntax

Use this syntax in `.rst` files:

```rst
.. kicad-schematic:: amplifier.kicad_sch
   :style: width: 800px; height: 500px;
   :controls: full
```

**Minimal example** (with defaults):

```rst
.. kicad-schematic:: amplifier.kicad_sch
```

### Option 3: Liquid Tag Syntax (Optional)

If you have the `pelican-liquid-tags` plugin installed, you can use this syntax in both `.md` and `.rst` files:

```liquid
{% kicad_schematic amplifier.kicad_sch style="width: 800px; height: 500px;" controls="full" %}
```

**To enable Liquid Tag support**, install the additional dependency:

```bash
pip install pelican-embed-kicad-kicanvas[liquid]
```

Or manually:

```bash
pip install pelican-liquid-tags
```

## Parameters

All three syntax options support the same parameters:

| Parameter | Description | Example | Default |
|-----------|-------------|---------|---------|
| `filename` | **(Required)** Name of the `.kicad_sch` file in `/static/schematics/` | `amplifier.kicad_sch` | — |
| `style` | CSS style attributes for the viewer | `width: 800px; height: 500px;` | Empty (uses KiCanvas defaults) |
| `controls` | Viewer controls mode | `full`, `minimal`, `none` | Empty (uses KiCanvas defaults) |

### Style Parameter

The `style` parameter accepts any valid CSS style attributes:

```markdown
{{ kicad_schematic("example.kicad_sch", style="width: 100%; height: 600px; border: 1px solid #ccc;") }}
```

### Controls Parameter

The `controls` parameter defines the viewer interface:

- `full`: All controls (pan, zoom, layers, etc.)
- `minimal`: Basic controls only
- `none`: No controls (view only)

## Examples

### Full-featured Embed

**Markdown**:
```markdown
{{ kicad_schematic("power_supply.kicad_sch", style="width: 1000px; height: 700px;", controls="full") }}
```

**reStructuredText**:
```rst
.. kicad-schematic:: power_supply.kicad_sch
   :style: width: 1000px; height: 700px;
   :controls: full
```

### Minimal Embed (Default Size)

**Markdown**:
```markdown
{{ kicad_schematic("sensor.kicad_sch") }}
```

**reStructuredText**:
```rst
.. kicad-schematic:: sensor.kicad_sch
```

### Responsive Width

**Markdown**:
```markdown
{{ kicad_schematic("circuit.kicad_sch", style="width: 100%; height: 500px;") }}
```

## Generated HTML

All three syntax options generate the same HTML output:

```html
<kicanvas-embed 
    src="/static/schematics/amplifier.kicad_sch" 
    controls="full" 
    style="width: 800px; height: 500px;">
</kicanvas-embed>
```

The plugin automatically injects the KiCanvas JavaScript library when any schematic is detected:

```html
<script src="https://unpkg.com/kicanvas@latest/dist/kicanvas.js"></script>
```

## Dependencies

### Required

- **Pelican** (≥4.5): Static site generator
- **Markdown** (≥3.2): For Markdown syntax support
- **docutils** (≥0.16): For reStructuredText syntax support

These are automatically installed with the plugin.

### Optional

- **pelican-liquid-tags** (≥1.0.0): Only required for Liquid Tag syntax support

Install with:

```bash
pip install pelican-embed-kicad-kicanvas[liquid]
```

## Compatibility with Other Plugins

### pelican-jinja2content

If you use the `pelican-jinja2content` plugin (which processes article content as Jinja2 templates), this plugin automatically registers the `kicad_schematic` function in Jinja2's global context. This means you can use the same Markdown syntax without any additional configuration:

```markdown
{{ kicad_schematic("amplifier.kicad_sch", style="width: 800px; height: 500px;") }}
```

The function works seamlessly with both pelican-jinja2content and the standard Markdown extension.

**No configuration needed** - it just works!

## KiCanvas Dependency Management

The plugin includes KiCanvas locally for reliability and offline support. The JavaScript library is bundled in `content/static/js/kicanvas.js` and automatically copied to your output directory.

### Version Control

Track the current KiCanvas version:

```bash
cat KICANVAS_VERSION
# Output: 4c27152 (git commit hash)
```

### Update KiCanvas

To update to the latest version:

```bash
# Using the update script
./scripts/update_kicanvas.sh

# Or manually
curl -L -o content/static/js/kicanvas.js https://kicanvas.org/kicanvas/kicanvas.js
echo "NEW_VERSION_HASH" > KICANVAS_VERSION
```

### Check for Updates

```bash
# Checks if a new version is available
python3 scripts/check_kicanvas_version.py
```

This compares your local version against the latest commit in the KiCanvas GitHub repository.

### Using CDN Instead (Optional)

If you prefer to use the CDN version (not recommended for production):

```python
# pelicanconf.py
KICANVAS_USE_CDN = True
```

This loads KiCanvas from `https://kicanvas.org/kicanvas/kicanvas.js` instead of the local copy.

## Development and Quality Assurance

### Verification Suite

Run all quality checks before committing:

```bash
make verify
```

This runs:

- **Code formatting** (ruff format --check)
- **Linting** (ruff check)
- **Type checking** (pyright)
- **Dependency updates** (KiCanvas version check)

### Individual Checks

```bash
# Linting only
make lint

# Type checking only
make typecheck

# Check for KiCanvas updates
python3 scripts/check_kicanvas_version.py
```

### Auto-fix Issues

```bash
# Auto-format code
ruff format pelican_kicad_embed/ scripts/

# Auto-fix linting errors
ruff check --fix pelican_kicad_embed/ scripts/
```

### GitHub Actions CI/CD

The repository includes automated workflows:

- **Test workflow** (`.github/workflows/test.yml`): Runs on every PR
  - Multi-platform testing (Ubuntu, macOS, Windows)
  - Python 3.8-3.11 compatibility
  - Code coverage reporting
  - Linting and formatting checks
  - Dependency version verification
  
- **Release workflow** (`.github/workflows/release.yml`): Triggered on tags
  - Builds distribution packages
  - Signs with Sigstore
  - Publishes to PyPI

## Troubleshooting

### Runtime

- **KiCanvas**: Loaded locally from `/static/js/kicanvas.js`
  - Bundled with the plugin for offline support
  - No external CDN dependencies (unless KICANVAS_USE_CDN=True)
  - Update with `./scripts/update_kicanvas.sh`

## Common Issues

### Schematics Not Displaying

1. **Verify file path**: Ensure `.kicad_sch` files are in `content/static/schematics/`
2. **Check STATIC_PATHS**: Confirm `static/schematics` is in your `pelicanconf.py` STATIC_PATHS
3. **Inspect browser console**: Look for 404 errors on schematic file URLs
4. **Verify syntax**: Ensure you're using the correct syntax for your file type (.md vs .rst)

### KiCanvas Script Not Loading

- Check browser console for JavaScript errors
- Verify internet connection (KiCanvas loads from CDN)
- Ensure no Content Security Policy blocking `unpkg.com`

### Liquid Tag Not Working

- Install the optional dependency: `pip install pelican-liquid-tags`
- Enable both plugins in `pelicanconf.py`:

  ```python
  PLUGINS = ['pelican_kicad_embed', 'liquid_tags']
  ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Credits

- **KiCanvas**: [github.com/theacodes/kicanvas](https://github.com/theacodes/kicanvas) - Interactive KiCad viewer
- **Pelican**: [getpelican.com](https://getpelican.com) - Static site generator

## Changelog

### 0.1.0 (2025-11-17)

- Initial release with comprehensive test suite (84 tests, 100% passing)
- Support for three syntax variants: Markdown Extension, reStructuredText Directive, Liquid Tag
- Automatic KiCanvas JavaScript library injection
- Configurable style and controls parameters
- Flexible filename parsing (quoted/unquoted, spaces supported)
- Parameter order-independent parsing
- GitHub Actions CI/CD workflows with Sigstore signing
- Multi-platform testing (Ubuntu, macOS, Windows)
- Python 3.7-3.11 support
