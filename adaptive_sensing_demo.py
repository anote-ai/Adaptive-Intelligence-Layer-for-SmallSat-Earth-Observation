from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from onboard_models import LightweightEventModel, TileFeatures
from policy import choose_mission_mode, prioritize_downlink, recommend_sensing_action


def load_tiles(csv_path: Path) -> List[TileFeatures]:
    tiles: List[TileFeatures] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tiles.append(
                TileFeatures(
                    tile_id=row["tile_id"],
                    ndvi=float(row["ndvi"]),
                    ndvi_baseline=float(row["ndvi_baseline"]),
                    soil_moisture=float(row["soil_moisture"]),
                    soil_moisture_baseline=float(row["soil_moisture_baseline"]),
                    et_proxy=float(row["et_proxy"]),
                    cloud_fraction=float(row["cloud_fraction"]),
                    power_available_w=float(row["power_available_w"]),
                    bandwidth_state=row["bandwidth_state"],
                )
            )
    return tiles


def run_simulation(tiles: List[TileFeatures]) -> Dict[str, Any]:
    model = LightweightEventModel()
    outputs: List[Dict[str, Any]] = []

    for tile in tiles:
        event = model.score_event(tile)
        mission_mode = choose_mission_mode(tile.power_available_w)
        sensing_action = recommend_sensing_action(event, mission_mode)
        priority = prioritize_downlink(event, tile.bandwidth_state)

        compact_packet = {
            "tile_id": tile.tile_id,
            "event_label": event["event_label"],
            "severity": event["severity"],
            "confidence": event["confidence"],
            "mission_mode": mission_mode,
            "recommended_action": sensing_action,
            "downlink_priority": priority,
            "reasoning": {
                "ndvi_drop": event["ndvi_drop"],
                "moisture_drop": event["moisture_drop"],
                "et_stress": event["et_stress"],
                "bandwidth_state": tile.bandwidth_state,
                "power_available_w": tile.power_available_w,
            },
        }
        outputs.append(compact_packet)

    outputs.sort(key=lambda x: (x["downlink_priority"], -x["severity"], -x["confidence"]))

    return {
        "system": "AAIL-EO software demonstration",
        "description": "Adaptive sensing and onboard prioritization simulation for regenerative agriculture use cases.",
        "transmit_queue": outputs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AAIL-EO adaptive sensing demo.")
    parser.add_argument("--input", required=True, help="Path to observation CSV input")
    parser.add_argument("--output", required=True, help="Path to JSON output")
    args = parser.parse_args()

    tiles = load_tiles(Path(args.input))
    result = run_simulation(tiles)

    out_path = Path(args.output)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote results to {out_path}")


if __name__ == "__main__":
    main()
