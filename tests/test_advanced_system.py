from app.ai.ai_verifier import AIBeaconVerifier
from app.disturbances.disturbance_engine import DisturbanceConfig, DisturbanceEngine
from app.scenarios.scenario_manager import ScenarioManager


def test_disturbance_engine_changes_position():
    engine = DisturbanceEngine(DisturbanceConfig(noise=0.3, vibration=0.5, turbulence=0.4, camera_motion=0.2))
    result = engine.apply_position_jitter((100.0, 80.0), 0.1)
    assert len(result) == 2
    assert result[0] != 100.0 or result[1] != 80.0


def test_ai_verifier_confirms_expected_target():
    verifier = AIBeaconVerifier()
    score = verifier.score_candidate(
        target_position=(120.0, 90.0),
        previous_position=(100.0, 80.0),
        estimated_velocity=(20.0, 10.0),
        brightness=0.9,
        history=[(100.0, 80.0), (110.0, 85.0)],
    )
    assert score > 0.5
    assert verifier.is_valid_candidate(score) is True


def test_scenario_manager_exposes_multiple_targets():
    manager = ScenarioManager()
    scenario = manager.get("multi_target")
    assert scenario.name == "multi_target"
    assert scenario.target_count == 3
