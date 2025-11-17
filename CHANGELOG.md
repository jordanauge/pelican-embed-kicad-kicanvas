# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-18

### 🚀 Initial Release

**Self-contained Pelican plugin for embedding interactive KiCad schematics**

- **Theme-independent script injection**: Direct HTML manipulation, works with any Pelican theme
- **Local KiCanvas bundle**: 441KB ES6 module included (version 4c27152), no external CDN dependencies
- **`.. kicad_schematic::` directive**: Embed KiCad `.kicad_sch` files in blog posts
- **Automatic file management**: Copy schematics to output, calculate proper URLs
- **Path resolution**: Support for relative paths, absolute paths, content-relative paths
- **Configuration option**: `KICANVAS_USE_CDN` to optionally use kicanvas.org CDN instead of local bundle

### 🛠️ DevOps & Quality Assurance

- **Comprehensive verification system**:
  - `make verify`: Unified verification command (lint + typecheck + dependency check)
  - `scripts/check_kicanvas_version.py`: Check for KiCanvas updates via GitHub API
  - `scripts/update_kicanvas.sh`: Download latest KiCanvas bundle
  - `scripts/lint.sh`: Code formatting and linting with ruff
  - `scripts/typecheck.sh`: Static type checking with pyright
- **CI/CD integration**: GitHub Actions workflow to verify dependencies before PRs
- **Version tracking**: `KICANVAS_VERSION` file tracks KiCanvas commit hash
- **Complete documentation**: DevOps workflows, dependency management, troubleshooting

### 📦 Features

- Interactive schematic viewer powered by [KiCanvas](https://github.com/theacodes/kicanvas)
- Automatic script injection when `.. kicad_schematic::` is used
- No theme modifications required - plugin is 100% self-contained
- Automatic URL generation for Pelican output structure
- Compatible with KiCad 9.0 schematic format

---

## Release Process

1. **Update version**: Bump version in `pelican_kicad_embed/__about__.py`
2. **Update CHANGELOG**: Document changes in this file
3. **Verify quality**: Run `make verify` (lint, typecheck, dependencies)
4. **Commit**: `git commit -m "chore: Prepare release vX.Y.Z"`
5. **Tag**: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
6. **Push**: `git push origin main --tags`
7. **GitHub Actions**: Automatically builds and publishes to PyPI

## Links

- [Repository](https://github.com/jordanauge/pelican-embed-kicad-kicanvas)
- [PyPI Package](https://pypi.org/project/pelican-embed-kicad-kicanvas/)
- [KiCanvas Project](https://github.com/theacodes/kicanvas)
