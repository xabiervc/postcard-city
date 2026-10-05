# Prototype Implementation

## Purpose
This prototype is the first executable proof of the Postcard City simulation contract. It is intentionally small and engine-agnostic.

## Implemented
- Monthly deterministic simulation.
- Seeded state creation.
- Aggregate districts.
- Tourism growth and tax revenue.
- Housing conversion and rent pressure.
- Worker accessibility proxy.
- Healthcare staffing pressure.
- Transport reliability.
- Budget updates.
- Aurora Leisure decision options with explicit scheduling.
- Causal transition traces for player-readable debugging.
- Delayed financing warning and housing protest events.
- Executive and causal reporting.
- Scenario content validation.
- Reproducibility and trace tests.

## Run locally
```bash
python -m pip install -e ".[dev]"
pytest
python -m postcard_city.cli --months 12 --decision renegotiate --show-trace --trace-limit 20
python tools/validate_content.py
```

## Deliberate limitations
This is not production gameplay. It has no final engine, visual map, full political simulation, media simulation, procedural generation, persistence layer, or final balance. The current slice data is still constructed in Python and will be moved behind content loading in the next iteration.

## Next technical steps
1. Load initial state and decision definitions from validated scenario content.
2. Add save/load serialization and migration identifiers.
3. Add election and media event contracts.
4. Add property-based invariants and scenario solvability checks.
5. Build a thin interactive presentation layer.
6. Profile simulation and UI response under the slice's maximum state.
