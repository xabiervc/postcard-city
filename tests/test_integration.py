from __future__ import annotations

import math

from postcard_city.simulation import Simulation


def test_budget_land_housing_and_traces_integrate():
    simulation = Simulation.from_default_slice(seed=17)
    parcel_id = next(parcel_id for parcel_id, parcel in simulation.state.parcels.items() if parcel.public_control and parcel.tenure == "available")
    initial_budget = simulation.state.budget

    simulation.apply_land_decision(parcel_id, "lease_ground")
    after_land_budget = simulation.state.budget
    assert after_land_budget > initial_budget
    assert any(trace.source == "land:lease_ground" and trace.target == "budget" for trace in simulation.state.traces)

    units = 10
    construction_cost = units * simulation.housing_parameters["construction_cost_per_unit"]
    simulation.start_social_housing(units)
    assert simulation.state.budget == after_land_budget - construction_cost
    assert any(trace.source == "social_housing_construction" and trace.target == "budget" for trace in simulation.state.traces)

    simulation.run(simulation.state.social_housing.construction_months)
    assert simulation.state.month == simulation.state.social_housing.construction_months
    assert simulation.state.social_housing.construction_progress == 1.0
    assert simulation.state.social_housing.occupied_units == units
    assert math.isfinite(simulation.state.budget)
    assert any(trace.source == "social_housing" and trace.target == "budget" for trace in simulation.state.traces)
