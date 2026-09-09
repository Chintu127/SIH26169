import math

from app.camera.camera_model import CameraModel
from app.beacon.beacon import BeaconModel
from app.tracking.tracker import Tracker
from app.control.controller import PIDController


def test_beacon_motion_updates_position():
    beacon = BeaconModel(position=(100, 100), velocity=(10, 5), radius=8)
    beacon.update(0.5)
    assert abs(beacon.position[0] - 105.0) < 1e-6
    assert abs(beacon.position[1] - 102.5) < 1e-6


def test_camera_projects_world_points():
    camera = CameraModel(width=800, height=600, fov_deg=60.0, pan=0.0, tilt=0.0)
    x, y = camera.world_to_image(0.0, 0.0)
    assert abs(x - 400.0) < 1e-6
    assert abs(y - 300.0) < 1e-6


def test_tracker_updates_from_detection():
    tracker = Tracker()
    tracker.update(detection=(200, 200), dt=0.1)
    assert tracker.state['x'] == 200
    assert tracker.state['y'] == 200


def test_pid_controller_reduces_error():
    pid = PIDController(kp=1.0, ki=0.1, kd=0.0, max_output=10.0)
    command = pid.update(error=5.0, dt=0.1)
    assert command > 0
    assert abs(command) <= 10.0
