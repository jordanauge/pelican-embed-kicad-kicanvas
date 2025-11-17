# Examples

This directory contains example Pelican content files demonstrating the plugin's usage.

## Files

### `example-markdown.md`

Demonstrates the Markdown syntax for embedding KiCad schematics:

```markdown
{{ kicad_schematic("filename.kicad_sch", style="...", controls="...") }}
```

### `example-rst.rst`

Demonstrates the reStructuredText directive syntax:

```rst
.. kicad-schematic:: filename.kicad_sch
   :style: ...
   :controls: ...
```

## Using These Examples

1. Copy these files to your Pelican `content/` directory
2. Place corresponding `.kicad_sch` files in `content/static/schematics/`
3. Run `pelican content` to build your site
4. View the generated HTML in `output/`

## Note

These examples reference schematic files that don't exist in this repository. You'll need to replace the filenames with your actual KiCad schematic files:

- `amplifier.kicad_sch`
- `power_supply.kicad_sch`
- `sensor_array.kicad_sch`
- `input_stage.kicad_sch`
- `output_stage.kicad_sch`
