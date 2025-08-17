"""Tests for configuration models."""

from pathlib import Path

from starui.config import ProjectConfig


class TestProjectConfig:
    """Test the ProjectConfig model."""

    def test_config_creation(self):
        """Test creating a config with required values."""
        config = ProjectConfig(
            project_root=Path("/test/path"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config.project_root == Path("/test/path")
        assert config.css_output == Path("static/css/app.css")
        assert config.component_dir == Path("src/ui")

    def test_css_output_absolute_path(self):
        """Test css_output_absolute property."""
        config = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config.css_output_absolute == Path("/project/static/css/app.css")

        # Test with already absolute path
        config2 = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("/absolute/path/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config2.css_output_absolute == Path("/absolute/path/app.css")

    def test_component_dir_absolute_path(self):
        """Test component_dir_absolute property."""
        config = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("src/ui"),
        )

        assert config.component_dir_absolute == Path("/project/src/ui")

        # Test with already absolute path
        config2 = ProjectConfig(
            project_root=Path("/project"),
            css_output=Path("static/css/app.css"),
            component_dir=Path("/absolute/ui"),
        )

        assert config2.component_dir_absolute == Path("/absolute/ui")
