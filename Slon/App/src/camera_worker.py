"""Camera worker thread for capturing video frames."""
from __future__ import annotations

import queue
import threading
import time
import os
from typing import Optional

os.environ.setdefault("OPENCV_LOG_LEVEL", "SILENT")

import cv2
from PySide6.QtGui import QImage

from .camera_discovery import camera_backends
from .config import CameraConfig


if hasattr(cv2, "setLogLevel"):
    cv2.setLogLevel(0)


class CameraWorker:
    """Handles video capture from a single camera in a separate thread."""

    def __init__(self, config: CameraConfig) -> None:
        self.config = config
        self.frames: queue.Queue[QImage] = queue.Queue(maxsize=1)
        self.status = self._status_text("запуск")
        self.is_online = False
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.name = f"CameraWorker-{config.index}"
        self._started = False
        self._reconnect_delay = 2
        self._max_reconnect_delay = 10
        self._config_lock = threading.Lock()
        self._reopen = threading.Event()

    def _status_text(self, text: str) -> str:
        name = self.config.name if self.config.enabled and self.config.name and self.config.name != "Нет камеры" else f"Окно {self.config.slot}"
        return f"{name}: {text}"

    def start(self) -> None:
        """Start the camera worker thread."""
        if not self._started:
            self._thread.start()
            self._started = True

    def stop(self) -> None:
        """Stop the camera worker thread."""
        self._stop.set()
        if self._started:
            self._thread.join(timeout=2)

    def apply_video_settings(self, width: int, height: int, fps: int) -> None:
        """Apply video settings and reopen the capture."""
        with self._config_lock:
            self.config.width = width
            self.config.height = height
            self.config.fps = fps
        self._reopen.set()

    def assign_device(self, device_index: int, device_name: str) -> None:
        """Assign a physical camera to this slot."""
        with self._config_lock:
            self.config.index = device_index
            self.config.name = device_name
            self.config.enabled = device_index >= 0
            self.config.assigned_device = device_index if device_index >= 0 else None
        self._reopen.set()

    def _current_config(self) -> CameraConfig:
        with self._config_lock:
            return CameraConfig(
                index=self.config.index,
                width=self.config.width,
                height=self.config.height,
                fps=self.config.fps,
                slot=self.config.slot,
                enabled=self.config.enabled,
                name=self.config.name,
                assigned_device=self.config.assigned_device,
            )

    def _open_capture(self) -> Optional[cv2.VideoCapture]:
        """Open video capture with a low-latency USB-friendly setup."""
        config = self._current_config()

        for backend in camera_backends():
            try:
                capture = cv2.VideoCapture(config.index, backend)
                if not capture.isOpened():
                    capture.release()
                    continue

                capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, config.width)
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, config.height)
                capture.set(cv2.CAP_PROP_FPS, config.fps)
                capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                capture.set(cv2.CAP_PROP_AUTOFOCUS, 0)
                return capture
            except Exception:
                continue

        return None

    def _process_frame(self, frame) -> Optional[QImage]:
        """Convert an OpenCV frame to a copied QImage."""
        try:
            if frame is None or frame.size == 0:
                return None

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width = rgb_frame.shape[:2]
            bytes_per_line = 3 * width
            return QImage(
                rgb_frame.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_RGB888,
            ).copy()
        except Exception:
            return None

    def _run(self) -> None:
        """Main worker loop."""
        capture: Optional[cv2.VideoCapture] = None
        reconnect_delay = self._reconnect_delay
        error_count = 0
        fps_count = 0
        actual_fps = 0
        last_fps_time = time.monotonic()

        while not self._stop.is_set():
            config = self._current_config()

            if not config.enabled:
                self.is_online = False
                self.status = self._status_text("не назначена")
                time.sleep(2)
                continue

            if capture is not None and self._reopen.is_set():
                capture.release()
                capture = None
                self._reopen.clear()

            if capture is None or not capture.isOpened():
                self.is_online = False
                self.status = self._status_text("подключение")
                capture = self._open_capture()

                if capture is None or not capture.isOpened():
                    self.status = self._status_text("недоступна")
                    if capture is not None:
                        capture.release()
                    capture = None
                    reconnect_delay = min(self._max_reconnect_delay, reconnect_delay + 1)
                    time.sleep(reconnect_delay)
                    continue

                reconnect_delay = self._reconnect_delay
                error_count = 0
                fps_count = 0
                actual_fps = 0
                last_fps_time = time.monotonic()
                continue

            ok, frame = capture.read()
            if not ok or frame is None:
                error_count += 1
                if error_count > 3:
                    self.is_online = False
                    self.status = self._status_text("нет сигнала")
                    capture.release()
                    capture = None
                    reconnect_delay = self._reconnect_delay
                    time.sleep(1)
                    continue

                time.sleep(0.005)
                continue

            error_count = 0
            fps_count += 1
            now = time.monotonic()
            if now - last_fps_time >= 1:
                actual_fps = fps_count
                fps_count = 0
                last_fps_time = now

            image = self._process_frame(frame)
            if image is not None:
                self.is_online = True
                self.status = self._status_text(f"видео ({actual_fps} fps)")

                if self.frames.full():
                    try:
                        self.frames.get_nowait()
                    except queue.Empty:
                        pass

                self.frames.put(image)

        if capture is not None:
            capture.release()
