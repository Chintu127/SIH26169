from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Tuple


@dataclass
class DisturbanceConfig:
    noise: float = 0.0
    vibration: float = 0.0
    turbulence: float = 0.0
    camera_motion: float = 0.0
    blur: float = 0.0
    seed: int = 7


class DisturbanceEngine:
    """Configurable disturbance layer for image noise, vibration, and optical turbulence."""

    def __init__(self, config: DisturbanceConfig | None = None) -> None:
        self.config = config or DisturbanceConfig()
        random.seed(self.config.seed)

    def apply_noise(self, value: float, scale: float = 1.0) -> float:
        return value + (random.random() - 0.5) * 2.0 * self.config.noise * scale

    def apply_vibration(self, point: Tuple[float, float]) -> Tuple[float, float]:
        x, y = point
        vib_x = (random.random() - 0.5) * 2.0 * self.config.vibration * 25.0
        vib_y = (random.random() - 0.5) * 2.0 * self.config.vibration * 25.0
        return x + vib_x, y + vib_y

    def apply_turbulence(self, point: Tuple[float, float], t: float) -> Tuple[float, float]:
        x, y = point
        offset_x = math.sin(t * 1.7 + 0.8) * self.config.turbulence * 15.0
        offset_y = math.cos(t * 1.9 + 1.1) * self.config.turbulence * 15.0
        return x + offset_x, y + offset_y

    def apply_camera_motion(self, point: Tuple[float, float], t: float) -> Tuple[float, float]:
        x, y = point
        shift_x = math.sin(t * 2.4) * self.config.camera_motion * 20.0
        shift_y = math.cos(t * 1.8) * self.config.camera_motion * 18.0
        return x + shift_x, y + shift_y

    def apply_position_jitter(self, point: Tuple[float, float], t: float) -> Tuple[float, float]:
        point = self.apply_vibration(point)
        point = self.apply_turbulence(point, t)
        point = self.apply_camera_motion(point, t)
        return point
