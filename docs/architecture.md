# Architecture Overview

The system uses a layered design:

1. Simulation layer
   - Defines environment, beacon motion, camera model, and scenarios.
2. Perception layer
   - Detects and validates candidate beacon positions.
3. Tracking layer
   - Maintains state and prediction logic.
4. Control layer
   - Converts tracking error to pan/tilt commands.
5. Metrics and reporting
   - Logs telemetry and exports summaries.

This structure keeps the UI separate from the core control logic and supports future hardware abstraction.
