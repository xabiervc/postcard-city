import pytest

from postcard_city.model import Decision
from postcard_city.scenario import DEFAULT_SCENARIO_PATH, load_scenario
from postcard_city.simulation import Simulation

AURORA = "aurora_leisure_proposal"


def build(mutate=None):
    scenario = load_scenario(DEFAULT_SCENARIO_PATH)
    if mutate:
        mutate(scenario)
    return Simulation(scenario)


def staffing_after(months, option=None, mutate=None):
    simulation = build(mutate)
    if option:
        simulation.apply_decision(Decision(AURORA, option))
    for _ in range(months):
        simulation.advance_month()
    return simulation.state.metrics["healthcare_staffing"]


def population(simulation):
    return sum(cohort.population for cohort in simulation.state.migration.values())


def set_parameter(name, value):
    return lambda scenario: scenario["parameters"].update({name: value})


def set_migration(**values):
    return lambda scenario: scenario["migration"]["parameters"].update(values)


def test_zero_staff_sensitivity_leaves_staffing_unchanged():
    baseline = build().state.metrics["healthcare_staffing"]
    result = staffing_after(36, "approve", set_parameter("healthcare_staff_sensitivity", 0.0))
    assert result == pytest.approx(baseline)


def test_without_tourism_growth_staffing_stays_at_baseline():
    baseline = build().state.metrics["healthcare_staffing"]
    result = staffing_after(60, None, set_parameter("monthly_base_tourist_growth", 0.0))
    assert result == pytest.approx(baseline)


def test_staffing_declines_strictly_as_sensitivity_increases():
    values = [
        staffing_after(36, "approve", set_parameter("healthcare_staff_sensitivity", sensitivity))
        for sensitivity in (0.0, 0.005, 0.01, 0.02)
    ]
    assert all(earlier > later for earlier, later in zip(values, values[1:]))


def test_higher_saturation_threshold_reduces_staffing_loss():
    default = staffing_after(36, "approve")
    relaxed = staffing_after(36, "approve", set_parameter("tourist_saturation_visitors", 2_000_000))
    assert relaxed > default


def test_higher_access_neutral_threshold_reduces_staffing_loss():
    default = staffing_after(36, "approve")
    tolerant = staffing_after(36, "approve", set_parameter("healthcare_access_neutral", 0.9))
    assert tolerant > default


def test_without_arrivals_population_declines():
    simulation = build(set_migration(base_arrival_rate=0.0))
    start = population(simulation)
    for _ in range(12):
        simulation.advance_month()
    assert population(simulation) < start


def test_without_departures_population_grows():
    simulation = build(set_migration(base_departure_rate=0.0))
    start = population(simulation)
    for _ in range(12):
        simulation.advance_month()
    assert population(simulation) > start


def test_higher_arrival_rate_yields_larger_population():
    results = []
    for rate in (0.002, 0.008):
        simulation = build(set_migration(base_arrival_rate=rate))
        for _ in range(12):
            simulation.advance_month()
        results.append(population(simulation))
    assert results[0] < results[1]


def test_population_stays_non_negative_under_extreme_departures():
    simulation = build(set_migration(base_arrival_rate=0.0, base_departure_rate=50.0))
    for _ in range(24):
        simulation.advance_month()
        assert all(cohort.population >= 0 for cohort in simulation.state.migration.values())
        assert all(value == value for value in simulation.state.metrics.values())
