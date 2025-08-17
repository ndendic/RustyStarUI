# Changelog

All notable changes to StarUI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-08-17

### Fixed
- Fixed create-release workflow to correctly update only the project version
- Fixed create-release workflow version extraction to use grep instead of tomli
- Fixed GitHub Actions to use `uv pip install` instead of `python -m pip install`

## [0.1.0] - 2025-08-17

### Added
- 🎨 **Core Component Library**
  - Button component with shadcn/ui variants (default, destructive, outline, secondary, ghost, link)
  - Alert component with title and description support
  - Badge component with clickable variants
  - Card component with header, content, and footer sections
  - Input component with comprehensive form support
  - Label component with accessibility features

- 🔧 **CLI Tools**
  - `star init` - Initialize new StarUI projects
  - `star add <component>` - Add components to existing projects  
  - `star dev <app.py>` - Development server with hot reloading
  - `star build` - Build production CSS
  - `star list` - List available components

- ⚡ **Modern Development Experience**
  - Zero-configuration setup with sensible defaults
  - Automatic Tailwind CSS v4 integration
  - shadcn/ui color scheme and design tokens
  - CSS reset and dark mode support
  - File watching and hot reloading

- 🎯 **StarHTML Integration**
  - Native StarHTML component compatibility
  - Type-safe component APIs with pragmatic flexibility
  - Proper FT return types and HTML attribute support
  - StarHTML dependency with type stubs

- 📦 **Build System & Quality**
  - Modern Python packaging with pyproject.toml
  - Comprehensive GitHub Actions CI/CD
  - Code quality enforcement (ruff, pyright, pytest)
  - Automated PyPI publishing with manual version selection
  - 25% test coverage with behavior-focused testing

### Technical Details
- **Dependencies**: StarHTML, Typer, Watchdog, Requests, Pydantic, Rich
- **Python Support**: 3.12+
- **Package Size**: ~34KB wheel
- **Type Safety**: 0 pyright errors with pragmatic configuration
- **Code Quality**: 100% ruff compliance


[0.1.0]: https://github.com/banditburai/starui/releases/tag/v0.1.0
[0.1.1]: https://github.com/banditburai/starui/releases/tag/v0.1.1