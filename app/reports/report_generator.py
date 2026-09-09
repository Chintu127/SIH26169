from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class ReportGenerator:
    """Generate a simple HTML summary report from simulation metrics."""

    def __init__(self, output_dir: str | Path = "reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, metrics: List[Dict[str, Any]], scenario_name: str = "clean") -> str:
        if not metrics:
            return ""

        summary = {
            "scenario": scenario_name,
            "samples": len(metrics),
            "final_pan": metrics[-1].get("camera_pan", 0.0),
            "final_tilt": metrics[-1].get("camera_tilt", 0.0),
            "avg_tracking_error": sum(abs(float(item.get("pan_error", 0.0))) for item in metrics) / len(metrics),
            "max_tracking_error": max(abs(float(item.get("pan_error", 0.0))) for item in metrics),
        }

        html = f"""
        <html>
          <head>
            <title>FSOC PAT Simulation Report</title>
            <style>
              body {{ font-family: Arial; background: #0f172a; color: #e2e8f0; margin: 32px; }}
              .card {{ background: #111827; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 16px; }}
              .metric {{ display: inline-block; margin-right: 20px; padding: 10px 12px; background: #1e293b; border-radius: 8px; }}
            </style>
          </head>
          <body>
            <h1>FSOC PAT Simulation Report</h1>
            <div class="card">
              <h2>Scenario: {scenario_name}</h2>
              <div class="metric">Samples: {summary['samples']}</div>
              <div class="metric">Final Pan: {summary['final_pan']:.2f}</div>
              <div class="metric">Final Tilt: {summary['final_tilt']:.2f}</div>
              <div class="metric">Average Tracking Error: {summary['avg_tracking_error']:.2f}</div>
              <div class="metric">Max Tracking Error: {summary['max_tracking_error']:.2f}</div>
            </div>
            <div class="card">
              <h3>Execution Summary</h3>
              <p>This report was generated from live simulation metrics for the configured PAT scenario.</p>
              <p>It reflects actual execution data captured during the run and is intended for documentation and evaluation reporting.</p>
            </div>
          </body>
        </html>
        """

        path = self.output_dir / "summary_report.html"
        path.write_text(html, encoding="utf-8")
        return str(path)
