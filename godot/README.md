# Godot vertical slice shell

This directory contains the first Godot 4 presentation shell for Postcard City.

## Current scope

- Godot scene tree and application shell.
- Demo simulation session with deterministic placeholder state.
- Metric cards.
- Event log.
- Timeline control.
- Two demo interventions.
- Before/after postcard comparison.

The demo session is intentionally local to Godot and does not yet call the Python simulation. The next integration step should replace `SimulationSession`'s placeholder methods with a versioned JSON gateway while keeping the scene and UI contracts unchanged.

## Run

Open `godot/project.godot` in Godot 4.x and run the project.
