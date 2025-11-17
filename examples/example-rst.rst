Embedding KiCad Schematics - reStructuredText Example
======================================================

:date: 2025-11-17
:category: Electronics
:tags: kicad, schematics, pelican
:slug: rst-example
:author: Your Name
:summary: Demonstration of embedding KiCad schematics using reStructuredText syntax

Embedding KiCad Schematics with reStructuredText
-------------------------------------------------

This article demonstrates how to embed interactive KiCad schematics using the reStructuredText directive provided by the ``pelican-embed-kicad-kicanvas`` plugin.

Basic Embed
~~~~~~~~~~~

Here's a simple amplifier schematic with default settings:

.. kicad-schematic:: amplifier.kicad_sch

The viewer above uses KiCanvas's default dimensions and controls.

Custom Sized Embed
~~~~~~~~~~~~~~~~~~

You can customize the size using the ``:style:`` option:

.. kicad-schematic:: power_supply.kicad_sch
   :style: width: 100%; height: 600px;

This embed is responsive (100% width) with a fixed height of 600 pixels.

Full-Featured Embed
~~~~~~~~~~~~~~~~~~~

For complex schematics, you might want full controls:

.. kicad-schematic:: sensor_array.kicad_sch
   :style: width: 1000px; height: 700px; border: 1px solid #ddd;
   :controls: full

This embed includes:

- Custom dimensions (1000×700px)
- A subtle border for visual separation
- Full control interface

Multiple Schematics
~~~~~~~~~~~~~~~~~~~

You can embed multiple schematics in a single article.

Input Stage
^^^^^^^^^^^

.. kicad-schematic:: input_stage.kicad_sch
   :style: width: 800px; height: 400px;

Output Stage
^^^^^^^^^^^^

.. kicad-schematic:: output_stage.kicad_sch
   :style: width: 800px; height: 400px;

Conclusion
~~~~~~~~~~

The reStructuredText directive syntax is powerful and flexible, making it easy to embed interactive schematics in your technical documentation!
