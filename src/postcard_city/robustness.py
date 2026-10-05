from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .mechanisms import card_by_id, resolve_configuration


@dataclass(frozen=True)
class RobustnessResult:
    card_id: str
    configuration_id: str | None
    context: dict[str, Any]
    samples: int
    target: str
    values: tuple[float, ...]
    classification: str

    def as_dict(self) -> dict[str, Any]:
        return {"card_id": self.card_id, "configuration_id": self.configuration_id, "context": self.context, "samples": self.samples, "target": self.target, "values": list(self.values), "min": min(self.values) if self.values else None, "max": max(self.values) if self.values else None, "classification": self.classification}


def _classify(values: list[float]) -> str:
    if not values: return "not-evaluable"
    if all(value >= 0 for value in values): return "robust"
    if any(value >= 0 for value in values): return "context-dependent"
    return "fragile"


def sweep_card(card_id: str, context: dict[str, Any], target: str | None = None, steps: int = 3) -> list[RobustnessResult]:
    card = card_by_id(card_id); configuration = resolve_configuration(card, context)
    if not configuration: return [RobustnessResult(card_id, None, context, 0, target or "none", (), "not-evaluable")]
    outcomes = [outcome for outcome in configuration.get("outcomes", []) if target is None or outcome["target"] == target]
    results = []
    for outcome in outcomes:
        low, high = outcome["low"], outcome["high"]
        values = tuple(low + (high - low) * index / max(steps - 1, 1) for index in range(steps))
        results.append(RobustnessResult(card_id, configuration["id"], context, steps, outcome["target"], values, _classify(list(values))))
    return results


def run_vertical_slice_report() -> dict[str, Any]:
    contexts = {"low_capacity": {"enforcement_capacity": 0.2, "tourism_pressure": 0.8, "arrears_support": 0.2, "construction_capacity": 0.4, "fiscal_stress": 0.8, "administrative_capacity": 0.4}, "balanced": {"enforcement_capacity": 0.8, "tourism_pressure": 0.8, "arrears_support": 0.8, "construction_capacity": 0.8, "fiscal_stress": 0.4, "administrative_capacity": 0.8}, "high_capacity": {"enforcement_capacity": 0.9, "tourism_pressure": 0.4, "arrears_support": 0.9, "construction_capacity": 0.9, "fiscal_stress": 0.2, "administrative_capacity": 0.9}}
    report = {"contexts": contexts, "results": []}
    for context_id, context in contexts.items():
        for card_id in ("str-regulation", "social-housing", "public-land-disposal"):
            for result in sweep_card(card_id, context):
                item = result.as_dict(); item["context_id"] = context_id; report["results"].append(item)
    return report


def write_report(path: str | Path) -> None:
    output = Path(path); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(run_vertical_slice_report(), indent=2), encoding="utf-8")
