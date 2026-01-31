import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

sys.path.append(BACKEND_DIR)

from app.main import app  # noqa: E402

__all__ = ["app"]
