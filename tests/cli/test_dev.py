"""Tests for the development server command."""

import subprocess
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from starui.cli.dev import (
    cleanup,
    get_or_create_css_input,
    setup_tailwind,
    show_status,
    wait_for_css,
)
from starui.dev.process_manager import ProcessManager


def test_get_or_create_css_input_existing(tmp_path):
    """Test that existing input.css is returned."""
    config = MagicMock()
    config.project_root = tmp_path
    
    # Create existing input.css
    css_dir = tmp_path / "static" / "css"
    css_dir.mkdir(parents=True)
    input_css = css_dir / "input.css"
    input_css.write_text("/* existing */")
    
    result = get_or_create_css_input(config)
    assert result == input_css


def test_get_or_create_css_input_creates_temp(tmp_path):
    """Test that temporary CSS is created when no input.css exists."""
    config = MagicMock()
    config.project_root = tmp_path
    config.css_output_absolute = tmp_path / "output.css"
    
    with patch("starui.cli.dev.generate_css_input") as mock_gen:
        mock_gen.return_value = "/* generated */"
        result = get_or_create_css_input(config)
        
        assert result.exists()
        assert result.suffix == ".css"
        assert result.read_text() == "/* generated */"
        mock_gen.assert_called_once_with(config)


def test_cleanup():
    """Test cleanup removes files."""
    mock_paths = [MagicMock(spec=Path) for _ in range(3)]
    mock_paths.append(None)  # Test None handling
    
    cleanup(*mock_paths)
    
    for path in mock_paths[:3]:
        path.unlink.assert_called_once_with(missing_ok=True)


@patch("starui.cli.dev.success")
def test_wait_for_css_exists(mock_success, tmp_path):
    """Test wait_for_css when CSS already exists."""
    css_path = tmp_path / "test.css"
    css_path.write_text("/* css */")
    
    wait_for_css(css_path)
    mock_success.assert_called_once_with("CSS ready")


@patch("starui.cli.dev.error")
@patch("starui.cli.dev.console")
@patch("time.sleep")
def test_wait_for_css_timeout(mock_sleep, mock_console, mock_error, tmp_path):
    """Test wait_for_css timeout."""
    from click.exceptions import Exit
    css_path = tmp_path / "nonexistent.css"
    
    with pytest.raises(Exit):
        wait_for_css(css_path, timeout=0.1)
    
    mock_console.print.assert_called_once()
    mock_error.assert_called_once_with("CSS build timed out")


class TestProcessManager:
    """Tests for ProcessManager class."""
    
    def test_init(self):
        """Test ProcessManager initialization."""
        manager = ProcessManager()
        assert manager.processes == {}
        assert manager.threads == {}
        assert not manager.shutdown.is_set()
    
    def test_start_process_existing(self):
        """Test starting process when one already exists."""
        manager = ProcessManager()
        mock_process = MagicMock()
        manager.processes["test"] = mock_process
        
        result = manager.start_process("test", ["cmd"])
        assert result == mock_process
    
    @patch("subprocess.Popen")
    def test_start_process_new(self, mock_popen):
        """Test starting a new process."""
        manager = ProcessManager()
        mock_proc = MagicMock()
        mock_proc.stdout.readline.return_value = ""
        mock_proc.poll.return_value = 0
        mock_popen.return_value = mock_proc
        
        result = manager.start_process("test", ["cmd"])
        assert result == mock_proc
        assert manager.processes["test"] == mock_proc
    
    def test_is_running(self):
        """Test checking if process is running."""
        manager = ProcessManager()
        mock_proc = MagicMock()
        mock_proc.poll.return_value = None
        manager.processes["test"] = mock_proc
        
        assert manager.is_running("test")
        
        mock_proc.poll.return_value = 0
        assert not manager.is_running("test")
    
    def test_stop_process(self):
        """Test stopping a process."""
        manager = ProcessManager()
        mock_proc = MagicMock()
        manager.processes["test"] = mock_proc
        
        manager.stop_process("test")
        mock_proc.terminate.assert_called_once()
        assert "test" not in manager.processes
    
    def test_stop_all(self):
        """Test stopping all processes."""
        manager = ProcessManager()
        mock_procs = {f"test{i}": MagicMock() for i in range(3)}
        manager.processes = mock_procs.copy()
        
        manager.stop_all()
        
        assert manager.shutdown.is_set()
        assert manager.processes == {}
        assert manager.threads == {}
        
        for proc in mock_procs.values():
            proc.terminate.assert_called_once()