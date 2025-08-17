"""Tests for CLI utilities."""

from unittest.mock import patch

import pytest

from starui.cli.utils import (
    confirm,
    console,
    create_progress,
    error,
    get_project_root,
    info,
    success,
    validate_component_name,
    warning,
)


class TestConsoleUtilities:
    """Test cases for console utility functions."""

    @patch("starui.cli.utils.console.print")
    def test_success_message(self, mock_print):
        """Test success message formatting."""
        success("Operation completed successfully")

        mock_print.assert_called_once()
        args = mock_print.call_args[0]
        # Should include green color and success indicator
        assert "[green]" in str(args[0]) or "✓" in str(args[0])

    @patch("starui.cli.utils.console.print")
    def test_error_message(self, mock_print):
        """Test error message formatting."""
        error("Something went wrong")

        mock_print.assert_called_once()
        args = mock_print.call_args[0]
        # Should include red color and error indicator
        assert "[red]" in str(args[0]) or "✗" in str(args[0]) or "❌" in str(args[0])

    @patch("starui.cli.utils.console.print")
    def test_warning_message(self, mock_print):
        """Test warning message formatting."""
        warning("This is a warning")

        mock_print.assert_called_once()
        args = mock_print.call_args[0]
        # Should include yellow color and warning indicator
        assert "[yellow]" in str(args[0]) or "⚠" in str(args[0])

    @patch("starui.cli.utils.console.print")
    def test_info_message(self, mock_print):
        """Test info message formatting."""
        info("Information message")

        mock_print.assert_called_once()
        args = mock_print.call_args[0]
        # Should include blue color or info indicator
        assert "[blue]" in str(args[0]) or "ℹ" in str(args[0])

    @patch("starui.cli.utils.typer.confirm")
    def test_confirm_function(self, mock_confirm):
        """Test confirmation prompt."""
        mock_confirm.return_value = True

        result = confirm("Are you sure?")

        assert result is True
        mock_confirm.assert_called_once_with("Are you sure?", default=False)

    def test_create_progress(self):
        """Test progress bar creation."""
        progress = create_progress()

        assert progress is not None
        assert hasattr(progress, "add_task")
        assert hasattr(progress, "update")


class TestProjectUtilities:
    """Test cases for project-related utilities."""

    def test_get_project_root_with_pyproject(self, tmp_path):
        """Test project root detection with pyproject.toml."""
        # Create a temporary project structure
        pyproject_file = tmp_path / "pyproject.toml"
        pyproject_file.write_text("[project]\nname = 'test'\n")

        subdir = tmp_path / "src" / "package"
        subdir.mkdir(parents=True)

        # Should find the project root from subdirectory
        with patch("pathlib.Path.cwd", return_value=subdir):
            root = get_project_root()
            assert root == tmp_path

    def test_get_project_root_without_pyproject(self, tmp_path):
        """Test project root detection without pyproject.toml."""
        subdir = tmp_path / "src" / "package"
        subdir.mkdir(parents=True)

        # Should return current directory if no pyproject.toml found
        with patch("pathlib.Path.cwd", return_value=subdir):
            root = get_project_root()
            assert root == subdir

    def test_validate_component_name_valid(self):
        """Test component name validation with valid names."""
        valid_names = ["button", "card", "input-field", "data-table"]

        for name in valid_names:
            assert validate_component_name(name) is True

    def test_validate_component_name_invalid(self):
        """Test component name validation with invalid names."""
        invalid_names = ["", "Button", "button_field", "123button", "button@#"]

        for name in invalid_names:
            assert validate_component_name(name) is False


class TestUtilityConfiguration:
    """Test cases for utility configuration."""

    def test_console_is_configured(self):
        """Test that console is properly configured."""
        assert console is not None
        assert hasattr(console, "print")
        assert hasattr(console, "status")

    def test_console_rich_integration(self):
        """Test that console integrates with Rich properly."""
        # Test that we can create status and progress
        with console.status("Testing...") as status:
            assert status is not None

        # Test that we can print with markup
        try:
            console.print("[green]Test[/green]", end="")
        except Exception:
            pytest.fail("Console should handle Rich markup")


class TestErrorHandling:
    """Test cases for error handling utilities."""

    def test_error_with_exception(self):
        """Test error handling with exception object."""
        test_exception = ValueError("Test error")

        with patch("starui.cli.utils.console.print") as mock_print:
            error("Operation failed", exception=test_exception)

            mock_print.assert_called()
            # Should have printed both the message and exception info
            assert mock_print.call_count >= 1

    def test_error_with_suggestions(self):
        """Test error with suggestions."""
        suggestions = ["Try running with --verbose", "Check your configuration"]

        with patch("starui.cli.utils.console.print") as mock_print:
            error("Operation failed", suggestions=suggestions)

            mock_print.assert_called()
            # Should have printed suggestions
            printed_content = str(mock_print.call_args_list)
            assert "Try running with --verbose" in printed_content or any(
                "Try running with --verbose" in str(call)
                for call in mock_print.call_args_list
            )
