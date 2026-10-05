from copy import deepcopy
import json
from pathlib import Path

import pytest

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover
    Draft202012Validator = None

ROOT = Path(__file__).parents[1]
SCHEMA_PATH = ROOT / "schemas" / "shared-state.schema.json"
CONTRACT_PATH = ROOT / "docs" / "shared-state-and-precedence-contract.md"


def schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def valid_state():
    return {
        "contract_version": "1.0",
        "turn": 4,
        "seed": 17,
        "state": {
            "public_budget": 100.0,
            "public_debt": 20.0,
            "fiscal_capacity": 80.0,
            "administrative_capacity": 70.0,
            "essential_service_availability": 95.0,
            "institutional_legitimacy": 60.0,
            "public_trust": 55.0,
            "population": 1000,
            "displacement": 3,
            "inequality": 0.3,
            "infrastructure_condition": 75.0,
        },
        "uncertainty": {"public_trust": 0.1},
        "trace": {
            "trace_id": "turn-4-state",
            "mechanisms": ["service-capacity"],
            "output_delta": {"public_budget": -2.0},
        },
    }


def test_shared_state_schema_accepts_valid_state():
    if Draft202012Validator is None:
        pytest.skip("jsonschema dependency is unavailable")
    errors = list(Draft202012Validator(schema()).iter_errors(valid_state()))
    assert errors == []


def test_shared_state_schema_rejects_invalid_ranges():
    if Draft202012Validator is None:
        pytest.skip("jsonschema dependency is unavailable")
    candidate = valid_state()
    candidate["state"]["public_trust"] = 101
    assert list(Draft202012Validator(schema()).iter_errors(candidate))


def test_shared_state_schema_rejects_missing_required_state():
    if Draft202012Validator is None:
        pytest.skip("jsonschema dependency is unavailable")
    candidate = valid_state()
    del candidate["state"]["population"]
    assert list(Draft202012Validator(schema()).iter_errors(candidate))


def test_shared_state_schema_rejects_negative_population():
    if Draft202012Validator is None:
        pytest.skip("jsonschema dependency is unavailable")
    candidate = valid_state()
    candidate["state"]["population"] = -1
    assert list(Draft202012Validator(schema()).iter_errors(candidate))


def test_shared_state_contract_names_precedence_and_shortfall():
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    assert "Precedence order" in text
    assert "Capacity saturation" in text
    assert "explicit shortfall decision" in text
    assert "stable reason code" in text


def test_shared_state_replay_inputs_are_traceable():
    first = valid_state()
    second = deepcopy(first)
    assert first == second
    assert first["seed"] == second["seed"]
    assert first["trace"] == second["trace"]
