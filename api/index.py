"""Vercel serverless entry point.

Serves the Flask backend (backend/app.py) as serverless functions at /api/* on the
SAME domain as the static site. A STATIC `from backend.app import app` import (with
backend/ as a package) lets Vercel's bundler trace and include the backend code.

Dependencies install from api/requirements.txt (the @vercel/python builder looks for
requirements next to the entrypoint). If the import still fails for ANY reason —
including missing deps — we expose a dependency-free WSGI app so /api/health returns
the real traceback as JSON instead of an opaque FUNCTION_INVOCATION_FAILED.
"""

import os
import sys

# make the repo root importable so `backend` resolves as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.app import app  # static import → Vercel bundles backend/
except Exception:
    import json
    import traceback

    _ERR = traceback.format_exc()

    def app(environ, start_response):  # minimal WSGI, needs no third-party deps
        start_response("500 Internal Server Error", [("Content-Type", "application/json")])
        return [json.dumps({"ok": False, "import_error": _ERR[-1800:]}).encode()]

__all__ = ["app"]
