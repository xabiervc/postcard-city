from __future__ import annotations

from postcard_city.simulation import Simulation


def test_events_are_resolved_at_most_once():
    simulation = Simulation.from_default_slice(seed=17)
    state = simulation.run(36)
    assert len(state.event_history) == len(set(state.event_history))
