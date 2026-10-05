from __future__ import annotations

import math

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
