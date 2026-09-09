from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple


@dataclass
class Tracker:
    """Minimal tracker that holds current estimate and predicted state."""

    state: Dict[str, float] = field(default_factory=lambda: {"x": 0.0, "y": 0.0, "vx": 0.0, "vy": 0.0, "confidence": 0.0})
    last_detection: Optional[Tuple[float, float]] = None

    def update(self, detection: Tuple[float, float], dt: float = 0.016) -> None:
        x, y = detection
        prev_x = self.state["x"]
        prev_y = self.state["y"]
        self.state["vx"] = (x - prev_x) / max(dt, 1e-6)
        self.state["vy"] = (y - prev_y) / max(dt, 1e-6)
        self.state["x"] = x
        self.state["y"] = y
        self.state["confidence"] = 1.0
        self.last_detection = detection

    def predict(self, dt: float = 0.016) -> Tuple[float, float]:
        return self.state["x"] + self.state["vx"] * dt, self.state["y"] + self.state["vy"] * dt
