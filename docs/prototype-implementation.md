# Prototype Implementation

## Purpose
This prototype is the first executable proof of the Postcard City simulation contract. It is intentionally small and engine-agnostic.

## Implemented
- Monthly deterministic simulation driven by validated scenario content.
- Scenario content is the single source of truth for the current slice.
- JSON Schema and semantic validation for scenarios.
- Aggregate districts, tourism growth and tax revenue.
- Housing conversion and rent pressure.
- Worker accessibility feeding healthcare staffing, with a trust and support penalty below a threshold.
- Transport reliability and budget.
- Aurora Leisure decision (approve, reject, renegotiate, audit), resolvable once, scheduled by month.
- Data-defined events with simple conditions.
- Causal transition traces for player-readable debugging.
- Executive and causal reports; CLI.
- Evidence registry and seven context-dependent housing-policy mechanism cards.
- JSON schemas and automated validation for evidence and mechanism content.
- Automated tests for determinism, invariants, content conformance, trace correctness, CLI behaviour, and evidence-reference integrity.

## Run locally
```bash
python -m pip install -e ".[dev]"
pytest
python tools/validate_content.py
python tools/validate_mechanisms.py
python -m postcard_city.cli --months 12 --decision renegotiate --show-trace --trace-limit 20
```

## Deliberate limitations
This is not production gameplay. Mechanism cards are currently preimplementation data and are not yet wired into the simulation. The prototype has no final engine, visual map, elections, media or opposition simulation, procedural generation, persistence layer, or final balance.

## Next technical steps
1. Add housing supply, social-housing construction, public-parcel sale/lease, and cohort migration using the validated mechanism cards.
2. Add save/load serialization with a schema version and migration identifier.
3. Add the election and media event contracts.
4. Add scenario solvability checks and robustness reports.
5. Build a thin interactive presentation layer.
