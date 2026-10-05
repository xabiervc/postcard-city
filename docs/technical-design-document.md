# Technical Design Document

## Technical direction
The first prototype should prioritize deterministic simulation, rapid iteration, testability, and data-driven content over visual fidelity.

## Recommended prototype architecture
- Simulation core: strongly typed, engine-agnostic module.
- Content: versioned JSON or YAML validated against schemas.
- Presentation: adapter layer for UI and map visualization.
- Seed service: named deterministic random streams.
- Save service: versioned snapshots with migration identifiers.
- Event service: data-driven event definitions and outcomes.
- Localization service: stable keys, plural rules, formatting, and fallback handling.

## Module boundaries
- `domain`: entities and value objects.
- `simulation`: monthly tick processing and systems.
- `content`: loading and validation.
- `generation`: region and scenario generation.
- `events`: decision and event resolution.
- `presentation`: view models and reports.
- `tools`: validators, seed inspection, balance reports.
- `tests`: unit, integration, property, scenario, and regression tests.

## Deterministic random streams
Use named streams such as `generation`, `events`, `media`, and `population`. A system must not consume another system's random stream implicitly.

## Save requirements
Save files include schema version, content version, seed, configuration, decision history, simulation time, and state snapshot. Loading an older version must either migrate safely or fail with a clear explanation.

## Performance strategy
The vertical slice uses aggregate cohorts and bounded event queues. Future scale should use level-of-detail simulation, batched updates, cached spatial queries, and profiling before optimization.

## Tooling requirements
- Content schema validator.
- Scenario validator.
- Seed replay tool.
- State inspector.
- Event trace viewer.
- Balance report generator.
- Localization key checker.
- Save migration tests.

## Technical spikes
1. Deterministic monthly simulation.
2. Region state serialization.
3. Schema validation and hot reload.
4. Basic spatial accessibility and commute calculation.
5. Event decision resolution.
6. UI summary-to-detail navigation.

## Initial engine decision
Do not lock the final engine before the simulation spike. Compare a fast data-oriented prototype path with the intended production engine using the same domain contracts.
