from __future__ import annotations

import math
import random
import tkinter as tk
from typing import Dict

from app.beacon.beacon import BeaconModel
from app.camera.camera_model import CameraModel
from app.control.controller import PIDController
from app.scenarios.scenario_manager import ScenarioManager
from app.tracking.tracker import Tracker


class PATGameWindow(tk.Tk):
    """A simple interactive, game-like PAT simulation window."""

    def __init__(self, scenario_name: str = "clean") -> None:
        super().__init__()
        self.title("AI Virtual Camera Tracking System")
        self.geometry("980x700")
        self.configure(bg="#0d1321")
        self.running = False
        self.clock = 0.0
        self.dt = 1.0 / 30.0

        self.scenario = ScenarioManager().get(scenario_name)
        self.camera = CameraModel(width=760, height=520, fov_deg=60.0)
        self.beacon = BeaconModel(position=(0.0, 0.0), velocity=(self.scenario.beacon_speed, 22.0), radius=12.0)
        self.tracker = Tracker()
        self.pan_controller = PIDController(kp=0.35, ki=0.04, kd=0.02, max_output=25.0)
        self.tilt_controller = PIDController(kp=0.35, ki=0.04, kd=0.02, max_output=25.0)

        self.canvas = tk.Canvas(self, width=760, height=520, bg="#111827", highlightthickness=0)
        self.canvas.pack(padx=16, pady=(16, 8), side=tk.TOP)

        controls = tk.Frame(self, bg="#0d1321")
        controls.pack(fill=tk.X, padx=16, pady=(0, 16))

        tk.Button(controls, text="Start", command=self.start).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(controls, text="Pause", command=self.pause).pack(side=tk.LEFT, padx=8)
        tk.Button(controls, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=8)

        label_text = tk.StringVar(value="Scenario: clean")
        tk.Label(controls, textvariable=label_text, fg="white", bg="#0d1321", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=12)
        self.status_var = label_text

        self.metrics_var = tk.StringVar(value="FPS: 0\nTracking Error: 0\nLock: SEARCH")
        tk.Label(self, textvariable=self.metrics_var, fg="#dbeafe", bg="#0d1321", justify=tk.LEFT, anchor="w", font=("Consolas", 10), padx=16).pack(fill=tk.X)

        self.bind("<Escape>", lambda event: self.destroy())
        self.after(40, self.tick)

    def start(self) -> None:
        self.running = True
        self.status_var.set(f"Scenario: {self.scenario.name}")

    def pause(self) -> None:
        self.running = False

    def reset(self) -> None:
        self.running = False
        self.clock = 0.0
        self.beacon.position = (0.0, 0.0)
        self.beacon.velocity = (self.scenario.beacon_speed, 22.0)
        self.camera.pan = 0.0
        self.camera.tilt = 0.0
        self.tracker.state = {"x": 0.0, "y": 0.0, "vx": 0.0, "vy": 0.0, "confidence": 0.0}
        self.canvas.delete("all")
        self.draw_scene()

    def draw_scene(self) -> None:
        self.canvas.delete("all")

        self.canvas.create_rectangle(0, 0, 760, 520, fill="#111827")
        self.canvas.create_line(20, 260, 740, 260, fill="#374151", width=1)
        self.canvas.create_line(380, 20, 380, 500, fill="#374151", width=1)

        bx, by = self.beacon.position
        px, py = self.camera.world_to_image(bx, by)

        self.canvas.create_line(380, 260, px, py, fill="#f59e0b", width=2, dash=(4, 4))
        self.canvas.create_oval(px - self.beacon.radius, py - self.beacon.radius, px + self.beacon.radius, py + self.beacon.radius, fill="#fbbf24", outline="#fef3c7", width=2)
        self.canvas.create_oval(380 - 10, 260 - 10, 380 + 10, 260 + 10, fill="#60a5fa", outline="#dbeafe", width=2)

        cx = 380
        cy = 260
        self.canvas.create_rectangle(cx - 80, cy - 60, cx + 80, cy + 60, outline="#93c5fd", width=2)
        self.canvas.create_text(20, 20, text="AI PAT Tracker", anchor="nw", fill="#e2e8f0", font=("Segoe UI", 12, "bold"))

        predicted_x, predicted_y = self.tracker.predict(self.dt)
        pred_px, pred_py = self.camera.world_to_image(predicted_x, predicted_y)
        self.canvas.create_oval(pred_px - 4, pred_py - 4, pred_px + 4, pred_py + 4, fill="#34d399", outline="#ecfdf5")

        if self.scenario.false_target:
            false_x = 150 + math.sin(self.clock * 1.7) * 90
            false_y = -90 + math.cos(self.clock * 1.5) * 60
            false_px, false_py = self.camera.world_to_image(false_x, false_y)
            self.canvas.create_oval(false_px - 8, false_py - 8, false_px + 8, false_py + 8, fill="#f87171", outline="#fecaca", width=2)

    def tick(self) -> None:
        if self.running:
            self.clock += self.dt
            self.beacon.position = (self.beacon.position[0] + self.beacon.velocity[0] * self.dt, self.beacon.position[1] + self.beacon.velocity[1] * self.dt)
            self.beacon.velocity = (self.beacon.velocity[0] * 0.995, self.beacon.velocity[1] + math.sin(self.clock) * 0.2)

            bx, by = self.beacon.position
            img_x, img_y = self.camera.world_to_image(bx, by)
            error_x = 380 - img_x
            error_y = 260 - img_y
            pan_cmd = self.pan_controller.update(error_x, self.dt)
            tilt_cmd = self.tilt_controller.update(error_y, self.dt)
            self.camera.set_orientation(self.camera.pan + pan_cmd * 0.01, self.camera.tilt + tilt_cmd * 0.01)
            self.tracker.update((img_x, img_y), self.dt)

            tracking_error = math.hypot(error_x, error_y)
            lock_state = "TRACKING" if tracking_error < 80 else "SEARCHING"
            fps = 1.0 / self.dt
            self.metrics_var.set(
                f"FPS: {fps:.1f}\n"
                f"Tracking Error: {tracking_error:.1f}\n"
                f"Lock: {lock_state}\n"
                f"Pan: {self.camera.pan:.2f}  Tilt: {self.camera.tilt:.2f}"
            )

        self.draw_scene()
        self.after(33, self.tick)


def launch_game(scenario_name: str = "clean") -> None:
    window = PATGameWindow(scenario_name)
    window.mainloop()
