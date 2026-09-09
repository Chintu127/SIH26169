from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PIDController:
    """Simple PID controller for pan/tilt tracking."""

    kp: float = 0.5
    ki: float = 0.05
    kd: float = 0.02
    max_output: float = 30.0
    integral: float = 0.0
    prev_error: float = 0.0

    def update(self, error: float, dt: float) -> float:
        self.integral += error * dt
        derivative = (error - self.prev_error) / max(dt, 1e-6)
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return max(-self.max_output, min(self.max_output, output))
