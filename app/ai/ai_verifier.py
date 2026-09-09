from __future__ import annotations

import math
from typing import Iterable, List, Tuple


class AIBeaconVerifier:
    """Small, explainable AI-style verifier for candidate beacon validation."""

    def score_candidate(
        self,
        target_position: Tuple[float, float],
        previous_position: Tuple[float, float],
        estimated_velocity: Tuple[float, float],
        brightness: float,
        history: Iterable[Tuple[float, float]],
    ) -> float:
        hist = list(history)
        if not hist:
            hist = [previous_position]

        displacement = math.hypot(
            target_position[0] - previous_position[0],
            target_position[1] - previous_position[1],
        )
        velocity_mag = math.hypot(estimated_velocity[0], estimated_velocity[1])

        motion_score = min(1.0, displacement / max(1.0, velocity_mag + 1.0))
        brightness_score = min(1.0, max(0.0, brightness))

        if len(hist) >= 2:
            recent = hist[-2:]
            trend = math.hypot(
                recent[-1][0] - recent[0][0],
                recent[-1][1] - recent[0][1],
            )
            temporal_score = min(1.0, trend / max(1.0, displacement + 1.0))
        else:
            temporal_score = 0.5

        score = 0.45 * brightness_score + 0.35 * motion_score + 0.20 * temporal_score
        return max(0.0, min(1.0, score))

    def is_valid_candidate(self, score: float, threshold: float = 0.55) -> bool:
        return score >= threshold
