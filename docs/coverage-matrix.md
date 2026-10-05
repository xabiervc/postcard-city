# Simulation Coverage Matrix

Status: normative planning artifact.

| System | Inputs | State outputs | Metrics | Required traces | Existing tests | Next tests |
|---|---|---|---|---|---|---|
| Decisions | decision and option IDs; effects | budget, tourism, support, trust, diversity, project status | state snapshot | decision source to changed target | `test_unknown_decision_is_rejected_and_not_recorded`; `test_a_decision_can_only_be_resolved_once` | effect-is-applied-once |
| Tourism | base growth, profile bonus, multiplier | tourism visitors, tourism revenue | tourism pressure | `tourism_demand → tourism_visitors` | `test_different_decisions_produce_different_states` | 12/36/60-month bounds |
| Housing market | conversion rate, tourism pressure, migration demand | permanent units, short-term units, average rent | affordability | housing conversion and rent deltas | `test_safeguarded_project_improves_diversity_and_limits_conversion`; `test_rent_trace_records_a_change_not_an_absolute_value` | conversion edge cases |
| Healthcare | staffing sensitivity, access neutral, capacity | healthcare staff | healthcare staffing ratio | `healthcare_staffing` source | `test_healthcare_staffing_actually_changes_and_depends_on_decision`; `test_low_healthcare_staffing_reduces_trust_and_is_traced` | sensitivity matrix |
| Migration | affordability, jobs, services, cohort sensitivities | cohort population, net migration | permanent population, essential-worker migration | regional attractiveness | integration and migration tests | cohort non-negativity |
| Social housing | units, construction months, costs, rent, arrears | progress, occupancy, rents, costs, arrears | public-housing cash flow | social housing to budget | integration and housing tests | arrears and delayed-occupancy cases |
| Land | parcel, tenure, mode, market value | budget, tenure, public control | budget | land decision to budget | housing/migration tests | repeated-sale rejection |
| Events | month, status, metric conditions | event history, support, trust | affected metrics | event effects | financing-warning test | duplicate-trigger policy |
| Validation | scenario schema and content | no state; loader failure | none | none | invalid-content parametrization | schema/property fuzz cases |

## Exit criteria

The core is ready for vertical-slice implementation when every row has:

- at least one deterministic behavioral test;
- at least one invariant test;
- explicit trace targets for player-visible causal changes;
- documented units and bounds;
- deterministic behavior under a fixed seed;
- no unresolved placeholder behavior.

## Vertical-slice gate

The first vertical slice must exercise, in one reproducible 12-month scenario:

1. one decision with two materially different options;
2. tourism and budget changes;
3. housing conversion and rent movement;
4. healthcare staffing degradation and its political consequence;
5. at least one migration response;
6. one social-housing or land action;
7. one conditional event;
8. a player-readable consequence report.
