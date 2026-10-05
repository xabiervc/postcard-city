# Simulation Contract

Status: normative pre-implementation contract.
Version: 1.0.

## Purpose

This document defines the observable contract of the Postcard City simulation. Production code and tests must preserve these rules unless this document is versioned and updated deliberately.

## Time model

The simulation advances in discrete calendar months. `state.month` starts at `0` and increases by exactly one after each successful `advance_month()` call.

A scheduled decision for month `N` is applied before the monthly update for month `N`.

## Monthly order

Each month is processed in this order:

1. Apply scheduled decisions.
2. Advance tourism demand and calculate tourism revenue.
3. Update permanent and short-term housing allocation.
4. Update healthcare staffing and transport reliability.
5. Update migration cohorts.
6. Advance social-housing construction and cash flow.
7. Recalculate metrics.
8. Resolve events whose conditions match the new state.
9. Clamp bounded state variables and return the state.

The order is intentional: later mechanisms observe the outputs of earlier mechanisms in the same month.

## Decision semantics

A decision is identified by `(decision_id, option_id)` and may be resolved only once per simulation. Unknown decisions and options fail with `ValueError` and must not modify decision history.

Decision effects are applied once when the decision is resolved. Recurring consequences belong to the monthly simulation update and must not be applied again as one-time effects.

## Core units

- Budget and financial flows: currency units per simulation month.
- Tourism visitors: visitors per simulation month.
- Housing units: physical dwelling units.
- Rent: currency units per dwelling per month.
- Healthcare staffing: staff members.
- Healthcare staffing ratio: total healthcare staff divided by total healthcare capacity.
- Support, trust, diversity, reliability, pressure, and rates: normalized values in `[0, 1]` unless a field explicitly documents another range.

Trace amounts are deltas, never absolute values.

## Housing

Permanent and short-term housing allocation must satisfy:

`residential_units + short_term_rental_units <= housing_units`.

Social-housing construction progress is bounded to `[0, 1]`. Occupancy cannot exceed built units. Rent is zero while units are unoccupied or construction is incomplete. Arrears are tracked separately and are not counted as collected rent.

Social housing may have negative net cash flow. Public ownership does not imply automatic profitability.

## Healthcare

Healthcare staffing is bounded by `[0, healthcare_capacity]`. Tourism pressure and project growth may reduce effective staffing. The staffing ratio is recalculated from current staff and capacity; it must not be cached as a constant.

When staffing falls below the configured neutral threshold, the configured trust and political-support penalties apply. The change must be represented by a trace whose source is `healthcare_staffing`.

## Migration

Migration is cohort-based. Each cohort is updated from affordability, jobs, services, tourism pressure, mobility, and its sensitivity weights. Population cannot become negative.

## Events

Events are evaluated after the monthly state and metrics update. Each event ID is unique in a valid scenario. Conditions must be explicit and reproducible from the state.

## Reproducibility

For a fixed scenario, seed, and ordered decision schedule, snapshots must be identical. Randomness must use the simulation-owned random generator and must not depend on wall-clock time, process identity, network state, or iteration order of unordered external inputs.

## Failure behavior

Invalid scenarios fail during loading with `ScenarioValidationError`. Invalid decisions fail without mutating decision history. Violations of bounded state are implementation defects, not values to silently ignore.

## Contract changes

Changes that alter ordering, units, decision semantics, event timing, or snapshot meaning require:

- a versioned update to this document;
- updated tests;
- a changelog entry;
- a migration note if persisted snapshots are affected.
