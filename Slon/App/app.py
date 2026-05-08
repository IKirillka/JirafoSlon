"""Слон - видеомониторинг с 4 камерами"""
import os

os.environ.setdefault("OPENCV_LOG_LEVEL", "SILENT")

from src.main_window import main


if __name__ == "__main__":
    main()
