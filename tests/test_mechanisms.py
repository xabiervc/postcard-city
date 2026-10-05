import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]


def test_evidence_and_mechanism_data_validate():
    evidence_schema = json.loads((ROOT / "schemas/evidence-record.schema.json").read_text())
    mechanism_schema = json.loads((ROOT / "schemas/mechanism-card.schema.json").read_text())
    evidence = json.loads((ROOT / "data/evidence/evidence-registry.json").read_text())
    cards = json.loads((ROOT / "data/mechanisms/housing-policy-cards.json").read_text())
    ids = {record["id"] for record in evidence["records"]}
    for record in evidence["records"]:
        assert list(Draft202012Validator(evidence_schema).iter_errors(record)) == []
    for card in cards["cards"]:
        assert list(Draft202012Validator(mechanism_schema).iter_errors(card)) == []
        assert set(card["evidence_ids"]) <= ids
        for configuration in card["configurations"]:
            for outcome in configuration["outcomes"]:
                refs = set(outcome.get("evidence_ids", [])) | set(outcome.get("alternative_evidence_ids", []))
                assert refs <= ids
                assert refs or outcome.get("assumed", False)


def test_expected_card_set_is_complete():
    cards = json.loads((ROOT / "data/mechanisms/housing-policy-cards.json").read_text())
    assert {card["id"] for card in cards["cards"]} == {
        "str-regulation", "social-housing", "public-land-disposal",
        "public-housing-disposal", "rent-regulation", "upzoning", "expropriation",
    }
