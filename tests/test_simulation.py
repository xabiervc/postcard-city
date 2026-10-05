from postcard_city.model import Decision
from postcard_city.simulation import Simulation


def test_same_seed_and_decisions_are_reproducible():
    first = Simulation.from_default_slice(4821)
    second = Simulation.from_default_slice(4821)
    for month in range(1, 13):
        if month == 1:
            decision = Decision("aurora_leisure_proposal", "renegotiate")
            first.apply_decision(decision)
            second.apply_decision(decision)
        first.advance_month()
        second.advance_month()
    assert first.state.snapshot() == second.state.snapshot()


def test_different_decisions_produce_different_states():
    approved = Simulation.from_default_slice(4821)
    rejected = Simulation.from_default_slice(4821)
    approved.apply_decision(Decision("aurora_leisure_proposal", "approve"))
    rejected.apply_decision(Decision("aurora_leisure_proposal", "reject"))
    for _ in range(12):
        approved.advance_month()
        rejected.advance_month()
    assert approved.state.snapshot() != rejected.state.snapshot()
    assert approved.state.tourism_visitors > rejected.state.tourism_visitors


def test_safeguarded_project_improves_diversity_and_limits_conversion():
    simulation = Simulation.from_default_slice()
    simulation.apply_decision(Decision("aurora_leisure_proposal", "renegotiate"))
    for _ in range(12):
        simulation.advance_month()
    core = simulation.state.districts["historic_core"]
    assert simulation.state.economic_diversity > 0.34
    assert core.short_term_rental_units < 34_000 + 500


def test_trace_explains_core_effects():
    simulation = Simulation.from_default_slice()
    simulation.apply_decision(Decision("aurora_leisure_proposal", "approve"))
    simulation.advance_month()
    targets = {trace.target for trace in simulation.state.traces}
    assert "budget" in targets
    assert "tourism_visitors" in targets
    assert "historic_core.residential_units" in targets


def test_unknown_decision_is_rejected():
    simulation = Simulation.from_default_slice()
    try:
        simulation.apply_decision(Decision("unknown", "approve"))
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown decisions must fail clearly")
