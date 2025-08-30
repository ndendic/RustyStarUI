"""WebSocket server for CSS hot reload."""

import asyncio
import json
from pathlib import Path

import websockets
from websockets.server import WebSocketServerProtocol


class CSSHotReloadServer:
    """WebSocket server for CSS hot reload notifications."""

    def __init__(self, port: int = 5001):
        self.port = port
        self.clients: set[WebSocketServerProtocol] = set()
        self.server = None

    async def notify_css_update(self, css_path: Path, build_time: float = 0) -> None:
        """Notify all clients about CSS update."""
        if not self.clients:
            return

        message = json.dumps(
            {
                "type": "css-update",
                "path": str(css_path),
                "timestamp": asyncio.get_event_loop().time(),
                "buildTime": build_time,
            }
        )

        disconnected = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
            except Exception:
                disconnected.add(client)

        self.clients -= disconnected

    async def handle_client(
        self, websocket: WebSocketServerProtocol, path: str
    ) -> None:
        """Handle a client WebSocket connection."""
        self.clients.add(websocket)
        try:
            await websocket.send(json.dumps({"type": "connected"}))
            async for _ in websocket:
                pass  # Keep connection alive
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.discard(websocket)

    async def start(self) -> None:
        """Start the WebSocket server."""
        self.server = await websockets.serve(self.handle_client, "localhost", self.port)

    async def stop(self) -> None:
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
