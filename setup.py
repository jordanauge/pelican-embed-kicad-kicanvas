"""Setup configuration for pelican-embed-kicad-kicanvas plugin."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from setuptools import find_packages, setup

# Read version from __about__.py
about: dict[str, Any] = {}
with open(Path(__file__).parent / "pelican_kicad_embed" / "__about__.py") as f:
    exec(f.read(), about)  # noqa: S102

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pelican-embed-kicad-kicanvas",
    version=about["__version__"],
    author=about["__author__"],
    author_email="jordan.auge@example.com",  # Update with actual email
    description="Pelican plugin for embedding interactive KiCad schematics using KiCanvas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pelican-embed-kicad-kicanvas",  # Update with actual URL
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Pelican :: Plugins",
    ],
    keywords="pelican plugin kicad kicanvas schematic electronics",
    python_requires=">=3.7",
    install_requires=[
        "pelican>=4.5",
        "markdown>=3.2",
        "docutils>=0.16",
    ],
    extras_require={
        "liquid": ["pelican-liquid-tags>=1.0.0"],
    },
    entry_points={
        "pelican.plugins": [
            "pelican_kicad_embed = pelican_kicad_embed",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    license="MIT",
)
