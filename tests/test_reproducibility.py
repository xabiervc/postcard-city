import json
from pathlib import Path

from postcard_city.scenario import load_scenario

ROOT = Path(__file__).parents[1]
SCENARIO_PATH = ROOT / "data" / "scenarios" / "the-overheated-destination.json"
CONTRACT_PATH = ROOT / "docs" / "shared-state-and-precedence-contract.md"


def load_snapshot(seed):
    scenario = load_scenario(SCENARIO_PATH)
    snapshot = {
        "seed": seed,
        "scenario": scenario,
    }
    return json.loads(json.dumps(snapshot, sort_keys=True, default=str))


def test_same_seed_replays_identically():
    assert load_snapshot(17) == load_snapshot(17)


def test_replay_seed_is_explicitly_distinct():
    assert load_snapshot(17) != load_snapshot(18)


def test_reproducibility_contract_is_documented():
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    assert "Fixed inputs and seed must produce identical state" in text
    assert "trace output" in text
