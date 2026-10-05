import pytest

from postcard_city.model import Decision
from postcard_city.simulation import Simulation

AURORA = "aurora_leisure_proposal"
STRATEGIES = [None, "approve", "reject", "renegotiate", "audit"]


def simulate(option, months, seed=None, social_units=0):
    simulation = Simulation.from_default_slice(seed)
    if option:
        simulation.apply_decision(Decision(AURORA, option))
    if social_units:
        simulation.start_social_housing(social_units)
    for _ in range(months):
        simulation.advance_month()
    return simulation


def test_decision_effects_are_applied_once():
    simulation = Simulation.from_default_slice()
    simulation.apply_decision(Decision(AURORA, "approve"))

    def decision_traces():
        return [t for t in simulation.state.traces if t.source == "decision:approve"]

    first = decision_traces()
    assert {"budget", "tourism_visitors"} <= {t.target for t in first}
    budget_trace = next(t for t in first if t.target == "budget")
    assert budget_trace.amount == pytest.approx(-18_000_000)
    for _ in range(12):
        simulation.advance_month()
    assert len(decision_traces()) == len(first)
    assert len(simulation.state.decision_history) == 1


def test_social_housing_is_unoccupied_and_earns_nothing_until_construction_completes():
    simulation = simulate(None, 23, social_units=100)
    housing = simulation.state.social_housing
    assert housing.occupied_units == 0
    assert housing.cumulative_rent_income == 0
    assert housing.cumulative_operating_cost > 0
    assert housing.construction_progress < 1.0
    simulation.advance_month()
    assert housing.occupied_units == 100
    assert housing.construction_progress == 1.0
    assert housing.cumulative_rent_income > 0


def test_social_housing_tracks_arrears_separately_and_is_not_automatically_profitable():
    simulation = simulate(None, 36, social_units=100)
    housing = simulation.state.social_housing
    occupied_months = 13
    gross_rent = 100 * 550 * occupied_months
    assert housing.cumulative_arrears > 0
    assert housing.cumulative_rent_income + housing.cumulative_arrears == pytest.approx(gross_rent)
    assert simulation.state.metrics["public_housing_net_cashflow"] < 0


def test_land_sale_is_irreversible_and_lease_keeps_ownership():
    simulation = Simulation.from_default_slice()
    budget = simulation.state.budget
    simulation.apply_land_decision("parcel_a", "sale_freehold")
    sold = simulation.state.parcels["parcel_a"]
    assert sold.tenure == "sold"
    assert not sold.public_control
    assert simulation.state.budget == pytest.approx(budget + 12_000_000)
    with pytest.raises(ValueError):
        simulation.apply_land_decision("parcel_a", "lease_ground")
    simulation.apply_land_decision("parcel_b", "lease_ground")
    leased = simulation.state.parcels["parcel_b"]
    assert leased.tenure == "leased"
    assert leased.public_control
    assert simulation.state.budget == pytest.approx(budget + 12_000_000 + 240_000)
    with pytest.raises(ValueError):
        simulation.apply_land_decision("parcel_b", "sale_freehold")


@pytest.mark.parametrize("parcel_id,mode", [("missing", "sale_freehold"), ("parcel_a", "gift")])
def test_invalid_land_decisions_do_not_change_state(parcel_id, mode):
    simulation = Simulation.from_default_slice()
    budget = simulation.state.budget
    with pytest.raises(ValueError):
        simulation.apply_land_decision(parcel_id, mode)
    assert simulation.state.budget == budget
    assert simulation.state.parcels["parcel_a"].tenure == "available"


@pytest.mark.parametrize("option", STRATEGIES)
def test_invariants_hold_over_ten_years_with_social_housing(option):
    simulation = Simulation.from_default_slice()
    if option:
        simulation.apply_decision(Decision(AURORA, option))
    simulation.start_social_housing(50)
    for _ in range(120):
        simulation.advance_month()
        state = simulation.state
        assert 0.0 <= state.institutional_trust <= 1.0
        assert 0.0 <= state.political_support <= 1.0
        assert 0.0 <= state.economic_diversity <= 1.0
        for district in state.districts.values():
            assert district.residential_units >= 0
            assert district.short_term_rental_units >= 0
            assert district.residential_units + district.short_term_rental_units <= district.housing_units
            assert 0.0 <= district.transport_reliability <= 1.0
            assert 0.0 <= district.healthcare_staff <= district.healthcare_capacity
            assert district.average_rent >= 0.0
        for cohort in state.migration.values():
            assert cohort.population >= 0
        housing = state.social_housing
        assert 0.0 <= housing.construction_progress <= 1.0
        assert 0 <= housing.occupied_units <= housing.units
        assert housing.cumulative_rent_income >= 0
        assert housing.cumulative_arrears >= 0
        assert all(value == value for value in state.metrics.values())
    assert all(trace.amount == trace.amount for trace in simulation.state.traces)


@pytest.mark.parametrize("option", STRATEGIES)
def test_current_model_has_no_spontaneous_staffing_recovery(option):
    """Characterization test: add a recovery mechanism deliberately and update this test with it."""
    simulation = Simulation.from_default_slice()
    if option:
        simulation.apply_decision(Decision(AURORA, option))
    previous = simulation.state.metrics["healthcare_staffing"]
    for _ in range(60):
        simulation.advance_month()
        current = simulation.state.metrics["healthcare_staffing"]
        assert current <= previous + 1e-12
        previous = current


def test_unconditional_approval_degrades_staffing_more_than_rejection():
    approved = simulate("approve", 36).state.metrics["healthcare_staffing"]
    rejected = simulate("reject", 36).state.metrics["healthcare_staffing"]
    assert approved < rejected


def test_financing_warning_fires_once_and_only_from_month_six():
    assert "aurora_financing_warning" not in simulate("approve", 5).state.event_history
    history = simulate("approve", 24).state.event_history
    assert history.count("aurora_financing_warning") == 1
    for option in (None, "reject", "renegotiate", "audit"):
        assert "aurora_financing_warning" not in simulate(option, 24).state.event_history
