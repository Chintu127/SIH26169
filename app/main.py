from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app.beacon.beacon import BeaconModel
from app.camera.camera_model import CameraModel
from app.simulation.pat_simulation import PATSimulation


def main() -> None:
    camera = CameraModel(width=800, height=600, fov_deg=60.0)
    beacon = BeaconModel(position=(0.0, 0.0), velocity=(40.0, 18.0), acceleration=(0.0, 0.0), radius=12.0)
    sim = PATSimulation(camera=camera, beacons=[beacon])

    metrics = sim.run(steps=180)

    output_dir = Path(ROOT) / "reports"
    output_dir.mkdir(exist_ok=True)
    with (output_dir / "metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("Simulation complete.")
    print(f"Generated {len(metrics)} metrics samples in {output_dir / 'metrics.json'}")
    print(f"Final camera pan: {sim.camera.pan:.3f}, tilt: {sim.camera.tilt:.3f}")
    print(f"Final beacon position: {sim.beacons[0].position}")


if __name__ == "__main__":
    main()
