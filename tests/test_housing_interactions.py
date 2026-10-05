import pytest

from postcard_city.model import Decision
from postcard_city.scenario import DEFAULT_SCENARIO_PATH, load_scenario
from postcard_city.simulation import Simulation

AURORA = "aurora_leisure_proposal"
GROSS_RENT_MONTHS = 13


def build(mutate=None):
    scenario = load_scenario(DEFAULT_SCENARIO_PATH)
    if mutate:
        mutate(scenario)
    return Simulation(scenario)


def set_social(**values):
    return lambda scenario: scenario["housing"]["social_housing"].update(values)


def set_profile(status, **values):
    return lambda scenario: scenario["project_profiles"][status].update(values)


def set_housing_parameter(**values):
    return lambda scenario: scenario["housing"]["parameters"].update(values)


def advance(simulation, months):
    for _ in range(months):
        simulation.advance_month()


def social_after(months, units=100, **values):
    simulation = build(set_social(**values))
    simulation.start_social_housing(units)
    advance(simulation, months)
    return simulation.state.social_housing


def operating_net(housing):
    return housing.cumulative_rent_income - housing.cumulative_operating_cost - housing.cumulative_maintenance_cost


def monthly_operating_net(rent):
    simulation = build(set_social(monthly_target_rent=rent))
    simulation.start_social_housing(100)
    advance(simulation, 24)
    housing = simulation.state.social_housing
    before = operating_net(housing)
    advance(simulation, 1)
    return operating_net(housing) - before


def test_higher_arrears_rate_increases_arrears_and_reduces_collected_rent():
    results = [social_after(36, arrears_rate=rate) for rate in (0.0, 0.08, 0.3)]
    arrears = [housing.cumulative_arrears for housing in results]
    collected = [housing.cumulative_rent_income for housing in results]
    assert arrears[0] == 0
    assert arrears[0] < arrears[1] < arrears[2]
    assert collected[0] > collected[1] > collected[2]
    for housing in results:
        assert housing.cumulative_rent_income + housing.cumulative_arrears == pytest.approx(100 * 550 * GROSS_RENT_MONTHS)


def test_higher_target_rent_improves_operating_result():
    results = [operating_net(social_after(36, monthly_target_rent=rent)) for rent in (400, 550, 900)]
    assert results[0] < results[1] < results[2]


def test_costs_accrue_during_construction_without_any_rent():
    housing = social_after(12)
    assert housing.cumulative_rent_income == 0
    assert operating_net(housing) == pytest.approx(-12 * 200_000)


def test_monthly_result_follows_rent_collection_minus_costs():
    assert monthly_operating_net(2200) == pytest.approx(100 * 2200 * 0.92 - 200_000)
    assert monthly_operating_net(1000) == pytest.approx(100 * 1000 * 0.92 - 200_000)


def test_higher_conversion_rate_shifts_housing_to_short_term_rentals():
    cores = []
    for rate in (0.003, 0.01):
        simulation = build(set_profile("approved", conversion_rate=rate))
        simulation.apply_decision(Decision(AURORA, "approve"))
        advance(simulation, 24)
        cores.append(simulation.state.districts["historic_core"])
    assert cores[1].residential_units < cores[0].residential_units
    assert cores[1].short_term_rental_units > cores[0].short_term_rental_units


def test_stronger_tourism_demand_raises_rent_and_lowers_essential_worker_migration():
    rents = []
    migration = []
    for weight in (0.2, 1.0):
        simulation = build(set_housing_parameter(tourism_demand_weight=weight))
        advance(simulation, 12)
        rents.append(simulation.state.districts["historic_core"].average_rent)
        migration.append(simulation.state.migration["essential_workers"].net_migration)
    assert rents[1] > rents[0]
    assert migration[1] < migration[0]


def test_budget_accounts_for_social_housing_exactly_once():
    with_housing = build()
    with_housing.start_social_housing(100)
    advance(with_housing, 36)
    baseline = build()
    advance(baseline, 36)
    housing = with_housing.state.social_housing
    expected = -100 * 180_000 + operating_net(housing)
    assert with_housing.state.budget - baseline.state.budget == pytest.approx(expected, rel=1e-9)
