"""Camera discovery helpers."""
from __future__ import annotations

import time
import os
import subprocess

os.environ.setdefault("OPENCV_LOG_LEVEL", "SILENT")

import cv2


if hasattr(cv2, "setLogLevel"):
    cv2.setLogLevel(0)


def camera_backends() -> list[int]:
    """Return OpenCV backends worth trying on this platform."""
    backends = []
    for name in ("CAP_MSMF", "CAP_DSHOW"):
        backend = getattr(cv2, name, None)
        if backend is not None and backend not in backends:
            backends.append(backend)
    return backends


def is_camera_available(index: int, timeout: float = 0.35) -> bool:
    """Check if a camera index can be opened by OpenCV."""
    for backend in camera_backends():
        capture = cv2.VideoCapture(index, backend)
        try:
            if not capture.isOpened():
                continue

            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            capture.set(cv2.CAP_PROP_FPS, 15)
            capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            started = time.monotonic()
            while time.monotonic() - started < timeout:
                ok, frame = capture.read()
                if ok and frame is not None and frame.size:
                    return True
                time.sleep(0.03)

            return True
        finally:
            capture.release()

    return False


def discover_camera_indexes(max_index: int = 8, limit: int = 4) -> list[int]:
    """Find camera indexes that are actually available."""
    found = []
    for index in range(max_index + 1):
        if is_camera_available(index):
            found.append(index)
            if len(found) >= limit:
                break

    return found[:limit]


def discover_camera_names() -> list[str]:
    """Return camera device names reported by Windows."""
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
            "Get-CimInstance Win32_PnPEntity | "
            "Where-Object { $_.PNPClass -in @('Camera','Image') } | "
            "ForEach-Object { $_.Name }"
        ),
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=4,
            check=False,
        )
    except Exception:
        return []

    names = []
    for line in result.stdout.splitlines():
        name = line.strip()
        if name and name not in names:
            names.append(name)
    return names


def discover_camera_devices(max_index: int = 8, limit: int = 4) -> list[tuple[int, str]]:
    """Return available camera indexes paired with readable names."""
    indexes = discover_camera_indexes(max_index=max_index, limit=limit)
    names = discover_camera_names()
    devices: list[tuple[int, str]] = []

    for position, index in enumerate(indexes):
        name = names[position] if position < len(names) else f"Камера {index}"
        devices.append((index, name))

    return devices
