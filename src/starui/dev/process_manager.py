"""Development process coordination."""

import asyncio
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from rich.console import Console

console = Console()


class ProcessManager:
    def __init__(self):
        self.processes = {}
        self.threads = {}
        self.shutdown_event = threading.Event()

    def start_process(
        self, name: str, cmd: list[str], cwd: Path = None, env: dict = None
    ) -> subprocess.Popen:
        if name in self.processes:
            console.print(f"[yellow]{name} already running[/yellow]")
            return self.processes[name]

        console.print(f"[green]Starting {name}...[/green]")
        process = subprocess.Popen(
            cmd,
            cwd=str(cwd) if cwd else None,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )
        self.processes[name] = process

        thread = threading.Thread(
            target=self._monitor_output, args=(name, process), daemon=True
        )
        thread.start()
        self.threads[f"{name}_monitor"] = thread
        return process

    def _monitor_output(self, name: str, process: subprocess.Popen):
        try:
            while process.poll() is None and not self.shutdown_event.is_set():
                if line := process.stdout.readline():
                    if clean := line.strip():
                        console.print(f"[dim cyan][{name}][/dim cyan] {clean}")
                else:
                    time.sleep(0.1)
        except Exception as e:
            console.print(f"[red]Error monitoring {name}: {e}[/red]")

    def start_uvicorn(
        self,
        app_file: Path,
        port: int,
        watch_patterns: list[str] = None,
        enable_css_hot_reload: bool = True,
    ) -> subprocess.Popen:
        if enable_css_hot_reload:
            wrapper_file = app_file.parent / f"{app_file.stem}_dev.py"
            if not wrapper_file.exists():
                wrapper_file.write_text(f"""from {app_file.stem} import app as original_app
from starui.dev.middleware import CSSHotReloadMiddleware
app = CSSHotReloadMiddleware(original_app)""")
            app_module = f"{wrapper_file.stem}:app"
        else:
            app_module = f"{app_file.stem}:app"

        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            app_module,
            "--reload",
            "--port",
            str(port),
            "--host",
            "localhost",
            "--reload-delay",
            "0.1",
        ]

        patterns = watch_patterns or ["*.py", "*.html"]
        for p in patterns:
            cmd.extend(["--reload-include", p])

        for exclude in [
            "*.css",
            "static/**",
            "**/tmp*",
            "**/__pycache__/**",
            "*_dev.py",
        ]:
            cmd.extend(["--reload-exclude", exclude])

        env = os.environ.copy()
        return self.start_process("uvicorn", cmd, app_file.parent, env=env)

    def start_tailwind_watcher(
        self,
        tailwind_binary: Path,
        input_css: Path,
        output_css: Path,
        project_root: Path,
        on_rebuild: callable = None,
    ) -> subprocess.Popen:
        cmd = [
            str(tailwind_binary),
            "--input",
            str(input_css),
            "--output",
            str(output_css),
            "--watch=always",
            "--cwd",
            str(project_root),
        ]
        process = self.start_process("tailwind", cmd, project_root)

        if on_rebuild:

            def monitor():
                last_mtime = output_css.stat().st_mtime if output_css.exists() else 0
                if last_mtime:
                    on_rebuild(output_css)

                while not self.shutdown_event.is_set():
                    try:
                        if (
                            output_css.exists()
                            and (mtime := output_css.stat().st_mtime) > last_mtime
                        ):
                            last_mtime = mtime
                            on_rebuild(output_css)
                    except Exception:
                        pass
                    time.sleep(0.5)

            thread = threading.Thread(target=monitor, daemon=True)
            thread.start()
            self.threads["tailwind_monitor"] = thread

        return process

    def start_websocket_server(self, websocket_server, loop) -> threading.Thread:
        def run():
            asyncio.set_event_loop(loop)
            loop.run_until_complete(websocket_server.start())
            try:
                while not self.shutdown_event.is_set():
                    loop.run_until_complete(asyncio.sleep(0.1))
            except Exception:
                pass
            finally:
                loop.run_until_complete(websocket_server.stop())

        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        self.threads["websocket"] = thread
        console.print("[green]WebSocket server started on port 5001[/green]")
        return thread

    def is_running(self, name: str) -> bool:
        return name in self.processes and self.processes[name].poll() is None

    def stop_process(self, name: str, timeout: int = 2) -> bool:
        if name not in self.processes:
            return True

        process = self.processes[name]
        try:
            process.terminate()
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=1)
        except Exception:
            pass

        self.processes.pop(name, None)
        return True

    def stop_all(self, timeout: int = 2):
        if self.shutdown_event.is_set():
            return  # Already shutting down

        self.shutdown_event.set()

        # Stop processes in parallel for speed
        for name in list(self.processes):
            self.stop_process(name, timeout)

        # Don't wait for threads, they're daemon threads
        self.processes.clear()
        self.threads.clear()

    def wait_for_any_exit(self):
        while not self.shutdown_event.is_set():
            dead = []
            for name, proc in self.processes.items():
                if proc.poll() is not None:
                    if name == "tailwind" and proc.returncode == 0:
                        continue
                    dead.append(name)

            if dead:
                for name in dead:
                    console.print(f"[red]{name} died unexpectedly[/red]")
                    del self.processes[name]
                if "uvicorn" in dead:
                    break

            time.sleep(0.5)
