from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class MetricsLogger:
    """Collect real runtime metrics for scenarios and export them as JSON."""

    def __init__(self) -> None:
        self.samples: List[Dict[str, Any]] = []

    def add(self, record: Dict[str, Any]) -> None:
        self.samples.append(record)

    def summary(self) -> Dict[str, Any]:
        if not self.samples:
            return {
                "simulation_duration": 0.0,
                "avg_tracking_error": 0.0,
                "max_tracking_error": 0.0,
                "fps": 0.0,
                "lock_retention": 0.0,
                "false_lock_rate": 0.0,
            }

        errors = [float(item.get("tracking_error", 0.0)) for item in self.samples]
        fps_values = [float(item.get("fps", 0.0)) for item in self.samples if item.get("fps") is not None]

        summary = {
            "simulation_duration": float(self.samples[-1].get("time", 0.0)),
            "avg_tracking_error": sum(errors) / len(errors),
            "max_tracking_error": max(errors) if errors else 0.0,
            "fps": sum(fps_values) / len(fps_values) if fps_values else 0.0,
            "lock_retention": float(self.samples[-1].get("lock_retention", 0.0)),
            "false_lock_rate": float(self.samples[-1].get("false_lock_rate", 0.0)),
        }
        return summary

    def save(self, path: str | Path) -> None:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8") as handle:
            json.dump({"samples": self.samples, "summary": self.summary()}, handle, indent=2)
