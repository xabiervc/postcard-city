from pathlib import Path

ROOT = Path(__file__).parents[1]
CONTRACT = ROOT / "docs" / "shared-state-and-precedence-contract.md"


def contract_text():
    return CONTRACT.read_text(encoding="utf-8")


def test_precedence_order_is_explicit_and_ordered():
    text = contract_text()
    priorities = [
        "immediate protection of life",
        "continuity of essential services",
        "preservation of administrative and infrastructure capacity",
        "legally binding transfers",
        "stabilization of legitimacy",
        "discretionary reforms",
    ]
    positions = [text.index(item) for item in priorities]
    assert positions == sorted(positions)


def test_capacity_shortfall_requires_observable_deficit_data():
    text = contract_text()
    for phrase in (
        "records the deficit",
        "affected population",
        "deferred action",
        "duration",
        "confidence interval",
        "explicit shortfall decision",
    ):
        assert phrase in text


def test_invariants_for_bounds_and_rejected_actions_are_documented():
    text = contract_text()
    for phrase in (
        "negative budgets",
        "service availability above 100",
        "stable reason code",
        "trace identifier",
        "reproduces the same state and trace",
    ):
        assert phrase in text
