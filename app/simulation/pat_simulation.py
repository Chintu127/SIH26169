from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List

from app.ai.ai_verifier import AIBeaconVerifier
from app.beacon.beacon import BeaconModel
from app.camera.camera_model import CameraModel
from app.control.controller import PIDController
from app.disturbances.disturbance_engine import DisturbanceConfig, DisturbanceEngine
from app.tracking.tracker import Tracker


@dataclass
class PATSimulation:
    """Closed-loop virtual PAT simulation with multi-target support, disturbance injection, and AI verification."""

    camera: CameraModel = None
    beacons: List[BeaconModel] = field(default_factory=list)
    tracker: Tracker = field(default_factory=Tracker)
    pan_controller: PIDController = field(default_factory=PIDController)
    tilt_controller: PIDController = field(default_factory=PIDController)
    disturbance: DisturbanceEngine = field(default_factory=lambda: DisturbanceEngine(DisturbanceConfig()))
    ai_verifier: AIBeaconVerifier = field(default_factory=AIBeaconVerifier)
    time: float = 0.0
    dt: float = 1.0 / 30.0
    metrics: List[dict] = field(default_factory=list)

    def __post_init__(self):
        if self.camera is None:
            self.camera = CameraModel()
        if not self.beacons:
            self.beacons = [
                BeaconModel(position=(0.0, 0.0), velocity=(40.0, 20.0), radius=12.0),
                BeaconModel(position=(150.0, -80.0), velocity=(30.0, -15.0), radius=10.0, intensity=0.65),
            ]

    def step(self) -> dict:
        self.time += self.dt
        for beacon in self.beacons:
            beacon.update(self.dt)

        primary = self.beacons[0]
        x_raw, y_raw = primary.position
        x_noisy, y_noisy = self.disturbance.apply_position_jitter((x_raw, y_raw), self.time)
        x_img, y_img = self.camera.world_to_image(x_noisy, y_noisy)

        cx = self.camera.width / 2.0
        cy = self.camera.height / 2.0
        pan_error = cx - x_img
        tilt_error = cy - y_img

        pan_command = self.pan_controller.update(pan_error, self.dt)
        tilt_command = self.tilt_controller.update(tilt_error, self.dt)

        self.camera.set_orientation(self.camera.pan + pan_command * 0.01, self.camera.tilt + tilt_command * 0.01)
        self.tracker.update((x_img, y_img), self.dt)

        ai_score = self.ai_verifier.score_candidate(
            target_position=(x_img, y_img),
            previous_position=self.tracker.last_detection or (x_img, y_img),
            estimated_velocity=(self.tracker.state["vx"], self.tracker.state["vy"]),
            brightness=primary.intensity,
            history=[(x_img, y_img)],
        )

        metric = {
            "time": self.time,
            "beacon_x": primary.position[0],
            "beacon_y": primary.position[1],
            "camera_pan": self.camera.pan,
            "camera_tilt": self.camera.tilt,
            "target_x_image": x_img,
            "target_y_image": y_img,
            "pan_error": pan_error,
            "tilt_error": tilt_error,
            "tracking_confidence": self.tracker.state["confidence"],
            "ai_score": ai_score,
            "candidate_valid": self.ai_verifier.is_valid_candidate(ai_score),
        }
        self.metrics.append(metric)
        return metric

    def run(self, steps: int = 180) -> List[dict]:
        for _ in range(steps):
            self.step()
        return self.metrics
