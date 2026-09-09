from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk

from app.ai.ai_verifier import AIBeaconVerifier
from app.disturbances.disturbance_engine import DisturbanceConfig, DisturbanceEngine
from app.scenarios.scenario_manager import ScenarioManager


class PATDashboard(tk.Tk):
    """Polished dashboard with controls and live telemetry."""

    def __init__(self) -> None:
        super().__init__()
        self.title("FSOC PAT Dashboard")
        self.geometry("1200x780")
        self.configure(bg="#0f172a")

        self.scenario_manager = ScenarioManager()
        self.ai_verifier = AIBeaconVerifier()
        self.disturbance = DisturbanceEngine(DisturbanceConfig())

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        sim_frame = tk.Frame(self.notebook, bg="#0f172a")
        self.notebook.add(sim_frame, text="Simulation")

        left = tk.Frame(sim_frame, bg="#0f172a", padx=12, pady=12)
        left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left, text="Scenario", bg="#0f172a", fg="#e2e8f0", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.scenario_var = tk.StringVar(value="clean")
        combo = ttk.Combobox(left, textvariable=self.scenario_var, values=self.scenario_manager.list_names(), state="readonly")
        combo.pack(fill=tk.X, pady=(0, 10))

        tk.Label(left, text="Disturbance Controls", bg="#0f172a", fg="#e2e8f0", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.noise_var = tk.DoubleVar(value=0.15)
        self.vibration_var = tk.DoubleVar(value=0.20)
        self.turbulence_var = tk.DoubleVar(value=0.10)
        self.camera_motion_var = tk.DoubleVar(value=0.12)

        for label, var in [
            ("Noise", self.noise_var),
            ("Vibration", self.vibration_var),
            ("Turbulence", self.turbulence_var),
            ("Camera Motion", self.camera_motion_var),
        ]:
            row = tk.Frame(left, bg="#0f172a")
            row.pack(fill=tk.X, pady=4)
            tk.Label(row, text=label, width=18, fg="#e2e8f0", bg="#0f172a").pack(side=tk.LEFT)
            tk.Scale(row, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL, variable=var, length=180, bg="#0f172a", fg="#e2e8f0").pack(side=tk.RIGHT)

        controls = tk.Frame(left, bg="#0f172a")
        controls.pack(fill=tk.X, pady=(16, 0))
        tk.Button(controls, text="Start Demo", command=self.start_demo, width=16, bg="#22c55e", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(controls, text="Generate Report", command=self.export_report, width=16, bg="#3b82f6", fg="white", relief=tk.FLAT).pack(side=tk.LEFT)

        metrics_frame = tk.Frame(sim_frame, bg="#0f172a")
        metrics_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.metrics_text = tk.Text(metrics_frame, height=26, width=64, bg="#111827", fg="#e2e8f0", font=("Consolas", 10))
        self.metrics_text.pack(fill=tk.BOTH, expand=True)

        self.metrics_text.insert(tk.END, "System ready\n")

    def start_demo(self) -> None:
        scenario = self.scenario_manager.get(self.scenario_var.get())
        line = (
            f"Scenario: {scenario.name}\n"
            f"Target count: {scenario.target_count}\n"
            f"Noise: {self.noise_var.get():.2f}\n"
            f"Vibration: {self.vibration_var.get():.2f}\n"
            f"Turbulence: {self.turbulence_var.get():.2f}\n"
            f"Camera Motion: {self.camera_motion_var.get():.2f}\n"
            f"AI Verification: {self.ai_verifier.is_valid_candidate(0.82)}\n\n"
        )
        self.metrics_text.insert(tk.END, line)

    def export_report(self) -> None:
        export_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(export_dir, exist_ok=True)
        report_path = os.path.join(export_dir, "dashboard_summary.txt")
        with open(report_path, "w", encoding="utf-8") as handle:
            handle.write("FSOC PAT Dashboard Summary\n")
            handle.write(f"Scenario: {self.scenario_var.get()}\n")
            handle.write(f"Noise: {self.noise_var.get():.2f}\n")
            handle.write(f"Vibration: {self.vibration_var.get():.2f}\n")
            handle.write(f"Turbulence: {self.turbulence_var.get():.2f}\n")
            handle.write(f"Camera Motion: {self.camera_motion_var.get():.2f}\n")
        self.metrics_text.insert(tk.END, f"Report saved to {report_path}\n")


def launch_dashboard() -> None:
    window = PATDashboard()
    window.mainloop()
