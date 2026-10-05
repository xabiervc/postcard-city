import pytest

from postcard_city.model import Decision
from postcard_city.simulation import Simulation

AURORA = "aurora_leisure_proposal"


def run(option=None, months=24):
    simulation = Simulation.from_default_slice()
    if option: simulation.apply_decision(Decision(AURORA, option))
    for _ in range(months): simulation.advance_month()
    return simulation


def test_social_housing_is_delayed_and_not_automatically_profitable():
    simulation = Simulation.from_default_slice()
    simulation.start_social_housing(100)
    before = simulation.state.social_housing.occupied_units
    for _ in range(6): simulation.advance_month()
    assert simulation.state.social_housing.occupied_units == before == 0
    assert simulation.state.metrics["public_housing_net_cashflow"] < 0


def test_migration_responds_to_housing_and_tourism():
    baseline = run(None, 24); boom = run("approve", 24)
    assert boom.state.metrics["permanent_population"] != baseline.state.metrics["permanent_population"]
    assert boom.state.metrics["essential_worker_net_migration"] < baseline.state.metrics["essential_worker_net_migration"]


def test_public_land_sale_is_irreversible_and_lease_retains_control():
    simulation = Simulation.from_default_slice(); sale = simulation.state.parcels["parcel_a"]; lease = simulation.state.parcels["parcel_b"]
    simulation.apply_land_decision("parcel_a", "sale_freehold"); simulation.apply_land_decision("parcel_b", "lease_ground")
    assert sale.tenure == "sold" and lease.tenure == "leased" and sale.public_control is False and lease.public_control is True
    with pytest.raises(ValueError): simulation.apply_land_decision("parcel_a", "lease_ground")


def test_migration_and_state_are_deterministic():
    assert run("renegotiate", 36).state.snapshot() == run("renegotiate", 36).state.snapshot()


def test_invariants_hold_after_long_run():
    state = run("approve", 120).state
    assert all(c.population >= 0 for c in state.migration.values())
    assert all(p.tenure in {"available", "reserved", "leased", "sold"} for p in state.parcels.values())
    assert all(d.residential_units + d.short_term_rental_units <= d.housing_units for d in state.districts.values())
    assert state.metrics["permanent_population"] >= 0
