from __future__ import annotations

import math

import pytest

from postcard_city.model import Decision
from postcard_city.simulation import Simulation


def test_events_are_resolved_at_most_once():
    simulation = Simulation.from_default_slice(seed=17)
    state = simulation.run(36)
    assert len(state.event_history) == len(set(state.event_history))


def test_long_run_preserves_state_invariants():
    simulation = Simulation.from_default_slice(seed=17)
    state = simulation.run(36)

    assert 0 <= state.institutional_trust <= 1
    assert 0 <= state.political_support <= 1
    assert 0 <= state.economic_diversity <= 1
    assert math.isfinite(state.budget)
    assert math.isfinite(state.tourism_visitors)

    for district in state.districts.values():
        assert 0 <= district.transport_reliability <= 1
        assert 0 <= district.residential_units <= district.housing_units
        assert 0 <= district.short_term_rental_units <= district.housing_units
        assert district.residential_units + district.short_term_rental_units <= district.housing_units


def test_run_requires_positive_months():
    simulation = Simulation.from_default_slice(seed=17)
    with pytest.raises(ValueError):
        simulation.run(0)
    with pytest.raises(ValueError):
        simulation.run(-1)


def test_run_rejects_decisions_outside_requested_range():
    simulation = Simulation.from_default_slice(seed=17)
    decision = Decision("project_direction", "high_growth")
    with pytest.raises(ValueError):
        simulation.run(2, scheduled=[(3, decision)])


def test_duplicate_decisions_are_rejected():
    simulation = Simulation.from_default_slice(seed=17)
    decision = Decision("project_direction", "high_growth")
    simulation.apply_decision(decision)
    with pytest.raises(ValueError):
        simulation.apply_decision(decision)


def test_land_and_housing_boundaries_are_rejected():
    simulation = Simulation.from_default_slice(seed=17)
    with pytest.raises(ValueError):
        simulation.apply_land_decision("unknown", "lease_ground")
    with pytest.raises(ValueError):
        simulation.apply_land_decision(next(iter(simulation.state.parcels)), "unknown")
    with pytest.raises(ValueError):
        simulation.start_social_housing(0)
    with pytest.raises(ValueError):
        simulation.start_social_housing(-1)


def test_second_social_housing_project_is_rejected():
    simulation = Simulation.from_default_slice(seed=17)
    simulation.start_social_housing(1)
    with pytest.raises(ValueError):
        simulation.start_social_housing(1)
