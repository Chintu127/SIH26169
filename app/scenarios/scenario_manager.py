from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class ScenarioConfig:
    name: str
    beacon_speed: float
    noise: float
    vibration: float
    turbulence: float
    camera_motion: float
    false_target: bool = False
    target_count: int = 1


class ScenarioManager:
    """Defines reusable simulation scenarios with deterministic settings."""

    def __init__(self) -> None:
        self.scenarios: Dict[str, ScenarioConfig] = {
            "clean": ScenarioConfig("clean", 40.0, 0.05, 0.05, 0.05, 0.05),
            "high_noise": ScenarioConfig("high_noise", 42.0, 0.45, 0.10, 0.10, 0.10),
            "vibration": ScenarioConfig("vibration", 48.0, 0.15, 0.65, 0.10, 0.20),
            "camera_motion": ScenarioConfig("camera_motion", 38.0, 0.10, 0.20, 0.15, 0.70),
            "fast_target": ScenarioConfig("fast_target", 90.0, 0.10, 0.10, 0.10, 0.10),
            "false_target": ScenarioConfig("false_target", 40.0, 0.12, 0.10, 0.08, 0.10, True),
            "multi_target": ScenarioConfig("multi_target", 34.0, 0.18, 0.14, 0.12, 0.12, target_count=3),
            "combined": ScenarioConfig("combined", 55.0, 0.35, 0.60, 0.40, 0.55, target_count=2),
        }

    def get(self, name: str) -> ScenarioConfig:
        key = name.lower().replace(" ", "_")
        if key not in self.scenarios:
            raise ValueError(f"Unknown scenario: {name}")
        return self.scenarios[key]

    def list_names(self) -> list[str]:
        return list(self.scenarios.keys())
