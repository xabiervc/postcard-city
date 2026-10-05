from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_SCENARIO_PATH = Path(__file__).resolve().parents[2] / "data" / "scenarios" / "the-overheated-destination.json"

class ScenarioValidationError(ValueError):
    pass


def load_scenario(path: str | Path = DEFAULT_SCENARIO_PATH) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    validate_scenario(data)
    return data


def validate_scenario(data: dict[str, Any]) -> None:
    required = {"schema_version", "id", "title", "default_seed", "region", "initial_state", "parameters", "project_profiles", "decisions", "events", "parcels", "migration", "housing"}
    missing = required - data.keys()
    if missing: raise ScenarioValidationError(f"Missing scenario fields: {sorted(missing)}")
    if data["schema_version"] != 2: raise ScenarioValidationError("Unsupported scenario schema_version")
    districts = data["region"]["districts"]
    ids = [d["id"] for d in districts]
    if len(ids) != len(set(ids)) or not {"historic_core", "outer_district"} <= set(ids): raise ScenarioValidationError("Invalid district ids")
    for d in districts:
        if d["residential_units"] + d["short_term_rental_units"] > d["housing_units"]: raise ScenarioValidationError(f"Overallocated housing in {d['id']}")
        if not 0 <= d["transport_reliability"] <= 1: raise ScenarioValidationError(f"Invalid transport in {d['id']}")
    statuses = set(data["project_profiles"])
    if data["initial_state"]["project_status"] not in statuses: raise ScenarioValidationError("Unknown initial project status")
    parcel_ids = [p["id"] for p in data["parcels"]]
    if len(parcel_ids) != len(set(parcel_ids)): raise ScenarioValidationError("Duplicate parcel ids")
    if any(p["district_id"] not in ids for p in data["parcels"]): raise ScenarioValidationError("Parcel references unknown district")
    cohort_ids = [c["id"] for c in data["migration"]["cohorts"]]
    if len(cohort_ids) != len(set(cohort_ids)): raise ScenarioValidationError("Duplicate cohort ids")
    social = data["housing"]["social_housing"]
    if not 0 <= social["arrears_rate"] <= 1 or not 0 <= social["essential_worker_share"] <= 1: raise ScenarioValidationError("Invalid social-housing rate")
    for decision in data["decisions"]:
        if len(decision.get("options", [])) < 2: raise ScenarioValidationError(f"Decision needs two options: {decision.get('id')}")
