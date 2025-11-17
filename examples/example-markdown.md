Title: Embedding KiCad Schematics - Markdown Example
Date: 2025-11-17
Category: Electronics
Tags: kicad, schematics, pelican
Slug: markdown-example
Author: Your Name
Summary: Demonstration of embedding KiCad schematics using Markdown syntax

# Embedding KiCad Schematics with Markdown

This article demonstrates how to embed interactive KiCad schematics using the Markdown syntax provided by the `pelican-embed-kicad-kicanvas` plugin.

## Basic Embed

Here's a simple amplifier schematic with default settings:

{{ kicad_schematic("amplifier.kicad_sch") }}

The viewer above uses KiCanvas's default dimensions and controls.

## Custom Sized Embed

You can customize the size using the `style` parameter:

{{ kicad_schematic("power_supply.kicad_sch", style="width: 100%; height: 600px;") }}

This embed is responsive (100% width) with a fixed height of 600 pixels.

## Full-Featured Embed

For complex schematics, you might want full controls:

{{ kicad_schematic("sensor_array.kicad_sch", style="width: 1000px; height: 700px; border: 1px solid #ddd;", controls="full") }}

This embed includes:
- Custom dimensions (1000×700px)
- A subtle border for visual separation
- Full control interface

## Multiple Schematics

You can embed multiple schematics in a single article:

### Input Stage

{{ kicad_schematic("input_stage.kicad_sch", style="width: 800px; height: 400px;") }}

### Output Stage

{{ kicad_schematic("output_stage.kicad_sch", style="width: 800px; height: 400px;") }}

## Conclusion

The Markdown syntax is clean and intuitive, making it easy to embed interactive schematics in your technical blog posts!
