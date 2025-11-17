# Quick Start Guide

Get up and running with pelican-embed-kicad-kicanvas in 5 minutes!

## Step 1: Install the Plugin

```bash
pip install pelican-embed-kicad-kicanvas
```

## Step 2: Enable in Pelican

Edit your `pelicanconf.py`:

```python
PLUGINS = [
    'pelican_kicad_embed',
    # ... your other plugins
]

STATIC_PATHS = [
    'images',
    'static/schematics',  # Add this
]
```

## Step 3: Add Your Schematics

Create the directory and add your KiCad files:

```bash
mkdir -p content/static/schematics
cp /path/to/your/schematic.kicad_sch content/static/schematics/
```

## Step 4: Embed in Your Content

### In Markdown (`.md`) files:

```markdown
Title: My Project
Date: 2025-11-17

Check out my amplifier circuit:

{{ kicad_schematic("amplifier.kicad_sch", style="width: 800px; height: 600px;") }}
```

### In reStructuredText (`.rst`) files:

```rst
My Project
==========

:date: 2025-11-17

Check out my amplifier circuit:

.. kicad-schematic:: amplifier.kicad_sch
   :style: width: 800px; height: 600px;
```

## Step 5: Build Your Site

```bash
pelican content
pelican --listen  # View at http://localhost:8000
```

## That's It!

Your schematics should now be interactive and viewable in the browser. 🎉

## Need More?

- **Customize controls**: Add `controls="full"` for full viewer interface
- **Responsive sizing**: Use `style="width: 100%; height: 500px;"` for responsive width
- **Multiple schematics**: Just add more embed tags throughout your content

## Troubleshooting

**Schematic not showing?**
- Check that the `.kicad_sch` file is in `content/static/schematics/`
- Verify `STATIC_PATHS` includes `static/schematics` in `pelicanconf.py`
- Check browser console for JavaScript errors

**Plugin not working?**
- Ensure you ran `pip install pelican-embed-kicad-kicanvas`
- Verify `pelican_kicad_embed` is in `PLUGINS` list in `pelicanconf.py`
- Try rebuilding: `pelican content --delete-output-directory`

## Next Steps

- Read the [full README](README.md) for all features
- Check out [examples](examples/) for more use cases
- Learn about the [architecture](ARCHITECTURE.md)
