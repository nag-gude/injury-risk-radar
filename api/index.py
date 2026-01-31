import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

sys.path.append(BACKEND_DIR)

from app.main import app as _app  # noqa: E402


async def app(scope, receive, send):
    if scope["type"] in {"http", "websocket"} and scope["path"].startswith("/api"):
        scope = dict(scope)
        scope["path"] = scope["path"][4:] or "/"
    await _app(scope, receive, send)


__all__ = ["app"]
