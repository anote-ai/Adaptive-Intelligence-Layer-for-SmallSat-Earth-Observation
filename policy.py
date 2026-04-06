from __future__ import annotations

from typing import Dict


def choose_mission_mode(power_available_w: float) -> str:
    if power_available_w < 6.0:
        return "low_power"
    if power_available_w < 10.0:
        return "constrained"
    return "nominal"


def recommend_sensing_action(event: Dict[str, float | str], mission_mode: str) -> str:
    label = str(event["event_label"])
    severity = float(event["severity"])

    if mission_mode == "low_power":
        if label == "high_stress":
            return "capture_compact_followup"
        return "defer_noncritical_revisit"

    if label == "high_stress" and severity >= 0.75:
        return "increase_revisit_and_zoom_priority"
    if label in {"high_stress", "moderate_stress"}:
        return "schedule_targeted_followup"
    return "continue_nominal_scan"


def prioritize_downlink(event: Dict[str, float | str], bandwidth_state: str) -> int:
    severity = float(event["severity"])
    confidence = float(event["confidence"])

    score = (severity * 0.7) + (confidence * 0.3)
    if bandwidth_state.lower() in {"low", "constrained"}:
        score += 0.1 if severity >= 0.6 else -0.1

    if score >= 0.8:
        return 1
    if score >= 0.55:
        return 2
    return 3
