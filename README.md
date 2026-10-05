# Postcard City

> Govern a living region. Build a destination. Decide what remains when the visitors leave.

## Status

**Deterministic simulation prototype with a documented vertical-slice design**

The repository contains an executable, tested simulation prototype and the design contracts for a future playable vertical slice. The simulation, CLI, reporting, robustness, sensitivity checks, and automated contracts are implemented. The project is **not yet a complete game**: visual presentation, playable characters, postcard comparison, campaign flow, and structured playtesting remain prototype work.

## Game overview

Postcard City is a political regional city simulator about tourism, housing, employment, public services, economic diversification, power, media, and livability.

The player is not an omnipotent mayor. The intended fantasy is to steer a living region under pressure, negotiate incompatible interests, accept uncertainty, and decide what kind of city deserves to be remembered.

The central question is not whether tourism is good or bad. It is whether a region can become a successful destination without becoming impossible to live in.

## Design north star

> **Turn a region into a destination without making it impossible to live there.**

## What makes it different

Postcard City is not a conventional empty-grid city builder and not a literal theme-park manager.

- Construction is a policy instrument, not the entire game.
- Tourism is a transforming force, not just an income source.
- Housing, jobs, services, and transport are connected.
- Economic opportunities can be beneficial, predatory, speculative, fraudulent, or misjudged.
- Information, legitimacy, evidence, and delayed consequences matter.
- Procedural variation creates coherent regional cases rather than random maps without context.
- Complexity should be scalable without removing the core fantasy.
- Postcards are intended to become playable memories of places, not decorative screenshots.

## Intended gameplay loop

```text
observe -> interpret -> prioritize -> intervene -> resolve -> remember
```

The planned player-facing cycle is:

1. Inspect districts, indicators, testimonies, and previous postcards.
2. Interpret competing causes, evidence, and uncertainty.
3. Prioritize one problem or value under resource and political constraints.
4. Intervene through a policy, decision, land action, housing action, or negotiation.
5. Advance time and resolve delayed effects or crises.
6. Review metrics, traces, affected perspectives, and changed places.
7. Create or compare a postcard that records what improved, what was displaced, and what remains unresolved.

The current CLI exposes the simulation and causal trace portions of this loop. The complete player-facing loop requires the vertical-slice prototype.

## Current vertical slice

### The Overheated Destination

A coastal historic metropolitan region has a profitable tourist centre, rising housing pressure, a car-dependent outer district, and an understaffed public hospital.

Aurora Leisure proposes a large hotel and entertainment district. The proposal promises visitors, jobs, tax income, and transport investment. Its risks concern financing, worker quality, public infrastructure costs, legal exceptions, housing pressure, and long-term dependence.

The current simulation supports four approaches:

- approve;
- reject;
- renegotiate;
- audit.

The simulation also supports monthly decisions, public land actions, social-housing construction, events, metrics, and causal traces. The future playable slice is designed to add four recurring perspectives, one crisis, two interventions, delayed consequences, and two comparable postcards.

## Implemented prototype

Implemented and covered by automated tests:

- deterministic monthly simulation with explicit seeds;
- aggregate districts and scenario validation;
- tourism growth, revenue, housing conversion, rent pressure, migration, healthcare staffing, and transport reliability;
- budget updates and public-housing construction/operations;
- public-land sale and ground-lease decisions;
- scheduled decisions and event resolution;
- causal traces and executive reporting;
- mechanism cards and robustness sweeps;
- sensitivity checks for staffing and migration;
- reproducibility, integration, invariant, boundary, robustness, and CLI tests.

Not yet implemented as a player-facing game:

- visual district presentation;
- playable recurring characters and relationship UI;
- crisis UI and campaign progression;
- postcard creation and comparison records;
- success/failure presentation;
- full accessibility implementation;
- structured playtests and calibration evidence.

## Running locally

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m postcard_city.cli --months 12 --decision renegotiate
python -m postcard_city.cli --months 6 --decision renegotiate --decision-month 2 --show-trace --trace-limit 5
python tools/validate_content.py
```

Additional CLI options include `--start-social-housing`, `--land-parcel`, `--land-mode`, `--seed`, `--show-trace`, and `--trace-limit`.

For a valid parcel ID, use a parcel whose scenario data has `public_control: true` and `tenure: "available"`.

## Design closure documents

- [Player fantasy and gameplay loop](docs/player-fantasy-and-gameplay-loop.md)
- [Postcard memory system](docs/postcard-memory-system.md)
- [Character bible](docs/character-bible.md)
- [Relationship system](docs/relationship-system.md)
- [Campaign structure](docs/campaign-structure.md)
- [Complexity budget](docs/complexity-budget.md)
- [Simulation calibration plan](docs/simulation-calibration-plan.md)
- [Information accessibility specification](docs/information-accessibility-spec.md)
- [Vertical-slice acceptance matrix](docs/vertical-slice-acceptance-matrix.md)

These documents intentionally distinguish design-ready requirements from features that require an interactive build or playtests.

## Repository structure

- `src/postcard_city/`: deterministic domain and simulation prototype.
- `data/`: authored scenario and mechanism content.
- `docs/`: product, design, simulation, technical, accessibility, and quality documentation.
- `schemas/`: machine-readable content contracts.
- `config/`: design and vertical-slice configuration.
- `tests/`: automated tests.
- `tools/`: validation and prototype tools.
- `.github/workflows/`: continuous integration.

## Development principles

1. Protect the core fantasy: govern a living region under pressure.
2. Make causes and consequences inspectable.
3. Prefer systemic consequences over moral labels.
4. Do not make tourism automatically good or bad.
5. Treat corruption as institutional debt, not a binary morality switch.
6. Keep residents, workers, institutions, businesses, media, and opposition distinct.
7. Use authored arcs around procedural variation.
8. Scale complexity without removing the core experience.
9. Build accessibility and localization into the architecture from day one.
10. Require deterministic tests for major simulation rules.

## Quality target

The project aims for an award-level standard comparable with the design, narrative, accessibility, presentation, and technical polish expected by major game awards. This is an aspiration and a set of gates, not a claim that the current prototype has reached that standard.

Current quality gates include:

- understandable but non-trivial decisions;
- multiple viable strategies;
- visible and traceable outcomes;
- coherent procedural scenarios;
- overview and deep-inspection support;
- accessibility designed in rather than patched in;
- reliable seeds, content, saves, and simulation results.

## Roadmap

### Phase 0 — Preimplementation
Product definition, simulation boundaries, schemas, vertical-slice design, technical risks, accessibility, localization, and quality gates.

### Phase 1 — Simulation prototype
Deterministic monthly simulation, causal traces, state inspection, reporting, robustness, sensitivity, serialization, and invariant tests.

### Phase 2 — Vertical slice
A small visual region, executive and detailed UI, four recurring perspectives, postcard comparison, one crisis, complete evaluation, and accessibility baseline.

### Phase 3 — Systems expansion
Procedural scenario generation, industry opportunities, more crises, deeper political actors, scalable complexity, and authoring tools.

### Phase 4 — Production
Multiple regional templates, campaign scenarios, sandbox, art, audio, narrative content, additional languages, and extensive playtesting.

### Phase 5 — Polish
Performance, accessibility audit, localization QA, onboarding, UX refinement, stability, balance, and final quality review.

## License

All rights reserved. See `LICENSE.md`.
