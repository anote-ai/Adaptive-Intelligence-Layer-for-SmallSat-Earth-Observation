from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class TileFeatures:
    tile_id: str
    ndvi: float
    ndvi_baseline: float
    soil_moisture: float
    soil_moisture_baseline: float
    et_proxy: float
    cloud_fraction: float
    power_available_w: float
    bandwidth_state: str


class LightweightEventModel:
    """A lightweight scoring model representing compressed onboard inference.

    This class uses simple, interpretable rules to simulate what a compact onboard
    model could do after ingesting preprocessed features from remote sensing data.
    """

    def score_event(self, tile: TileFeatures) -> Dict[str, float | str]:
        ndvi_drop = max(0.0, tile.ndvi_baseline - tile.ndvi)
        moisture_drop = max(0.0, tile.soil_moisture_baseline - tile.soil_moisture)
        et_stress = max(0.0, tile.et_proxy)
        cloud_penalty = min(0.5, tile.cloud_fraction)

        raw_score = (
            0.45 * ndvi_drop
            + 0.35 * moisture_drop
            + 0.20 * et_stress
            - 0.15 * cloud_penalty
        )
        severity = max(0.0, min(1.0, raw_score))

        if severity >= 0.65:
            label = "high_stress"
        elif severity >= 0.35:
            label = "moderate_stress"
        else:
            label = "nominal"

        confidence = max(0.1, min(0.99, 1.0 - cloud_penalty))

        return {
            "event_label": label,
            "severity": round(severity, 3),
            "confidence": round(confidence, 3),
            "ndvi_drop": round(ndvi_drop, 3),
            "moisture_drop": round(moisture_drop, 3),
            "et_stress": round(et_stress, 3),
        }
