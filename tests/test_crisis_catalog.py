import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
SCHEMA_PATH = ROOT / "docs" / "crisis-catalog.schema.json"
DOC_PATH = ROOT / "docs" / "crisis-and-risk-system.md"
CATALOG_PATH = ROOT / "docs" / "crisis-catalog.md"


def test_crisis_schema_is_valid_json():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["type"] == "object"
    assert set(schema["required"]) == {
        "id", "family", "minimum_level", "severity", "phases",
        "signals", "consequences", "decisions",
    }


def test_crisis_schema_has_all_event_families_and_levels():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert set(schema["properties"]["family"]["enum"]) == {
        "natural", "infrastructure", "accident", "public_health",
        "deliberate_violence", "geopolitical", "economic",
    }
    assert set(schema["properties"]["minimum_level"]["enum"]) == {
        "relaxed", "standard", "advanced", "expert",
    }


def test_crisis_schema_requires_all_lifecycle_phases():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    phases = schema["properties"]["phases"]
    assert phases["minItems"] == 4
    assert phases["maxItems"] == 4
    assert phases["items"]["enum"] == ["prevention", "preparedness", "response", "recovery"]


def test_crisis_document_states_safety_and_vertical_slice_rules():
    text = DOC_PATH.read_text(encoding="utf-8")
    for phrase in (
        "No gore", "Biological hazards", "Terrorism and war",
        "content filtering", "first vertical slice",
    ):
        assert phrase in text


def test_expanded_crisis_catalog_covers_broad_families():
    text = CATALOG_PATH.read_text(encoding="utf-8")
    for phrase in (
        "Natural and environmental",
        "Buildings and infrastructure",
        "Transport and industrial",
        "Health and care",
        "Safety, crime, and social cohesion",
        "Geopolitical and migration",
        "Economic and institutional",
        "Housing and demographic",
    ):
        assert phrase in text


def test_expanded_catalog_includes_slow_and_non_disaster_crises():
    text = CATALOG_PATH.read_text(encoding="utf-8")
    for phrase in (
        "vacancy trap",
        "corruption investigation",
        "youth exodus",
        "mental-health emergency",
        "data breach",
        "misinformation",
    ):
        assert phrase in text
