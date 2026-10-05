from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_SCENARIO_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "scenarios" / "the-overheated-destination.json"
)

DISTRICT_FIELDS = {
    "id", "population", "housing_units", "residential_units", "short_term_rental_units",
    "average_rent", "jobs", "healthcare_capacity", "healthcare_staff", "transport_reliability",
}
EFFECT_FIELDS = {
    "project_status", "budget_delta", "tourism_multiplier", "political_support_delta",
    "institutional_trust_delta", "economic_diversity_delta", "reason",
}


class ScenarioValidationError(ValueError):
    pass


def load_scenario(path: str | Path = DEFAULT_SCENARIO_PATH) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    validate_scenario(data)
    return data


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ScenarioValidationError(message)


def validate_scenario(data: dict[str, Any]) -> None:
    required = {
        "schema_version", "id", "title", "default_seed", "region", "initial_state",
        "parameters", "project_profiles", "decisions", "events",
    }
    missing = required - data.keys()
    _require(not missing, f"Missing scenario fields: {sorted(missing)}")
    _require(data["schema_version"] == 1, "Unsupported scenario schema_version")

    districts = data["region"].get("districts", [])
    _require(len(districts) >= 2, "A scenario needs at least two districts")
    ids = [district.get("id") for district in districts]
    _require(len(ids) == len(set(ids)), "District ids must be unique")
    _require("historic_core" in ids and "outer_district" in ids,
             "The vertical slice requires historic_core and outer_district")
    for district in districts:
        absent = DISTRICT_FIELDS - district.keys()
        _require(not absent, f"District {district.get('id')} missing fields: {sorted(absent)}")
        _require(
            district["residential_units"] + district["short_term_rental_units"] <= district["housing_units"],
            f"District {district['id']} has more used units than housing units",
        )
        _require(0.0 <= district["transport_reliability"] <= 1.0,
                 f"District {district['id']} transport_reliability must be within 0..1")
        _require(district["healthcare_staff"] >= 0 and district["healthcare_capacity"] > 0,
                 f"District {district['id']} has invalid healthcare values")

    statuses = set(data["project_profiles"])
    _require(data["initial_state"]["project_status"] in statuses, "Unknown initial project_status")
    for status, profile in data["project_profiles"].items():
        absent = {"growth_bonus", "conversion_rate", "transport_bonus"} - profile.keys()
        _require(not absent, f"Project profile {status} missing fields: {sorted(absent)}")

    _require(len(data["decisions"]) >= 1, "A scenario must define at least one decision")
    decision_ids = [decision.get("id") for decision in data["decisions"]]
    _require(len(decision_ids) == len(set(decision_ids)), "Decision ids must be unique")
    for decision in data["decisions"]:
        _require("options" in decision, f"Decision missing options: {decision.get('id')}")
        _require(len(decision["options"]) >= 2, f"Decision needs at least two options: {decision['id']}")
        option_ids = [option.get("id") for option in decision["options"]]
        _require(len(option_ids) == len(set(option_ids)), f"Duplicate option ids in {decision['id']}")
        for option in decision["options"]:
            _require("label_key" in option, f"Option {option.get('id')} missing label_key")
            effects = option.get("effects", {})
            unknown = set(effects) - EFFECT_FIELDS
            _require(not unknown, f"Option {option['id']} has unknown effects: {sorted(unknown)}")
            status = effects.get("project_status")
            _require(status is None or status in statuses,
                     f"Option {option['id']} references unknown project_status {status}")

    event_ids = [event.get("id") for event in data["events"]]
    _require(len(event_ids) == len(set(event_ids)), "Event ids must be unique")
