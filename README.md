# Anote AAIL-EO Supporting Software Package

This repository provides a lightweight, reviewable software demonstration of the key capabilities behind the **Anote Adaptive Intelligence Layer for SmallSat Earth Observation (AAIL-EO)** submission.

## Purpose
This package is intended to support Phase 1 technical evaluation. It demonstrates how an adaptive onboard processing pipeline can:

1. ingest observation tiles with vegetation and moisture indicators,
2. detect potential agricultural stress events,
3. score the severity and confidence of those events,
4. decide whether to continue nominal sensing or adapt sensing behavior,
5. prioritize only the highest-value observations for downlink.

This is a software demonstration rather than a flight-ready satellite implementation. It is structured to make the technical logic easy to inspect and run.

## Key Capabilities Demonstrated
- **Onboard event detection** using lightweight anomaly scoring from NDVI, soil moisture, and evapotranspiration proxy inputs.
- **Adaptive sensing policy** that changes sensing priority and revisit behavior based on detected conditions.
- **Bandwidth-aware downlink prioritization** that sends compact event summaries instead of all raw observations.
- **Resource-aware operation modes** that simulate decisions under reduced power and limited compute.
- **Clear, inspectable architecture** suitable for Phase 1 technical review.

## Repository Contents
- `adaptive_sensing_demo.py` — main end-to-end simulation.
- `onboard_models.py` — lightweight onboard anomaly and event scoring logic.
- `policy.py` — adaptive sensing and downlink prioritization policy.
- `sample_observations.csv` — sample inputs representing observation tiles.
- `sample_output.json` — example prioritized outputs from a run.
- `architecture_notes.md` — mapping from software components to the proposed SmallSat concept.
- `requirements.txt` — minimal dependencies.

## How to Run
```bash
python adaptive_sensing_demo.py --input sample_observations.csv --output run_output.json
```

## Notes for Judges
This package intentionally avoids proprietary implementation details while preserving enough technical clarity to evaluate the core concept. The current demonstration uses compact tabular features as stand-ins for onboard preprocessed products derived from NASA datasets such as MODIS vegetation indices, SMAP soil moisture, and ECOSTRESS evapotranspiration products.

## Expected Output
The script outputs a JSON file containing:
- event detections,
- severity and confidence scores,
- sensing action recommendation,
- downlink priority ranking,
- mission mode justification.

## Suggested Review Lens
Judges may evaluate this package by asking:
- Does the logic demonstrate adaptive sensing rather than static sensing?
- Does the software show credible onboard processing and prioritization behavior?
- Does the system behave differently under constrained conditions?
- Is the architecture consistent with the Phase 1 paper?
