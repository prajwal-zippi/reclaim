"""Vercel serverless entry point.

Serves the Flask backend (backend/app.py) as serverless functions at /api/*
on the SAME domain as the static site — no CORS, no separate service, and no
Render-style sleep. Set env vars (DATABASE_URL, SECRET_KEY, ...) in the Vercel
project dashboard.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app import app  # noqa: E402,F401  (Vercel's Python runtime serves this WSGI `app`)
