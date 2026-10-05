# Simulation Calibration Plan

## Purpose

Mathematical stability is necessary but does not prove that the game produces interesting decisions. Calibration must test both system behaviour and play value.

## Reference runs

Maintain deterministic runs for:

- baseline balanced conditions;
- low-capacity stress;
- high tourism pressure;
- housing scarcity;
- healthcare staffing stress;
- strong public-housing intervention;
- land-sale and land-lease alternatives;
- extreme migration departure pressure.

Each run records seed, inputs, decisions, state snapshots, events, traces, and final postcards.

## Behavioural checks

The calibration suite should detect:

- strategies that dominate all alternatives;
- interventions with no observable consequence;
- metrics that never affect a decision;
- states from which recovery is impossible without player agency;
- runaway growth or collapse;
- oscillation that players cannot explain;
- delayed consequences that arrive too late to matter;
- repeated choices that produce identical outcomes.

## Playability checks

A prototype playtest should measure:

- time to first meaningful decision;
- percentage of players who can state the main trade-off;
- percentage who can predict at least one consequence;
- number of unnecessary panel switches;
- perceived clarity of causal feedback;
- whether the delayed consequence is remembered;
- whether players choose different priorities on replay;
- whether a failure feels caused rather than arbitrary.

## Acceptance thresholds for the slice

The slice is not ready for expansion unless:

- most playtesters can explain the first intervention without coaching;
- every primary metric is connected to a decision or visible consequence;
- at least two strategies are viable but imperfect;
- no single strategy dominates across all reference contexts;
- the delayed consequence is noticed and attributed;
- the final postcard comparison is understandable without debug tools.

Exact numerical thresholds should be set after the first five playtests rather than fabricated in advance.
