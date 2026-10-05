from postcard_city.mechanisms import card_by_id, resolve_configuration
from postcard_city.robustness import run_vertical_slice_report, sweep_card


def test_cards_resolve_by_context():
    card = card_by_id("str-regulation")
    high = resolve_configuration(card, {"enforcement_capacity": 0.9, "tourism_pressure": 0.8})
    low = resolve_configuration(card, {"enforcement_capacity": 0.1, "tourism_pressure": 0.8})
    assert high["id"] == "credible-enforcement"
    assert low["id"] == "weak-enforcement"


def test_sweep_is_deterministic_and_classified():
    first = [result.as_dict() for result in sweep_card("str-regulation", {"enforcement_capacity": 0.9, "tourism_pressure": 0.8})]
    second = [result.as_dict() for result in sweep_card("str-regulation", {"enforcement_capacity": 0.9, "tourism_pressure": 0.8})]
    assert first == second
    assert first[0]["classification"] in {"robust", "context-dependent", "fragile", "not-evaluable"}


def test_vertical_slice_report_contains_all_contexts_and_cards():
    report = run_vertical_slice_report()
    assert len(report["contexts"]) == 3
    cards = {item["card_id"] for item in report["results"]}
    assert cards == {"str-regulation", "social-housing", "public-land-disposal"}
