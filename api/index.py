"""Vercel serverless entry point.

Serves the Flask backend (backend/app.py) as serverless functions at /api/* on the
SAME domain as the static site. A STATIC `from backend.app import app` import (with
backend/ as a package) lets Vercel's bundler trace and include the backend code — the
earlier sys.path + dynamic import could not be traced, so backend/ was left out of the
function bundle and every request crashed with FUNCTION_INVOCATION_FAILED.

If the import still fails for any reason, we expose a tiny fallback app so /api/health
returns the real traceback as JSON instead of an opaque 500.
"""

import os
import sys
import traceback

# make the repo root importable so `backend` resolves as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from backend.app import app  # static import → Vercel bundles backend/
except Exception:
    _ERR = traceback.format_exc()
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.get("/api/health")
    def _health():
        return jsonify({"ok": False, "import_error": _ERR[-1600:]}), 500

    @app.route("/", defaults={"_path": ""})
    @app.route("/<path:_path>")
    def _catch_all(_path):
        return jsonify({"ok": False, "import_error": _ERR[-1600:]}), 500

# Vercel's Python runtime serves this WSGI callable named `app`.
__all__ = ["app"]
