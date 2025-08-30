"""Development server with CSS hot reload."""

import asyncio
import socket
import tempfile
import time
from pathlib import Path

import typer
from rich.panel import Panel
from rich.table import Table

from ..config import detect_project_config
from ..css.binary import TailwindBinaryManager
from ..dev import CSSHotReloadServer
from ..dev.process_manager import ProcessManager
from ..templates.css_input import generate_css_input
from .utils import console, error, success


def check_port_available(port: int) -> bool:
    """Check if a port is available."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
            return True
    except OSError:
        return False


def find_available_port(start_port: int = 5000, max_tries: int = 100) -> int:
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_tries):
        if check_port_available(port):
            return port
    raise RuntimeError(
        f"No available ports in range {start_port}-{start_port + max_tries}"
    )


def dev_command(
    app_file: str | None = typer.Argument(None, help="StarHTML app file to run"),
    port: int = typer.Option(5000, "--port", "-p", help="Port for app server"),
    css_hot_reload: bool = typer.Option(
        True, "--css-hot/--no-css-hot", help="Enable CSS hot reload"
    ),
    strict: bool = typer.Option(
        False, "--strict", help="Fail if requested port is unavailable"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show details"),
) -> None:
    """Start development server with CSS hot reload.

    By default, if the requested port is in use, automatically finds the next
    available port. Use --strict to disable this behavior.
    """

    if not app_file:
        error("App file is required")
        raise typer.Exit(1)

    app_path = Path(app_file)
    if not app_path.exists():
        error(f"App file not found: {app_file}")
        raise typer.Exit(1)

    config = detect_project_config()
    manager = ProcessManager()
    input_css_path = None

    # Handle port availability
    if check_port_available(port):
        actual_port = port
    elif strict:
        error(f"Port {port} is already in use")
        raise typer.Exit(1)
    else:
        console.print(
            f"[yellow]Port {port} is in use, finding available port...[/yellow]"
        )
        actual_port = find_available_port(port + 1)
        success(f"✓ Using port {actual_port} instead")

    # Always auto-discover CSS WebSocket port
    css_ws_port = find_available_port(actual_port + 1)  # Try next port after app port

    try:
        input_css_path = _prepare_css_input(config)
        websocket_server = _start_css_hot_reload(
            css_hot_reload, css_ws_port, manager, verbose
        )
        _start_tailwind_watcher(manager, input_css_path, config, websocket_server)
        _wait_for_css_build(config)
        _start_app_server(manager, app_path, actual_port, css_ws_port, css_hot_reload)
        _display_info(config, actual_port, css_ws_port, css_hot_reload, app_file)

        console.print("Press Ctrl+C to stop\n")
        try:
            manager.wait_for_any_exit()
        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/yellow]")

    except Exception as e:
        error(f"Dev server error: {e}")
        raise typer.Exit(1) from e
    finally:
        manager.stop_all()
        _cleanup_temp_files(input_css_path, config, app_path, verbose)


def _prepare_css_input(config) -> Path:
    """Get or create CSS input file for Tailwind."""
    project_input = config.project_root / "static" / "css" / "input.css"

    if project_input.exists():
        return project_input

    config.css_output_absolute.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".css",
        dir=config.css_output_absolute.parent,
        delete=False,
    ) as f:
        f.write(generate_css_input(config))
        return Path(f.name)


def _start_css_hot_reload(
    enabled: bool, port: int, manager: ProcessManager, verbose: bool
) -> CSSHotReloadServer | None:
    """Start CSS hot reload WebSocket server if enabled."""
    if not enabled:
        return None

    try:
        loop = asyncio.new_event_loop()
        websocket_server = CSSHotReloadServer(port=port)
        manager.start_websocket_server(websocket_server, loop)
        success(f"✓ CSS hot reload enabled on port {port}")
        return websocket_server
    except Exception as e:
        error(f"Failed to start CSS hot reload: {e}")
        return None


def _start_tailwind_watcher(
    manager: ProcessManager, input_css: Path, config, websocket_server
):
    """Start Tailwind CSS watcher process."""
    binary_manager = TailwindBinaryManager("latest")

    def notify_css_update(css_path: Path):
        if websocket_server:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(websocket_server.notify_css_update(css_path, 0))
            except Exception:
                pass
            finally:
                loop.close()

    manager.start_tailwind_watcher(
        tailwind_binary=Path(binary_manager.get_binary()),
        input_css=input_css,
        output_css=config.css_output_absolute,
        project_root=config.project_root,
        on_rebuild=notify_css_update if websocket_server else None,
    )


def _wait_for_css_build(config):
    """Wait for initial CSS build to complete."""
    if config.css_output_absolute.exists():
        success("✓ CSS ready")
        return

    console.print("[yellow]Building CSS...[/yellow]")
    for _ in range(20):
        if config.css_output_absolute.exists():
            success("✓ CSS built")
            return
        time.sleep(0.5)

    error("CSS build timed out")
    raise typer.Exit(1)


def _start_app_server(
    manager: ProcessManager,
    app_path: Path,
    port: int,
    css_ws_port: int,
    css_hot_reload: bool = True,
):
    """Start uvicorn app server."""
    manager.start_uvicorn(
        app_file=app_path,
        port=port,
        watch_patterns=["*.py", "*.html"],
        enable_css_hot_reload=css_hot_reload,
        css_ws_port=css_ws_port,
    )
    success(f"✓ Server running at http://localhost:{port}")


def _display_info(
    config, port: int, css_ws_port: int, css_hot_reload: bool, app_file: str
):
    """Display development server status."""
    table = Table(title="StarUI Development Server", show_header=False)
    table.add_column(style="cyan")
    table.add_column(style="green")

    table.add_row("App", f"http://localhost:{port}")
    table.add_row("File", app_file)
    table.add_row("CSS", str(config.css_output))
    if css_hot_reload:
        table.add_row("Hot Reload", f"✓ (WebSocket on port {css_ws_port})")
    else:
        table.add_row("Hot Reload", "✗")

    console.print(Panel(table, border_style="green"))


def _cleanup_temp_files(
    input_css_path: Path | None, config, app_path: Path, verbose: bool
):
    """Clean up temporary files."""
    if input_css_path and input_css_path.name.startswith("tmp"):
        input_css_path.unlink(missing_ok=True)

    # Clean up all dev wrapper files
    for wrapper_file in app_path.parent.glob(f"{app_path.stem}_dev_*.py"):
        wrapper_file.unlink(missing_ok=True)

    try:
        for temp_file in config.css_output_absolute.parent.glob("tmp*.css"):
            temp_file.unlink()
    except Exception:
        pass
