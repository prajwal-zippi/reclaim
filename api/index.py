"""Vercel serverless entry point.

Serves the Flask backend (backend/app.py) as serverless functions at /api/*
on the SAME domain as the static site. Set env vars (DATABASE_URL, SECRET_KEY,
...) in the Vercel project dashboard.
"""

import os
import sys

_HERE = os.path.dirname(__file__)
for _p in (os.path.join(_HERE, "..", "backend"), os.path.join(_HERE, "..")):
    _abs = os.path.abspath(_p)
    if _abs not in sys.path:
        sys.path.insert(0, _abs)

try:
    from app import app  # backend/app.py on sys.path
except ModuleNotFoundError:
    from backend.app import app  # repo-root layout

# Vercel's Python runtime serves this WSGI callable named `app`.
__all__ = ["app"]
