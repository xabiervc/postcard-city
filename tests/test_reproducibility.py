import json
from pathlib import Path

from postcard_city.scenario import load_scenario
from postcard_city.simulation import Simulation


def replay_scenario():
    return load_scenario(
        {
            "name": "replay-fixture",
            "population": 1000,
            "housing_units": 500,
            "jobs": 600,
            "budget": 100.0,
            "healthcare_capacity": 100.0,
            "education_capacity": 100.0,
            "transport_capacity": 100.0,
        }
    )


def run_replay(seed):
    simulation = Simulation(replay_scenario(), seed=seed)
    outputs = []
    for _ in range(3):
        result = simulation.step()
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
