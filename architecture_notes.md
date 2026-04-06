# Architecture Notes

## Conceptual Mapping
This software package maps directly to the AAIL-EO mission concept described in the paper.

- `sample_observations.csv` represents compact onboard features derived from satellite sensing.
- `onboard_models.py` represents lightweight onboard inference running on a constrained compute stack.
- `policy.py` represents the adaptive policy engine that selects sensing and downlink behavior.
- `adaptive_sensing_demo.py` ties the full loop together: observe, infer, decide, prioritize.

## What This Demonstrates
This package is designed to demonstrate the minimum key capabilities needed for Phase 1 review:
1. event detection from land-observation features,
2. adaptive mission behavior based on detected conditions,
3. downlink prioritization under constrained bandwidth,
4. behavior change under constrained power.

## What Is Abstracted
This package does not attempt to implement:
- flight-qualified embedded software,
- direct sensor drivers,
- radiation fault tolerance,
- command and telemetry interfaces,
- complete orbital simulation.

Those elements would be addressed in later prototype phases.
