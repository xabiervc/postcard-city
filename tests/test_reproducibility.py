import dataclasses
import json
from pathlib import Path

from postcard_city.simulation import Simulation

ROOT = Path(__file__).parents[1]
SCENARIO_PATH = ROOT / "data" / "scenarios" / "the-overheated-destination.json"
CONTRACT_PATH = ROOT / "docs" / "shared-state-and-precedence-contract.md"


def normalize(value):
    if dataclasses.is_dataclass(value):
        return {key: normalize(item) for key, item in vars(value).items()}
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    return value


def run_replay(seed):
    simulation = Simulation.from_scenario_file(SCENARIO_PATH, seed=seed)
    return normalize(simulation.run(12))


def test_same_seed_replays_identically():
    assert run_replay(17) == run_replay(17)


def test_replay_seed_is_explicitly_distinct():
    assert run_replay(17) != run_replay(18)


def test_reproducibility_contract_is_documented():
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    assert "Fixed inputs and seed must produce identical state" in text
    assert "trace output" in text
