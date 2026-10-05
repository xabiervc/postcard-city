from postcard_city.model import Decision
from postcard_city.simulation import Simulation


def test_same_seed_and_decisions_are_reproducible():
    decisions = [Decision("aurora_leisure_proposal", "renegotiate")]
    first = Simulation.from_default_slice(4821).run(12, decisions).snapshot()
    second = Simulation.from_default_slice(4821).run(12, decisions).snapshot()
    assert first == second


def test_different_decisions_produce_different_states():
    approved = Simulation.from_default_slice(4821).run(
        12, [Decision("aurora_leisure_proposal", "approve")]
    ).snapshot()
    rejected = Simulation.from_default_slice(4821).run(
        12, [Decision("aurora_leisure_proposal", "reject")]
    ).snapshot()
    assert approved != rejected
    assert approved["tourism_visitors"] > rejected["tourism_visitors"]


def test_safeguarded_project_improves_diversity_and_limits_conversion():
    simulation = Simulation.from_default_slice()
    simulation.run(12, [Decision("aurora_leisure_proposal", "renegotiate")])
    core = simulation.state.districts["historic_core"]
    assert simulation.state.economic_diversity > 0.34
    assert core.short_term_rental_units < 34_000 + 500


def test_unknown_decision_is_rejected():
    simulation = Simulation.from_default_slice()
    try:
        simulation.apply_decision(Decision("unknown", "approve"))
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown decisions must fail clearly")
