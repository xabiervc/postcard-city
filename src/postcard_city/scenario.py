from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_SCENARIO_PATH = Path(__file__).resolve().parents[2] / "data" / "scenarios" / "the-overheated-destination.json"

class ScenarioValidationError(ValueError):
    pass


ALLOWED_EFFECTS = {
    "budget_delta",
    "tourism_multiplier",
    "political_support_delta",
    "institutional_trust_delta",
    "economic_diversity_delta",
    "project_status",
    "reason",
}


def load_scenario(path: str | Path = DEFAULT_SCENARIO_PATH) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    validate_scenario(data)
    return data


def validate_scenario(data: dict[str, Any]) -> None:
    required = {"schema_version", "id", "title", "default_seed", "region", "initial_state", "parameters", "project_profiles", "decisions", "events", "parcels", "migration", "housing"}
    missing = required - data.keys()
    if missing:
        raise ScenarioValidationError(f"Missing scenario fields: {sorted(missing)}")
    if data["schema_version"] != 2:
        raise ScenarioValidationError("Unsupported scenario schema_version")

    districts = data["region"].get("districts", [])
    if len(districts) != 2:
        raise ScenarioValidationError("Scenario must contain exactly two districts")
    ids = [d["id"] for d in districts]
    if len(ids) != len(set(ids)) or not {"historic_core", "outer_district"} <= set(ids):
        raise ScenarioValidationError("Invalid district ids")

    for district in districts:
        required_district = {"id", "housing_units", "residential_units", "short_term_rental_units", "transport_reliability"}
        if not required_district <= district.keys():
            raise ScenarioValidationError(f"Incomplete district: {district.get('id')}")
        units = district["residential_units"]
        if not isinstance(units, int) or isinstance(units, bool) or not 0 <= units <= 1_000_000:
            raise ScenarioValidationError(f"Invalid residential units in {district['id']}")
        if district["residential_units"] + district["short_term_rental_units"] > district["housing_units"]:
            raise ScenarioValidationError(f"Overallocated housing in {district['id']}")
        if not 0 <= district["transport_reliability"] <= 1:
            raise ScenarioValidationError(f"Invalid transport in {district['id']}")

    statuses = set(data["project_profiles"])
    if data["initial_state"]["project_status"] not in statuses:
        raise ScenarioValidationError("Unknown initial project status")

    parcel_ids = [parcel["id"] for parcel in data["parcels"]]
    if len(parcel_ids) != len(set(parcel_ids)):
        raise ScenarioValidationError("Duplicate parcel ids")
    if any(parcel["district_id"] not in ids for parcel in data["parcels"]):
        raise ScenarioValidationError("Parcel references unknown district")

    cohort_ids = [cohort["id"] for cohort in data["migration"]["cohorts"]]
    if len(cohort_ids) != len(set(cohort_ids)):
        raise ScenarioValidationError("Duplicate cohort ids")

    social = data["housing"]["social_housing"]
    if not 0 <= social["arrears_rate"] <= 1 or not 0 <= social["essential_worker_share"] <= 1:
        raise ScenarioValidationError("Invalid social-housing rate")

    for decision in data["decisions"]:
        options = decision.get("options", [])
        if len(options) < 2:
            raise ScenarioValidationError(f"Decision needs two options: {decision.get('id')}")
        for option in options:
            effects = option.get("effects", {})
            unknown = set(effects) - ALLOWED_EFFECTS
            if unknown:
                raise ScenarioValidationError(f"Unknown effects in {option.get('id')}: {sorted(unknown)}")
            status = effects.get("project_status")
            if status is not None and status not in statuses:
                raise ScenarioValidationError(f"Unknown project status: {status}")

    event_ids = [event["id"] for event in data["events"]]
    if len(event_ids) != len(set(event_ids)):
        raise ScenarioValidationError("Duplicate event ids")
