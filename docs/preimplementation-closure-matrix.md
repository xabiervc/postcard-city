# Preimplementation Closure Matrix

Status: normative planning artifact.
Version: 1.0.

## Definition of done

Preimplementation is complete when every required subsystem has a stable contract, versioned data shape, documented causal model, validation coverage, integration points, safety constraints, and a traceable path to implementation. A passing unit-test suite alone is not sufficient.

Each row is closed only when all six gates are satisfied:

1. contract: inputs, outputs, invariants, state transitions, and failure behavior are explicit;
2. schema: entities, units, ranges, defaults, references, and versioning are defined;
3. causal model: mechanisms, feedbacks, delays, uncertainty, and observable effects are documented;
4. validation: happy paths, edge cases, invariants, determinism, and negative cases are tested;
5. integration: dependencies and cross-system effects are specified and tested;
6. safety and traceability: rights, non-operational boundaries, explanations, and evidence links are recorded.

## Closure status

| Area | Current evidence | Priority | Remaining closure work |
|---|---|---:|---|
| Core simulation contract | `docs/simulation-contract.md`, contract tests | P0 | Add explicit cross-system precedence and failure semantics |
| Scenario and crisis catalog | `docs/crisis-catalog.md`, `docs/crisis-catalog.schema.json`, validation tests | P0 | Version references, dependency rules, and complete scenario coverage |
| Causal mechanisms and traces | `docs/mechanism-cards.md`, `docs/mechanism-runtime.md`, trace tests | P0 | Require every material output to cite a mechanism and uncertainty |
| Housing and migration | `docs/housing-and-migration.md`, integration tests | P0 | Close distributional effects, capacity limits, and long-run feedbacks |
| Healthcare staffing | staffing model and sensitivity tests | P1 | Document intervention boundaries, lag assumptions, and failure modes |
| Social mobilization and protest | `docs/social-mobilization-system.md`, design tests | P1 | Add integration contract for budget, legitimacy, services, and rights |
| Strategic crises | `docs/strategic-crisis-catalog.md`, design tests | P1 | Link crisis families to common state, uncertainty, and recovery model |
| Technology and R&D | `docs/technology-and-rnd-system.md`, design tests | P1 | Define spillovers, failure states, and evidence confidence updates |
| Procedural generation | `docs/procedural-generation-bible.md`, scenario validation | P1 | Define reproducibility, content provenance, and rejection rules |
| Accessibility and localization | `docs/accessibility-and-localization.md` | P2 | Add testable acceptance criteria and content fallback behavior |
| Quality and release | `docs/quality-plan.md`, CI | P0 | Add integration, property, performance, and reproducibility gates |

## Cross-system state

The following shared variables must have one authoritative definition and one unit convention:

- public budget, debt, and fiscal capacity;
- institutional legitimacy and public trust;
- administrative capacity and service availability;
- population, displacement, and migration;
- inequality, household income, and distributional burden;
- infrastructure condition and land use;
- information quality, uncertainty, and evidence confidence;
- time, lags, recovery, and long-term memory.

No subsystem may silently redefine a shared variable. Adapters must declare transformations, units, rounding, and uncertainty effects.

## Priority plan

### P0 — before implementation

- freeze the shared state vocabulary and units;
- specify precedence when policies or crises compete for capacity;
- add integration and property tests across housing, migration, services, budget, legitimacy, and crisis systems;
- define deterministic replay and seed compatibility;
- require causal traces for material outputs;
- document known model limitations and unresolved assumptions.

### P1 — before vertical slice expansion

- close social mobilization, strategic crisis, technology, and procedural-generation integration contracts;
- add scenario composition and recovery tests;
- validate uncertainty propagation and distributional reporting;
- define performance budgets and representative workloads.

### P2 — before content scale-up

- formalize accessibility and localization acceptance tests;
- add content provenance and review workflows;
- define migration/version compatibility for saved simulations;
- expand adversarial and fairness-oriented review.

## Exit criteria

The repository may claim “100% preimplementation” only when:

- all P0 rows have no unspecified remaining closure work;
- every shared variable has an owner, unit, range, and transformation policy;
- at least one integration test covers each P0 dependency edge;
- deterministic replay produces identical state and trace outputs for a fixed seed;
- invalid or unsafe content is rejected by validation;
- every material output has a causal explanation and uncertainty marker;
- CI runs unit, integration, property, schema, and reproducibility checks;
- open assumptions and known limitations are listed and accepted.

Until then, status should be reported as “preimplementation in progress,” not complete.

## Next implementation gate

The next concrete gate is the shared-state and precedence contract. It should be completed before adding more subsystem-specific design or implementation, because all later integration tests depend on it.
