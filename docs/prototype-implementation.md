# Prototype Implementation

## Purpose
This prototype is the first executable proof of the Postcard City simulation contract. It is intentionally small and engine-agnostic.

## Implemented
- Monthly deterministic simulation driven by validated scenario content.
- Scenario content as the current slice source of truth.
- JSON Schema and semantic validation for scenarios.
- Aggregate districts, tourism growth, tax revenue, housing pressure, and worker accessibility.
- Finite public parcels with freehold sale, restricted sale, and ground lease states.
- Social-housing construction delay, operating costs, below-market rents, arrears, maintenance, and essential-worker allocation.
- Cohort migration for essential workers, families, students, and retirees.
- Tourism-driven housing demand and migration pressure.
- Public-housing net cash-flow reporting, including arrears.
- Causal transition traces, executive reports, and CLI.
- Evidence registry and context-dependent policy mechanism cards.
- Automated tests for determinism, invariants, content conformance, land tenure, construction delay, arrears, and migration.

## Deliberate limitations
This is not production gameplay. Migration and housing coefficients are prototype calibration, not universal empirical estimates. Mechanism cards are not yet fully wired as runtime policy effects. The prototype has no final engine, visual map, elections, media or opposition simulation, procedural generation, or persistence layer.

## Next technical steps
1. Add save/load serialization with schema version and migration identifier.
2. Add explicit policy-card loading and robustness reports.
3. Add election, media, and opposition contracts.
4. Add scenario solvability checks with at least two viable housing strategies.
5. Build a thin interactive presentation layer.
