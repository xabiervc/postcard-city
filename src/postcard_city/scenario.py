from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ScenarioValidationError(ValueError):
    pass


def load_scenario(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    with source.open(encoding="utf-8") as handle:
        data = json.load(handle)
    validate_scenario(data)
    return data


def validate_scenario(data: dict[str, Any]) -> None:
    required = {"id", "title", "region", "decisions"}
    missing = required - data.keys()
    if missing:
        raise ScenarioValidationError(f"Missing scenario fields: {sorted(missing)}")
    if not data["decisions"]:
        raise ScenarioValidationError("A scenario must define at least one decision")
    for decision in data["decisions"]:
        for field in ("id", "options"):
            if field not in decision:
                raise ScenarioValidationError(f"Decision missing field: {field}")
        if len(decision["options"]) < 2:
            raise ScenarioValidationError(f"Decision needs at least two options: {decision['id']}")
