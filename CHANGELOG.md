# Changelog

All notable changes to StarUI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **🎨 Optimized Template System**
  - 57% CSS reduction with hybrid theming support
  - Enhanced ThemeToggle component with smart .dark class and data-theme detection
  - WCAG AA compliant OKLCH colors for better accessibility
  - Default theme system included in `star init` for immediate productivity

### Changed
- **🔧 Modern, Idiomatic Codebase**
  - Refactored CLI commands (add.py, init.py) for concise, Pythonic patterns
  - Enhanced app starter template with semantic color system
  - Improved ThemeToggle to intelligently handle both Tailwind and semantic approaches
  - Updated dependency resolution system with comprehensive test coverage

### Fixed
- **✨ Enhanced Developer Experience**
  - Removed CSS reset (Tailwind v4 handles it automatically)
  - Fixed StarHTML DatastarAttr type compatibility (no more type: ignore needed)
  - Enhanced component dependency system with theme_toggle → button resolution
  - Improved code formatting and linting compliance across all files

### Technical
- Updated StarHTML dependency to use latest GitHub version with DatastarAttr type fixes
- Added comprehensive test suite for dependency resolution system
- Enhanced ThemeToggle to support both `.dark` class and `data-theme` attribute approaches

## [0.1.2] - 2025-08-18

### Changed
- Updated default theme to use modern `oklch` color space matching shadcn v2 with Tailwind v4
- Modernized type hints to use Python 3.10+ union syntax (`X | None` instead of `Optional[X]`)
- Improved code quality with more Pythonic patterns (dict comprehensions, walrus operator)

### Fixed
- Fixed CSS template generation - removed double curly braces that were causing Tailwind v4 errors
- Fixed component import transformation - components now correctly import utilities from starui instead of relative imports

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
[0.1.2]: https://github.com/banditburai/starUI/releases/tag/v0.1.2
