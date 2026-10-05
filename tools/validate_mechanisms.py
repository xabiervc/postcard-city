from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from postcard_city.scenario import _require

ROOT = Path(__file__).resolve().parents[1]


def validate() -> None:
    evidence_schema = json.loads((ROOT / "schemas/evidence-record.schema.json").read_text(encoding="utf-8"))
    mechanism_schema = json.loads((ROOT / "schemas/mechanism-card.schema.json").read_text(encoding="utf-8"))
    evidence = json.loads((ROOT / "data/evidence/evidence-registry.json").read_text(encoding="utf-8"))
    cards = json.loads((ROOT / "data/mechanisms/housing-policy-cards.json").read_text(encoding="utf-8"))
    evidence_ids = set()
    for record in evidence["records"]:
        errors = list(Draft202012Validator(evidence_schema).iter_errors(record))
        _require(not errors, f"Invalid evidence record {record.get('id')}: {errors}")
        evidence_ids.add(record["id"])
    for card in cards["cards"]:
        errors = list(Draft202012Validator(mechanism_schema).iter_errors(card))
        _require(not errors, f"Invalid mechanism card {card.get('id')}: {errors}")
        _require(set(card["evidence_ids"]) <= evidence_ids, f"Unknown evidence in {card['id']}")
        for configuration in card["configurations"]:
            for outcome in configuration["outcomes"]:
                refs = set(outcome.get("evidence_ids", [])) | set(outcome.get("alternative_evidence_ids", []))
                _require(refs <= evidence_ids, f"Unknown outcome evidence in {card['id']}")
                if not outcome.get("assumed", False):
                    _require(refs, f"Unreferenced empirical outcome in {card['id']}")
        for behavior in card["expected_behaviours"]:
            _require(set(behavior.get("evidence_ids", [])) <= evidence_ids,
                     f"Unknown behavior evidence in {card['id']}")
    print(f"Validated {len(evidence['records'])} evidence records and {len(cards['cards'])} mechanism cards")


if __name__ == "__main__":
    validate()
