from postcard_city.model import Decision
from postcard_city.simulation import Simulation


def test_full_vertical_slice_integration():
    simulation = Simulation.from_default_slice(4821)
    simulation.start_social_housing(100)
    simulation.apply_land_decision("parcel_a", "sale_restricted")
    simulation.apply_land_decision("parcel_b", "lease_ground")
    simulation.apply_decision(Decision("aurora_leisure_proposal", "renegotiate"))
    simulation.run(36)
    state = simulation.state
    assert state.project_status == "safeguarded"
    assert state.parcels["parcel_a"].tenure == "sold"
    assert state.parcels["parcel_b"].tenure == "leased"
    assert state.social_housing.occupied_units == 100
    assert state.metrics["permanent_population"] > 0
    assert state.metrics["healthcare_staffing"] > 0
    assert state.metrics["public_housing_net_cashflow"] < 0


def test_replay_is_deterministic_after_all_major_actions():
    def run():
        simulation = Simulation.from_default_slice(777)
        simulation.start_social_housing(50)
        simulation.apply_land_decision("parcel_b", "lease_ground")
        simulation.apply_decision(Decision("aurora_leisure_proposal", "audit"))
        simulation.run(48)
        return simulation.state.snapshot()
    assert run() == run()


def test_housing_supply_uses_long_term_units_only():
    simulation = Simulation.from_default_slice()
    before = simulation.state.districts["historic_core"].average_rent
    simulation.advance_month()
    assert simulation.state.districts["historic_core"].average_rent >= before


def test_public_housing_cashflow_includes_rent_income():
    simulation = Simulation.from_default_slice()
    simulation.start_social_housing(100)
    for _ in range(24): simulation.advance_month()
    housing = simulation.state.social_housing
    assert housing.occupied_units == 100
    assert housing.cumulative_arrears > 0
    assert housing.cumulative_rent_income > 0
    assert simulation.state.metrics["public_housing_net_cashflow"] < 0


def test_invalid_actions_do_not_mutate_state():
    simulation = Simulation.from_default_slice()
    snapshot = simulation.state.snapshot()
    try: simulation.apply_land_decision("parcel_a", "invalid")
    except ValueError: pass
    assert simulation.state.snapshot() == snapshot
