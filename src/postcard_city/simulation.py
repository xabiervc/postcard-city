from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .model import Decision, DistrictState, RegionState, TraceEntry
from .scenario import DEFAULT_SCENARIO_PATH, load_scenario, validate_scenario


@dataclass(frozen=True)
class SimulationConfig:
    monthly_base_tourist_growth: float
    tourist_spend: float
    tourism_tax_rate: float
    monthly_public_cost: float
    healthcare_staffing_threshold: float
    tourist_saturation_visitors: float
    healthcare_staff_sensitivity: float
    healthcare_access_neutral: float
    healthcare_trust_penalty_scale: float
    healthcare_support_penalty_scale: float


class Simulation:
    """Deterministic monthly simulation driven entirely by validated scenario content."""

    def __init__(self, scenario: dict[str, Any], seed: int | None = None):
        validate_scenario(scenario)
        self.scenario = copy.deepcopy(scenario)
        self.config = SimulationConfig(**self.scenario["parameters"])
        self.profiles = self.scenario["project_profiles"]
        self.state = self._build_state(self.scenario, self.scenario["default_seed"] if seed is None else seed)
        self._rng = random.Random(self.state.seed)
        self._resolved_decisions: set[str] = set()
        self._update_metrics(record=False)

    @classmethod
    def from_scenario_file(cls, path: str | Path = DEFAULT_SCENARIO_PATH, seed: int | None = None) -> "Simulation":
        return cls(load_scenario(path), seed)

    @classmethod
    def from_default_slice(cls, seed: int | None = None) -> "Simulation":
        return cls.from_scenario_file(DEFAULT_SCENARIO_PATH, seed)

    @staticmethod
    def _build_state(scenario: dict[str, Any], seed: int) -> RegionState:
        districts = {
            item["id"]: DistrictState(**{**item, "healthcare_staff": float(item["healthcare_staff"])})
            for item in scenario["region"]["districts"]
        }
        initial = scenario["initial_state"]
        return RegionState(
            seed=seed, month=0, budget=float(initial["budget"]),
            tourism_visitors=float(initial["tourism_visitors"]), tourism_revenue=0.0,
            institutional_trust=initial["institutional_trust"],
            political_support=initial["political_support"],
            economic_diversity=initial["economic_diversity"],
            districts=districts, project_status=initial["project_status"],
        )

    def _find_option(self, decision: Decision) -> dict[str, Any]:
        for item in self.scenario["decisions"]:
            if item["id"] == decision.decision_id:
                for option in item["options"]:
                    if option["id"] == decision.option_id:
                        return option
                raise ValueError(f"Unknown option: {decision.option_id}")
        raise ValueError(f"Unknown decision: {decision.decision_id}")

    def apply_decision(self, decision: Decision) -> None:
        option = self._find_option(decision)
        if decision.decision_id in self._resolved_decisions:
            raise ValueError(f"Decision already resolved: {decision.decision_id}")
        self._resolved_decisions.add(decision.decision_id)
        self.state.decision_history.append(decision)
        effects = option["effects"]
        reason = effects.get("reason", "player decision")
        state = self.state
        before = {"budget": state.budget, "tourism_visitors": state.tourism_visitors,
                  "institutional_trust": state.institutional_trust,
                  "political_support": state.political_support,
                  "economic_diversity": state.economic_diversity}
        if "project_status" in effects:
            state.project_status = effects["project_status"]
        state.budget += effects.get("budget_delta", 0.0)
        state.tourism_visitors *= effects.get("tourism_multiplier", 1.0)
        state.political_support += effects.get("political_support_delta", 0.0)
        state.institutional_trust += effects.get("institutional_trust_delta", 0.0)
        state.economic_diversity += effects.get("economic_diversity_delta", 0.0)
        self._clamp_state()
        for key, old in before.items():
            delta = getattr(state, key) - old
            if abs(delta) > 1e-12:
                state.traces.append(TraceEntry(state.month, f"decision:{decision.option_id}", key, delta, reason))

    def advance_month(self) -> RegionState:
        state = self.state
        state.month += 1
        profile = self.profiles[state.project_status]
        before_visitors = state.tourism_visitors
        growth = self.config.monthly_base_tourist_growth + profile["growth_bonus"]
        state.tourism_visitors *= 1.0 + growth
        self._trace("seasonal_and_project_demand", "tourism_visitors", state.tourism_visitors - before_visitors,
                    "monthly tourism demand and project status")
        before_budget = state.budget
        state.tourism_revenue = state.tourism_visitors * self.config.tourist_spend * self.config.tourism_tax_rate
        state.budget += state.tourism_revenue - self.config.monthly_public_cost
        self._trace("tourism_revenue", "budget", state.budget - before_budget,
                    "tourism tax revenue minus recurring public costs")
        self._update_districts(profile)
        self._update_metrics(record=True)
        self._resolve_events()
        self._clamp_state()
        return state

    def run(self, months: int, scheduled: Iterable[tuple[int, Decision]] = ()) -> RegionState:
        by_month: dict[int, list[Decision]] = {}
        for month, decision in scheduled:
            if not 1 <= month <= months:
                raise ValueError(f"Decision month {month} is outside 1..{months}")
            by_month.setdefault(month, []).append(decision)
        for month in range(1, months + 1):
            for decision in by_month.get(month, []):
                self.apply_decision(decision)
            self.advance_month()
        return self.state

    def _trace(self, source: str, target: str, amount: float, reason: str) -> None:
        self.state.traces.append(TraceEntry(self.state.month, source, target, amount, reason))

    def _worker_accessibility(self) -> float:
        core = self.state.districts["historic_core"]
        outer = self.state.districts["outer_district"]
        affordability = max(0.0, 1.0 - core.average_rent / 2_000.0)
        return (outer.transport_reliability + affordability) / 2.0

    def _update_districts(self, profile: dict[str, float]) -> None:
        state = self.state
        core = state.districts["historic_core"]
        outer = state.districts["outer_district"]
        converted = max(0, int(core.residential_units * profile["conversion_rate"]))
        core.residential_units -= converted
        core.short_term_rental_units += converted
        self._trace("tourism_pressure", "historic_core.residential_units", -converted,
                    "visitor growth and project status convert residential capacity to short-term rentals")
        before_rent = core.average_rent
        core.average_rent *= 1.0 + (0.006 if converted else 0.002)
        self._trace("housing_pressure", "historic_core.average_rent", core.average_rent - before_rent,
                    "reduced residential capacity increases rent pressure")
        core.tourist_pressure = min(1.0, state.tourism_visitors / self.config.tourist_saturation_visitors)
        before_transport = outer.transport_reliability
        outer.transport_reliability -= 0.004 * core.tourist_pressure
        outer.transport_reliability += profile["transport_bonus"]
        outer.transport_reliability = min(1.0, max(0.0, outer.transport_reliability))
        self._trace("tourism_pressure", "outer_district.transport_reliability",
                    outer.transport_reliability - before_transport,
                    "tourism load and project safeguards change regional transport reliability")
        access = self._worker_accessibility()
        rate = self.config.healthcare_staff_sensitivity * (access - self.config.healthcare_access_neutral)
        for district in state.districts.values():
            before_staff = district.healthcare_staff
            district.healthcare_staff = min(
                float(district.healthcare_capacity), max(0.0, district.healthcare_staff * (1.0 + rate)))
            self._trace("worker_accessibility", f"{district.id}.healthcare_staff",
                        district.healthcare_staff - before_staff,
                        "housing cost and transport decide whether health workers stay or can be recruited")

    def _update_metrics(self, record: bool) -> None:
        state = self.state
        core = state.districts["historic_core"]
        total_capacity = sum(d.healthcare_capacity for d in state.districts.values())
        total_staff = sum(d.healthcare_staff for d in state.districts.values())
        ratio = total_staff / total_capacity
        state.metrics = {
            "housing_affordability": max(0.0, 1.0 - core.average_rent / 2_000.0),
            "worker_accessibility": self._worker_accessibility(),
            "healthcare_staffing": ratio,
            "tourism_pressure": core.tourist_pressure,
            "budget_millions": state.budget / 1_000_000.0,
        }
        shortfall = self.config.healthcare_staffing_threshold - ratio
        if record and shortfall > 0:
            trust_loss = self.config.healthcare_trust_penalty_scale * shortfall
            support_loss = self.config.healthcare_support_penalty_scale * shortfall
            state.institutional_trust -= trust_loss
            state.political_support -= support_loss
            self._trace("healthcare_staffing", "institutional_trust", -trust_loss,
                        "staffing below threshold weakens confidence in public services")
            self._trace("healthcare_staffing", "political_support", -support_loss,
                        "staffing below threshold harms government approval")

    def _condition_met(self, when: dict[str, Any]) -> bool:
        state = self.state
        if "project_status" in when and state.project_status != when["project_status"]:
            return False
        if "month" in when and state.month != when["month"]:
            return False
        if "month_multiple_of" in when and state.month % when["month_multiple_of"] != 0:
            return False
        if "metric_gt" in when:
            metric = when["metric_gt"]
            if state.metrics.get(metric["name"], 0.0) <= metric["value"]:
                return False
        return True

    def _resolve_events(self) -> None:
        state = self.state
        for event in self.scenario["events"]:
            if not self._condition_met(event["when"]):
                continue
            state.event_history.append(event["id"])
            for key, attr in (("political_support_delta", "political_support"),
                              ("institutional_trust_delta", "institutional_trust")):
                delta = event["effects"].get(key)
                if delta:
                    setattr(state, attr, getattr(state, attr) + delta)
                    self._trace(event["id"], attr, delta, event["reason"])

    def _clamp_state(self) -> None:
        state = self.state
        state.institutional_trust = min(1.0, max(0.0, state.institutional_trust))
        state.political_support = min(1.0, max(0.0, state.political_support))
        state.economic_diversity = min(1.0, max(0.0, state.economic_diversity))
        for district in state.districts.values():
            district.residential_units = max(0, min(district.housing_units, district.residential_units))
            district.short_term_rental_units = max(0, min(
                district.housing_units - district.residential_units, district.short_term_rental_units))
            district.transport_reliability = min(1.0, max(0.0, district.transport_reliability))
            district.average_rent = max(0.0, district.average_rent)
