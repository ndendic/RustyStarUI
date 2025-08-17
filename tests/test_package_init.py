"""Test package initialization and basic functionality."""


def test_package_importable():
    """Test that starui package can be imported."""
    import starui

    assert starui.__version__ is not None


def test_package_version():
    """Test that package version is correctly set."""
    import starui

    assert starui.__version__ == "0.1.0"


def test_package_has_entry_point():
    """Test that CLI entry point is properly configured."""
    import tomllib
    from pathlib import Path

    # Read pyproject.toml to check entry point configuration
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)

    # Verify CLI entry point is configured
    scripts = pyproject_data.get("project", {}).get("scripts", {})
    assert "star" in scripts, "CLI entry point 'star' not found in project.scripts"
    assert scripts["star"] == "starui.cli.main:app", (
        "CLI entry point has incorrect target"
    )
