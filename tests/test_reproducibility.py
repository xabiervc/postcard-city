import json
from pathlib import Path

from postcard_city.scenario import load_scenario
from postcard_city.simulation import simulate_year

SCENARIO_PATH = Path(__file__).parents[1] / "data" / "scenarios" / "the-overheated-destination.json"


def run_replay(seed):
    scenario = load_scenario(SCENARIO_PATH)
    outputs = []
    for _ in range(3):
        result = simulate_year(scenario, seed=seed)
        outputs.append(result)
    return json.loads(json.dumps(outputs, sort_keys=True, default=str))


def test_same_seed_replays_identically():
    assert run_replay(17) == run_replay(17)


def test_replay_seed_is_explicitly_distinct():
    assert run_replay(17) != run_replay(18)


def test_reproducibility_contract_is_documented():
    path = Path(__file__).parents[1] / "docs" / "shared-state-and-precedence-contract.md"
    text = path.read_text(encoding="utf-8")
    assert "Fixed inputs and seed must produce identical state" in text
    assert "trace output" in text
