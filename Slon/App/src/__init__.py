"""Slon - Video monitoring application."""
import os

os.environ.setdefault("OPENCV_LOG_LEVEL", "SILENT")

from .main_window import main

__all__ = ["main"]
