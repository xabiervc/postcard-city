# Prototype Implementation

## Purpose
This prototype is the first executable proof of the Postcard City simulation contract. It is intentionally small and engine-agnostic.

## Implemented
- Monthly deterministic simulation driven by validated scenario content.
- Scenario content is the single source of truth: region, initial state, parameters, project profiles, decisions with effects, and events.
- JSON Schema (`schemas/scenario.schema.json`) plus semantic validation (`scenario.py`).
- Aggregate districts, tourism growth and tax revenue.
- Housing conversion and rent pressure.
- Worker accessibility feeding healthcare staffing, with a trust and support penalty below a threshold.
- Transport reliability and budget.
- Aurora Leisure decision (approve, reject, renegotiate, audit), resolvable once, scheduled by month.
- Data-defined events with simple conditions.
- Causal transition traces for player-readable debugging.
- Executive and causal reports; CLI.
- 30 tests: determinism, invariants over 60 months for five strategies, schema conformance, invalid-content rejection, trace correctness, CLI.

## Run locally
```bash
python -m pip install -e ".[dev]"
pytest
python -m postcard_city.cli --months 12 --decision renegotiate --show-trace --trace-limit 20
python tools/validate_content.py
```

## Deliberate limitations
This is not production gameplay. It has no final engine, visual map, elections, media or opposition simulation, procedural generation, persistence layer, or final balance. See `CHANGELOG.md` for the known balance issues.

## Next technical steps
1. Rebalance so that the strategies are genuinely competitive (rent growth tied to policy, tourism saturation feedback, stronger costs for the boom path).
2. Add save/load serialization with a schema version and migration identifier.
3. Add the election and media event contracts and implement the first election.
4. Add scenario solvability checks (at least two viable strategies) as an automated test.
5. Build a thin interactive presentation layer.
6. Profile simulation and UI response under the slice's maximum state.
