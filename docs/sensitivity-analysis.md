# Sensitivity Analysis

Status: pre-implementation verification artifact.

## Purpose

This document records which scenario parameters are swept by automated tests, the direction of change the design requires, and what the tests do not claim. The tests live in `tests/test_sensitivity.py`.

## Scope and honesty about calibration

The sensitivity tests verify the direction and boundedness of responses. They do not establish that parameter magnitudes are calibrated against empirical data. Magnitude calibration requires sources recorded in `docs/evidence-registry.md` and is a separate, open task.

## Healthcare staffing

| Parameter | Change | Required effect on staffing ratio | Test |
|---|---|---|---|
| `healthcare_staff_sensitivity` | set to 0 | No change from baseline | `test_zero_staff_sensitivity_leaves_staffing_unchanged` |
| `healthcare_staff_sensitivity` | 0, 0.005, 0.01, 0.02 | Strictly decreasing | `test_staffing_declines_strictly_as_sensitivity_increases` |
| `monthly_base_tourist_growth` | set to 0 with no project | No change from baseline | `test_without_tourism_growth_staffing_stays_at_baseline` |
| `tourist_saturation_visitors` | raised to 2,000,000 | Higher staffing than default | `test_higher_saturation_threshold_reduces_staffing_loss` |
| `healthcare_access_neutral` | raised to 0.9 | Higher staffing than default | `test_higher_access_neutral_threshold_reduces_staffing_loss` |

Known model limitation: staffing has no recovery mechanism. A characterization test in `tests/test_contract_behavior.py` documents this; adding recovery is a deliberate design change that must update that test and `docs/simulation-contract.md`.

## Migration

| Parameter | Change | Required effect | Test |
|---|---|---|---|
| `base_arrival_rate` | set to 0 | Total population declines over 12 months | `test_without_arrivals_population_declines` |
| `base_departure_rate` | set to 0 | Total population grows over 12 months | `test_without_departures_population_grows` |
| `base_arrival_rate` | 0.002 versus 0.008 | Larger population at the higher rate | `test_higher_arrival_rate_yields_larger_population` |
| `base_departure_rate` | 50 with arrivals at 0 | Cohort populations stay non-negative and metrics stay finite | `test_population_stays_non_negative_under_extreme_departures` |

The growth and decline tests rely on the default scenario having positive attractiveness below the 0.5 departure threshold. If scenario data changes that property, these tests must fail and be reviewed rather than loosened.

## Not yet covered

- Interaction effects between housing supply, rents, and migration.
- Sensitivity of social-housing cash flow to arrears and operating cost.
- Sensitivity of political support and trust to staffing shortfall penalties.
- Multi-parameter sweeps and tipping points.
- Empirical calibration of every parameter.
