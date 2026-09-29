"""
Root entrypoint for running `python app.py` in the terminal.
Exports the Flask `app` instance for WSGI / Gunicorn / Vercel compatibility.
"""
import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app import app
from run import main

if __name__ == "__main__":
    main()
