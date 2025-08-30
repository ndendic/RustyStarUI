"""ASGI middleware for CSS hot reload injection."""

from collections.abc import Awaitable, Callable
from typing import Any


class CSSHotReloadMiddleware:
    """Injects CSS hot reload script into HTML responses."""

    SCRIPT = b"""<script>
(()=>{
if(!['localhost','127.0.0.1'].includes(location.hostname))return;
const ws=new WebSocket('ws://localhost:5001/css-hot-reload');
ws.onmessage=e=>{
const m=JSON.parse(e.data);
if(m.type==='css-update')[...document.querySelectorAll('link[href*="starui.css"]')].forEach(l=>{
const n=l.cloneNode();n.href=l.href.split('?')[0]+'?t='+Date.now();
n.onload=()=>l.remove();l.after(n);
console.log(`[CSS] Updated in ${(m.buildTime||0).toFixed(2)}s`);
})};
ws.onopen=()=>console.log('[CSS] Hot reload connected');
ws.onclose=()=>setTimeout(()=>location.reload(),1000);
})()
</script>"""

    def __init__(
        self, app: Callable[[dict[str, Any], Callable, Callable], Awaitable[None]]
    ):
        self.app = app

    async def __call__(
        self,
        scope: dict[str, Any],
        receive: Callable[[], Awaitable[dict[str, Any]]],
        send: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Buffer response to potentially modify HTML
        response_started = False
        response_body = bytearray()
        headers: list[tuple[bytes, bytes]] = []
        status_code = 200

        async def send_wrapper(message: dict[str, Any]) -> None:
            nonlocal response_started, response_body, headers, status_code

            if message["type"] == "http.response.start":
                response_started = True
                headers = message.get("headers", [])
                status_code = message.get("status", 200)
                return  # Don't send yet, buffer it

            elif message["type"] == "http.response.body":
                body = message.get("body", b"")
                if body:
                    response_body.extend(body)

                # If this is the last chunk
                if not message.get("more_body", False):
                    # Check if this is an HTML response
                    content_type = None
                    for name, value in headers:
                        if name.lower() == b"content-type":
                            content_type = value.decode(
                                "utf-8", errors="ignore"
                            ).lower()
                            break

                    if content_type and "text/html" in content_type:
                        if b"</head>" in response_body:
                            response_body = response_body.replace(
                                b"</head>", self.SCRIPT + b"</head>"
                            )
                        elif b"</body>" in response_body:
                            response_body = response_body.replace(
                                b"</body>", self.SCRIPT + b"</body>"
                            )
                        else:
                            response_body += self.SCRIPT

                        # Update content-length if present
                        new_headers = []
                        for name, value in headers:
                            if name.lower() == b"content-length":
                                new_headers.append(
                                    (name, str(len(response_body)).encode())
                                )
                            else:
                                new_headers.append((name, value))
                        headers = new_headers

                    # Send the buffered response
                    await send(
                        {
                            "type": "http.response.start",
                            "status": status_code,
                            "headers": headers,
                        }
                    )
                    await send(
                        {
                            "type": "http.response.body",
                            "body": bytes(response_body),
                            "more_body": False,
                        }
                    )
                    return

            # For other message types, pass through
            await send(message)

        await self.app(scope, receive, send_wrapper)
