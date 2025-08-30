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


def port_available(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", port))
            return True
    except OSError:
        return False


def find_port(start: int = 5000, max_tries: int = 100) -> int:
    for port in range(start, start + max_tries):
        if port_available(port):
            return port
    raise RuntimeError(f"No ports available in {start}-{start + max_tries}")


def resolve_port(requested: int, strict: bool) -> int:
    if port_available(requested):
        return requested

    if strict:
        error(f"Port {requested} is already in use")
        raise typer.Exit(1)

    console.print(f"[yellow]Port {requested} in use, finding available...[/yellow]")
    available = find_port(requested + 1)
    success(f"✓ Using port {available}")
    return available


def prepare_css_input(config) -> Path:
    project_input = config.project_root / "static" / "css" / "input.css"
    if project_input.exists():
        return project_input

    css_dir = config.css_output_absolute.parent
    css_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".css", dir=css_dir, delete=False
    ) as f:
        f.write(generate_css_input(config))
        return Path(f.name)


def start_css_websocket(
    port: int, manager: ProcessManager
) -> CSSHotReloadServer | None:
    try:
        loop = asyncio.new_event_loop()
        server = CSSHotReloadServer(port=port)
        manager.start_websocket_server(server, loop)
        success(f"✓ CSS hot reload on port {port}")
        return server
    except Exception as e:
        error(f"CSS hot reload failed: {e}")
        return None


def start_tailwind(manager: ProcessManager, input_css: Path, config, ws_server):
    binary = TailwindBinaryManager("latest").get_binary()

    callback = None
    if ws_server:

        def callback(css_path: Path):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(ws_server.notify_css_update(css_path, 0))
            except Exception:
                pass
            finally:
                loop.close()

    manager.start_tailwind_watcher(
        tailwind_binary=Path(binary),
        input_css=input_css,
        output_css=config.css_output_absolute,
        project_root=config.project_root,
        on_rebuild=callback,
    )


def wait_for_css(config, timeout: int = 10):
    if config.css_output_absolute.exists():
        success("✓ CSS ready")
        return

    console.print("[yellow]Building CSS...[/yellow]")
    for _ in range(timeout * 2):  # Check every 0.5s
        if config.css_output_absolute.exists():
            success("✓ CSS built")
            return
        time.sleep(0.5)

    error("CSS build timed out")
    raise typer.Exit(1)


def cleanup_files(input_css: Path | None, config, app_path: Path):
    if input_css and input_css.name.startswith("tmp"):
        input_css.unlink(missing_ok=True)

    for wrapper in app_path.parent.glob(f"{app_path.stem}_dev_*.py"):
        wrapper.unlink(missing_ok=True)

    for temp in config.css_output_absolute.parent.glob("tmp*.css"):
        temp.unlink(missing_ok=True)


def show_status(config, port: int, ws_port: int, css_hot: bool, app_file: str):
    table = Table(title="StarUI Development Server", show_header=False)
    table.add_column(style="cyan")
    table.add_column(style="green")

    table.add_row("App", f"http://localhost:{port}")
    table.add_row("File", app_file)
    table.add_row("CSS", str(config.css_output))
    table.add_row("Hot Reload", f"✓ (WebSocket on port {ws_port})" if css_hot else "✗")

    console.print(Panel(table, border_style="green"))


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
    input_css = None

    app_port = resolve_port(port, strict)
    ws_port = find_port(app_port + 1)

    try:
        input_css = prepare_css_input(config)
        ws_server = start_css_websocket(ws_port, manager) if css_hot_reload else None
        start_tailwind(manager, input_css, config, ws_server)
        wait_for_css(config)

        manager.start_uvicorn(
            app_file=app_path,
            port=app_port,
            watch_patterns=["*.py", "*.html"],
            enable_css_hot_reload=css_hot_reload,
            css_ws_port=ws_port,
        )
        success(f"✓ Server running at http://localhost:{app_port}")

        show_status(config, app_port, ws_port, css_hot_reload, app_file)
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
        cleanup_files(input_css, config, app_path)
