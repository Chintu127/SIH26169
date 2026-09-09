# AI Virtual Camera Tracking System for FSOC PAT Simulation

This project is a lightweight, locally runnable virtual Pointing, Acquisition and Tracking (PAT) simulation for the SIH 2026 problem statement on AI-based virtual camera tracking for coarse alignment of mobile free-space optical communication terminals.

## Features

- Virtual environment with moving beacon
- Virtual camera with configurable field of view and orientation
- Closed-loop pan/tilt tracking
- Classical tracking state estimator
- Scenario-based simulation runner
- Metrics collection and export
- Python-only, offline execution

## Project structure

- app/: core simulation logic
- tests/: verification tests
- reports/: output data and summaries

## Quick start

1. Install dependencies:
   python -m pip install -r requirements.txt
2. Run the demo:
   python app/main.py
3. Run tests:
   python -m pytest tests/test_core.py

## Notes

This is a working MVP designed to provide a demonstrable closed-loop tracking loop and a foundation for future AI, disturbance, and UI improvements.
