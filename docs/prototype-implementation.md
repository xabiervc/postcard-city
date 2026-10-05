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
- Aurora Leisure decision options.
- Delayed financing warning and housing protest events.
- Executive reporting.
- Scenario content validation.
- Reproducibility tests.

## Run locally
```bash
python -m pip install -e .[dev]
pytest
python -m postcard_city.cli --months 12 --decision renegotiate
python tools/validate_content.py
```

## Deliberate limitations
This is not production gameplay. It has no final engine, visual map, full political simulation, media simulation, procedural generation, persistence layer, or final balance. The purpose is to validate deterministic causal relationships before expanding the scope.

## Next technical steps
1. Add explicit state transition traces.
2. Add save/load serialization and migration identifiers.
3. Replace hard-coded slice data with schema-backed content loading.
4. Add election and media event contracts.
5. Add property-based invariants and scenario solvability checks.
6. Build a thin interactive presentation layer.
