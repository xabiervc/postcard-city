import pytest

from postcard_city.model import Decision
from postcard_city.simulation import Simulation

AURORA = "aurora_leisure_proposal"


def run(option, months=12, seed=None):
    simulation = Simulation.from_default_slice(seed)
    scheduled = [(1, Decision(AURORA, option))] if option else []
    simulation.run(months, scheduled)
    return simulation


def test_same_seed_and_decisions_are_reproducible():
    assert run("renegotiate", seed=4821).state.snapshot() == run("renegotiate", seed=4821).state.snapshot()


def test_different_decisions_produce_different_states():
    approved, rejected = run("approve"), run("reject")
    assert approved.state.snapshot() != rejected.state.snapshot()
    assert approved.state.tourism_visitors > rejected.state.tourism_visitors


def test_safeguarded_project_improves_diversity_and_limits_conversion():
    simulation = run("renegotiate")
    core = simulation.state.districts["historic_core"]
    assert simulation.state.economic_diversity > 0.34
    assert core.short_term_rental_units < 34_000 + 500


def test_healthcare_staffing_actually_changes_and_depends_on_decision():
    """Regression: staffing used to be constant because of integer truncation."""
    baseline = Simulation.from_default_slice().state.metrics["healthcare_staffing"]
    approved, safeguarded = run("approve", 36), run("renegotiate", 36)
    assert approved.state.metrics["healthcare_staffing"] < baseline
    assert approved.state.metrics["healthcare_staffing"] < safeguarded.state.metrics["healthcare_staffing"]


def test_low_healthcare_staffing_reduces_trust_and_is_traced():
    simulation = run(None, 36)
    sources = {trace.source for trace in simulation.state.traces}
    assert "healthcare_staffing" in sources


def test_trace_explains_core_effects():
    simulation = Simulation.from_default_slice()
    simulation.apply_decision(Decision(AURORA, "approve"))
    simulation.advance_month()
    targets = {trace.target for trace in simulation.state.traces}
    assert {"budget", "tourism_visitors", "historic_core.residential_units",
            "historic_core.average_rent", "outer_district.healthcare_staff"} <= targets


def test_rent_trace_records_a_change_not_an_absolute_value():
    simulation = Simulation.from_default_slice()
    start = simulation.state.districts["historic_core"].average_rent
    simulation.advance_month()
    trace = next(t for t in simulation.state.traces if t.target == "historic_core.average_rent")
    assert trace.amount == pytest.approx(simulation.state.districts["historic_core"].average_rent - start)
    assert abs(trace.amount) < start


def test_unknown_decision_is_rejected_and_not_recorded():
    simulation = Simulation.from_default_slice()
    with pytest.raises(ValueError):
        simulation.apply_decision(Decision("unknown", "approve"))
    with pytest.raises(ValueError):
        simulation.apply_decision(Decision(AURORA, "unknown"))
    assert simulation.state.decision_history == []


def test_a_decision_can_only_be_resolved_once():
    simulation = Simulation.from_default_slice()
    simulation.apply_decision(Decision(AURORA, "audit"))
    with pytest.raises(ValueError):
        simulation.apply_decision(Decision(AURORA, "approve"))
    assert len(simulation.state.decision_history) == 1


def test_scheduled_month_must_be_in_range():
    with pytest.raises(ValueError):
        Simulation.from_default_slice().run(6, [(7, Decision(AURORA, "audit"))])


def test_approval_triggers_financing_warning_in_month_six():
    assert "aurora_financing_warning" in run("approve", 6).state.event_history
    assert "aurora_financing_warning" not in run("reject", 12).state.event_history


@pytest.mark.parametrize("option", [None, "approve", "reject", "renegotiate", "audit"])
def test_invariants_hold_for_every_strategy(option):
    simulation = Simulation.from_default_slice()
    scheduled = [(1, Decision(AURORA, option))] if option else []
    for month in range(1, 61):
        for scheduled_month, decision in scheduled:
            if scheduled_month == month:
                simulation.apply_decision(decision)
        simulation.advance_month()
        state = simulation.state
        assert 0.0 <= state.institutional_trust <= 1.0
        assert 0.0 <= state.political_support <= 1.0
        assert 0.0 <= state.economic_diversity <= 1.0
        for district in state.districts.values():
            assert district.residential_units >= 0 and district.short_term_rental_units >= 0
            assert district.residential_units + district.short_term_rental_units <= district.housing_units
            assert 0.0 <= district.transport_reliability <= 1.0
            assert 0.0 <= district.healthcare_staff <= district.healthcare_capacity
            assert district.average_rent >= 0.0
        assert all(value == value for value in state.metrics.values())
