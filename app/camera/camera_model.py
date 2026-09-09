from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Tuple


@dataclass
class CameraModel:
    """Simple virtual camera model for PAT simulation."""

    width: int = 800
    height: int = 600
    fov_deg: float = 60.0
    pan: float = 0.0
    tilt: float = 0.0
    max_pan: float = 90.0
    max_tilt: float = 60.0
    frame_rate: float = 30.0

    def world_to_image(self, x: float, y: float) -> Tuple[float, float]:
        """Project a world point into image coordinates."""
        cx = self.width / 2.0
        cy = self.height / 2.0
        scale = self.width / (2.0 * math.tan(math.radians(self.fov_deg / 2.0)))
        px = cx + x * scale
        py = cy - y * scale
        return px, py

    def set_orientation(self, pan: float, tilt: float) -> None:
        self.pan = max(-self.max_pan, min(self.max_pan, pan))
        self.tilt = max(-self.max_tilt, min(self.max_tilt, tilt))

    def get_orientation(self) -> Tuple[float, float]:
        return self.pan, self.tilt
