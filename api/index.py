"""
Vercel Serverless Function entrypoint for Savitha Canteen Flask Backend.
"""
import os
import sys

# Ensure root directory is in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app import app

# Vercel WSGI entrypoint
app.debug = False