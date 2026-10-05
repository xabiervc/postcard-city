from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .scenario import ScenarioValidationError

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_PATH = ROOT / "data" / "evidence" / "evidence-registry.json"
CARDS_PATH = ROOT / "data" / "mechanisms" / "housing-policy-cards.json"


def load_policy_cards(path: str | Path = CARDS_PATH) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def load_evidence(path: str | Path = EVIDENCE_PATH) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def card_by_id(card_id: str, cards: dict[str, Any] | None = None) -> dict[str, Any]:
    cards = cards or load_policy_cards()
    for card in cards["cards"]:
        if card["id"] == card_id:
            return card
    raise ScenarioValidationError(f"Unknown mechanism card: {card_id}")


def evidence_by_id(evidence_id: str, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    evidence = evidence or load_evidence()
    for record in evidence["records"]:
        if record["id"] == evidence_id:
            return record
    raise ScenarioValidationError(f"Unknown evidence record: {evidence_id}")


def _matches(condition: dict[str, Any], context: dict[str, Any]) -> bool:
    variable = condition["variable"]
    relation = condition["relation"]
    value = context.get(variable)
    if value is None:
        return False
    if relation in {"high", "medium_or_high", "low"}:
        threshold = {"low": 0.35, "medium_or_high": 0.5, "high": 0.65}[relation]
        return value >= threshold if relation != "low" else value < threshold
    if relation == "positive":
        return value > 0
    if relation == "negative":
        return value < 0
    return True


def resolve_configuration(card: dict[str, Any], context: dict[str, Any]) -> dict[str, Any] | None:
    scored: list[tuple[int, dict[str, Any]]] = []
    for configuration in card["configurations"]:
        conditions = configuration.get("context", [])
        score = sum(1 for condition in conditions if _matches(condition, context))
        if score == len(conditions):
            scored.append((score, configuration))
    return max(scored, key=lambda item: item[0])[1] if scored else None


def evidence_summary(configuration: dict[str, Any], evidence: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    evidence = evidence or load_evidence()
    ids: set[str] = set()
    for outcome in configuration.get("outcomes", []):
        ids.update(outcome.get("evidence_ids", []))
        ids.update(outcome.get("alternative_evidence_ids", []))
    return [{"id": item, "title": evidence_by_id(item, evidence)["title"], "certainty": evidence_by_id(item, evidence).get("certainty")} for item in sorted(ids)]
