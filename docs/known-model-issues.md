# Known Model Issues

Status: open findings from static review of `src/postcard_city/simulation.py` at commit `b5ec6f4`. They have not been confirmed by execution. Each finding must first be reproduced with a test marked `xfail(strict=True)` and then fixed, so that CI turns red when the fix lands and the marker is removed.

## KMI-1: Public-housing cash-flow metric subtracts arrears twice

`_update_social_housing` accumulates `cumulative_rent_income` as gross rent minus arrears. `_update_metrics` then computes `public_housing_net_cashflow` as cumulative rent income minus operating cost, maintenance, and `cumulative_arrears`. Arrears are therefore subtracted twice in the metric. The budget subtracts them once, so the metric and the budget disagree.

Impact: the metric understates public-housing cash flow by the cumulative arrears divided by elapsed months.

Proposed resolution: remove the second subtraction, or accumulate gross rent separately and derive collected rent explicitly. Review `tests/test_housing_migration.py` and `tests/test_integration.py` before changing, because existing assertions may depend on the current values.

## KMI-2: Housing demand is measured in persons and supply in dwellings

`_update_housing` compares `sum(cohort.population)` (persons) with `residential_units` plus occupied social units (dwellings). In the default scenario supply is about 210,000 dwellings and demand is about 280,000 persons or more, so vacancy is always 0. The `supply_relief_weight` term therefore never acts, and social housing or land policy cannot lower rents through this channel.

Impact: undermines the design claim that supply-side housing policy affects rents.

Proposed resolution: convert demand to households with an explicit household-size parameter, or define cohorts in households. Document the unit in `docs/simulation-contract.md`.

## KMI-3: Declared parameter is not read

`housing.parameters.migration_demand_weight` is declared in the scenario but is not read in `simulation.py`. Other modules were not reviewed for this finding.

Impact: a documented causal channel from migration demand to rent pressure does not exist in the code reviewed.

Proposed resolution: wire the parameter into rent pressure or remove it from the scenario and its schema.

## Resolution protocol

1. Reproduce the finding with an `xfail(strict=True)` test.
2. Check existing tests that depend on the affected behavior.
3. Fix the implementation and remove the marker.
4. Update `docs/simulation-contract.md` and `docs/coverage-matrix.md`.
5. Record the change in the changelog.
