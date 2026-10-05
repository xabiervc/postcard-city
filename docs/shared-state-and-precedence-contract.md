# Shared State and Precedence Contract

Status: normative pre-implementation contract.
Version: 1.0.

## Purpose

This document defines the shared state vocabulary and resolution order used by all simulation subsystems. A subsystem may add domain-specific variables, but it must not silently redefine a shared variable, unit, range, clock, or precedence rule.

## Shared state registry

| Variable | Unit and range | Owner | Update rule |
|---|---|---|---|
| simulation time | integer turns; strictly increasing | core runtime | advance once per resolved turn |
| public budget | budget units; finite and non-negative | fiscal layer | income minus committed and realized expenditure |
| public debt | budget units; non-negative | fiscal layer | prior debt plus borrowing minus repayment |
| fiscal capacity | capacity units; finite and non-negative | fiscal layer | derived from revenue, debt service, and confidence |
| administrative capacity | capacity units; finite and non-negative | core services layer | prior capacity plus investment minus overload and attrition |
| essential-service availability | percentage points, 0–100 | service layer | weighted service output after capacity allocation |
| institutional legitimacy | index, 0–100 | legitimacy layer | evidence-weighted response to outcomes and fairness |
| public trust | index, 0–100 | legitimacy layer | updated from transparency, service outcomes, and perceived treatment |
| population | persons; integer, non-negative | demographic layer | births plus arrivals minus deaths and departures |
| displacement | persons; integer, non-negative | migration layer | displaced households generated minus settled households |
| inequality | normalized index, 0–1 | distribution layer | distributional incidence after transfers and shocks |
| infrastructure condition | index, 0–100 | infrastructure layer | maintenance and investment minus deterioration |
| uncertainty | probability mass or bounded confidence score | evidence layer | updated from observations and model confidence |

## Update discipline

Each turn is resolved in phases: observe, validate, allocate, resolve, record, and advance. Domain systems may propose changes during allocation, but only the owning layer commits updates to shared variables.

Adapters must declare source variable, destination variable, unit conversion, rounding rule, uncertainty effect, and trace identifier. Invalid ranges are rejected rather than silently clipped, except where a schema explicitly defines a bounded projection.

## Precedence order

When actions compete for limited capacity, the resolver applies this order:

1. immediate protection of life and prevention of severe irreversible harm;
2. continuity of essential services and legally required functions;
3. preservation of administrative and infrastructure capacity;
4. legally binding transfers, debt service, and contractual obligations;
5. stabilization of legitimacy, trust, and social cohesion;
6. discretionary reforms, growth, prestige, and optional projects.

A lower-priority action may proceed only after higher-priority requirements are funded or an explicit shortfall decision is recorded. The resolver must expose the trade-off; it must not hide displacement of one objective by another.

## Capacity saturation

If demand exceeds available fiscal, administrative, or service capacity, the resolver records the deficit, affected population, deferred action, duration, and confidence interval. It may not create negative budgets, service availability above 100, impossible staffing, or unbounded debt without an explicit failure state.

Repeated overload produces documented deterioration, not an implicit hard reset. Recovery requires a policy, available capacity, and a causal trace linking the intervention to the improvement.

## Uncertainty and deterministic replay

Every material resolution records a seed, input snapshot, mechanism identifiers, uncertainty marker, and output delta. Fixed inputs and seed must produce identical state, ordering, rounding, and trace output across supported runtimes.

Uncertainty must propagate through adapters. A precise-looking output may not be emitted when material inputs are unresolved; the system must expose a range, confidence marker, or unresolved status.

## Invariants

The following invariants are mandatory:

- time never decreases;
- population, debt, displacement, and budget obligations are not negative;
- service availability remains within 0–100;
- legitimacy, trust, and infrastructure condition remain within 0–100;
- every committed delta has an owner and trace identifier;
- every rejected action reports a stable reason code;
- no lower-priority action silently displaces a higher-priority obligation;
- replaying the same validated input and seed reproduces the same state and trace.

## Integration requirements

Housing, migration, healthcare staffing, social mobilization, strategic crises, technology, and procedural generation must map their outputs to this registry before integration is considered complete. Each adapter requires schema validation, unit tests, edge-case tests, and at least one cross-system integration test.

## Exit criteria

This contract is considered implemented only when the repository contains:

- a versioned schema or typed representation of the registry;
- precedence-resolution tests, including capacity shortfall cases;
- deterministic replay tests for state and traces;
- invalid-range and stable-error tests;
- integration tests for each P0 dependency edge;
- documentation of unresolved assumptions and known limitations.
