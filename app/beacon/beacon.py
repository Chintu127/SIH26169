from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class BeaconModel:
    """Simple optical beacon model with position and velocity."""

    position: Tuple[float, float] = (0.0, 0.0)
    velocity: Tuple[float, float] = (0.0, 0.0)
    acceleration: Tuple[float, float] = (0.0, 0.0)
    radius: float = 10.0
    intensity: float = 1.0
    active: bool = True
    history: list[Tuple[float, float]] = field(default_factory=list)

    def update(self, dt: float) -> None:
        if not self.active:
            return
        vx, vy = self.velocity
        ax, ay = self.acceleration
        x, y = self.position
        x += (vx * dt) + (0.5 * ax * dt * dt)
        y += (vy * dt) + (0.5 * ay * dt * dt)
        self.velocity = (vx + ax * dt, vy + ay * dt)
        self.position = (x, y)
        self.history.append((x, y))

    def set_trajectory(self, position: Tuple[float, float], velocity: Tuple[float, float]) -> None:
        self.position = position
        self.velocity = velocity
