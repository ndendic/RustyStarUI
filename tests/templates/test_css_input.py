"""Tests for CSS input template generation."""

from pathlib import Path

from starui.config import ProjectConfig
from starui.templates.css_input import generate_css_input


class TestCSSInput:
    """Test the CSS input generation."""

    def test_generate_css_input_with_reset(self):
        """Test CSS generation includes reset by default."""
        css = generate_css_input()

        assert '@import "tailwindcss";' in css
        assert "box-sizing: border-box" in css
        assert ":root {" in css
        assert "--background:" in css
        assert "--foreground:" in css

    def test_generate_css_input_without_reset(self):
        """Test CSS generation without reset."""
        css = generate_css_input(include_reset=False)

        assert "box-sizing: border-box" not in css
        assert ":root {" in css  # Theme variables should still be there

    def test_generate_css_input_with_config(self):
        """Test CSS generation with a config (though it's unused)."""
        config = ProjectConfig(
            project_root=Path("/tmp/test"),
            css_output=Path("dist/styles.css"),
            component_dir=Path("components/ui"),
        )
        css = generate_css_input(config)

        assert ":root {" in css
        assert "--background:" in css

    def test_dark_theme_variables_included(self):
        """Test that dark theme variables are included."""
        css = generate_css_input()

        assert ".dark {" in css
        assert ".dark" in css and "--background: oklch(0.145 0 0);" in css
        assert "@theme inline {" in css
