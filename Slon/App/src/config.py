"""Configuration and constants for the application."""
from dataclasses import dataclass
from typing import Optional


ADMIN_PASSWORD = "0098"


@dataclass
class CameraConfig:
    """Camera configuration parameters."""
    index: int
    width: int
    height: int
    fps: int
    slot: int = 1
    enabled: bool = True
    name: str = ""
    assigned_device: Optional[int] = None
