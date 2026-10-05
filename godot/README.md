# Godot playable demo

This directory contains the first local playable demo for Postcard City.

## Demo loop

1. Read the objective and current metrics.
2. Select and confirm one of two interventions.
3. Advance months up to the twelve-month slice.
4. Receive a hospital staffing crisis at month four.
5. Read three perspective-based testimonies.
6. Compare the initial and final postcards.
7. Reach a success or failure message based on livability thresholds.

The backend is still a deterministic local Godot demo state. It is intentionally not presented as the authoritative Python simulation yet. The next integration step is a versioned JSON gateway so the same scene/UI contract can consume real `RegionState`, events, and traces.

## Run

Open `godot/project.godot` in Godot 4.x and run the project.
