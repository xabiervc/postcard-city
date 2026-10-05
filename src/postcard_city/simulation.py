from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

from .model import Decision, DistrictState, RegionState, TraceEntry


@dataclass(frozen=True)
class SimulationConfig:
    monthly_base_tourist_growth: float = 0.018
    tourist_spend: float = 115.0
    tourism_tax_rate: float = 0.08
    monthly_public_cost: float = 2_000_000.0
    healthcare_staffing_threshold: float = 0.72


class Simulation:
    """Small deterministic monthly simulation for the vertical slice."""

    def __init__(self, state: RegionState, config: SimulationConfig | None = None):
        self.state = state
        self.config = config or SimulationConfig()
        self._rng = random.Random(state.seed)

    @classmethod
    def from_default_slice(cls, seed: int = 4821) -> "Simulation":
        districts = {
            "historic_core": DistrictState(
                id="historic_core", population=180_000, housing_units=105_000,
                residential_units=71_000, short_term_rental_units=34_000,
                average_rent=1_520, jobs=130_000, healthcare_capacity=1_000,
                healthcare_staff=860, transport_reliability=0.71,
            ),
            "outer_district": DistrictState(
                id="outer_district", population=260_000, housing_units=142_000,
                residential_units=139_000, short_term_rental_units=3_000,
                average_rent=820, jobs=72_000, healthcare_capacity=1_350,
                healthcare_staff=920, transport_reliability=0.58,
            ),
        }
        simulation = cls(RegionState(
            seed=seed, month=0, budget=80_000_000.0,
            tourism_visitors=420_000.0, tourism_revenue=0.0,
            institutional_trust=0.62, political_support=0.54,
            economic_diversity=0.34, districts=districts,
        ))
        simulation._update_metrics()
        return simulation

    def apply_decision(self, decision: Decision) -> None:
        self.state.decision_history.append(decision)
        if decision.decision_id != "aurora_leisure_proposal":
            raise ValueError(f"Unknown decision: {decision.decision_id}")
        before_budget = self.state.budget
        before_visitors = self.state.tourism_visitors
        before_trust = self.state.institutional_trust
        if decision.option_id == "approve":
            self.state.project_status = "approved"
            self.state.budget -= 18_000_000.0
            self.state.tourism_visitors *= 1.08
            self.state.political_support += 0.04
            reason = "public infrastructure commitment for the unqualified proposal"
        elif decision.option_id == "reject":
            self.state.project_status = "rejected"
            self.state.political_support -= 0.03
            self.state.institutional_trust += 0.02
            reason = "rejection protects institutional autonomy but disappoints investors"
        elif decision.option_id == "renegotiate":
            self.state.project_status = "safeguarded"
            self.state.budget -= 8_000_000.0
            self.state.tourism_visitors *= 1.04
            self.state.economic_diversity += 0.04
            self.state.institutional_trust += 0.03
            reason = "safeguards trade immediate growth for public conditions"
        elif decision.option_id == "audit":
            self.state.project_status = "under_audit"
            self.state.budget -= 2_000_000.0
            self.state.institutional_trust += 0.05
            reason = "independent review increases confidence but delays the project"
        else:
            raise ValueError(f"Unknown option: {decision.option_id}")
        self.state.traces.extend([
            TraceEntry(self.state.month, "decision", "budget", self.state.budget - before_budget, reason),
            TraceEntry(self.state.month, "decision", "tourism_visitors", self.state.tourism_visitors - before_visitors, reason),
            TraceEntry(self.state.month, "decision", "institutional_trust", self.state.institutional_trust - before_trust, reason),
        ])
        self._clamp_state()

    def advance_month(self) -> RegionState:
        self.state.month += 1
        before_visitors = self.state.tourism_visitors
        growth = self.config.monthly_base_tourist_growth
        if self.state.project_status == "approved":
            growth += 0.025
        elif self.state.project_status == "safeguarded":
            growth += 0.012
        elif self.state.project_status == "under_audit":
            growth -= 0.004
        self.state.tourism_visitors *= 1.0 + growth
        self.state.traces.append(TraceEntry(
            self.state.month, "seasonal_and_project_demand", "tourism_visitors",
            self.state.tourism_visitors - before_visitors, "monthly tourism demand and project status",
        ))
        before_budget = self.state.budget
        self.state.tourism_revenue = self.state.tourism_visitors * self.config.tourist_spend * self.config.tourism_tax_rate
        self.state.budget += self.state.tourism_revenue - self.config.monthly_public_cost
        self.state.traces.append(TraceEntry(
            self.state.month, "tourism_revenue", "budget", self.state.budget - before_budget,
            "tourism tax revenue minus recurring public costs",
        ))
        self._update_districts()
        self._update_metrics()
        self._resolve_events()
        self._clamp_state()
        return self.state

    def run(self, months: int, decisions: Iterable[Decision] = ()) -> RegionState:
        decisions_by_month = {index + 1: decision for index, decision in enumerate(decisions)}
        for month in range(1, months + 1):
            decision = decisions_by_month.get(month)
            if decision:
                self.apply_decision(decision)
            self.advance_month()
        return self.state

    def _update_districts(self) -> None:
        core = self.state.districts["historic_core"]
        outer = self.state.districts["outer_district"]
        conversion_rate = 0.003 if self.state.project_status == "approved" else 0.001
        conversion_rate = 0.0005 if self.state.project_status == "safeguarded" else conversion_rate
        converted = max(0, int(core.residential_units * conversion_rate))
        core.residential_units -= converted
        core.short_term_rental_units += converted
        core.average_rent *= 1.0 + (0.006 if converted else 0.002)
        core.tourist_pressure = min(1.0, self.state.tourism_visitors / 900_000.0)
        self.state.traces.append(TraceEntry(
            self.state.month, "tourism_pressure", "historic_core.residential_units", -converted,
            "visitor growth and project status convert residential capacity to short-term rentals",
        ))
        self.state.traces.append(TraceEntry(
            self.state.month, "housing_pressure", "historic_core.average_rent", core.average_rent,
            "reduced residential capacity increases rent pressure",
        ))
        before_transport = outer.transport_reliability
        outer.transport_reliability = max(0.0, outer.transport_reliability - 0.004 * core.tourist_pressure)
        if self.state.project_status == "safeguarded":
            outer.transport_reliability = min(1.0, outer.transport_reliability + 0.002)
        self.state.traces.append(TraceEntry(
            self.state.month, "tourism_pressure", "outer_district.transport_reliability",
            outer.transport_reliability - before_transport, "tourism load and safeguards change regional transport reliability",
        ))
        worker_access = outer.transport_reliability * (1_000 / max(outer.average_rent, 1))
        before_staff = outer.healthcare_staff
        outer.healthcare_staff = max(0, int(outer.healthcare_staff * (0.999 + min(worker_access, 0.001))))
        self.state.traces.append(TraceEntry(
            self.state.month, "worker_accessibility", "outer_district.healthcare_staff",
            outer.healthcare_staff - before_staff, "housing cost and transport affect staff retention",
        ))

    def _update_metrics(self) -> None:
        core = self.state.districts["historic_core"]
        total_capacity = sum(d.healthcare_capacity for d in self.state.districts.values())
        total_staff = sum(d.healthcare_staff for d in self.state.districts.values())
        healthcare_ratio = total_staff / total_capacity
        affordability = max(0.0, 1.0 - core.average_rent / 2_000.0)
        worker_access = (self.state.districts["outer_district"].transport_reliability + affordability) / 2.0
        self.state.metrics = {
            "housing_affordability": affordability,
            "worker_accessibility": worker_access,
            "healthcare_staffing": healthcare_ratio,
            "tourism_pressure": core.tourist_pressure,
            "budget_millions": self.state.budget / 1_000_000.0,
        }
        if healthcare_ratio < self.config.healthcare_staffing_threshold:
            self.state.institutional_trust -= 0.008
            self.state.political_support -= 0.006
            self.state.traces.append(TraceEntry(
                self.state.month, "healthcare_staffing", "institutional_trust", -0.008,
                "staffing below threshold weakens confidence in public services",
            ))
            self.state.traces.append(TraceEntry(
                self.state.month, "healthcare_staffing", "political_support", -0.006,
                "staffing below threshold harms government approval",
            ))

    def _resolve_events(self) -> None:
        if self.state.project_status == "approved" and self.state.month == 6:
            self.state.event_history.append("aurora_financing_warning")
            self.state.institutional_trust -= 0.04
            self.state.traces.append(TraceEntry(
                self.state.month, "aurora_financing_warning", "institutional_trust", -0.04,
                "project financing appears less secure than publicly claimed",
            ))
        if self.state.metrics.get("tourism_pressure", 0) > 0.72 and self.state.month % 6 == 0:
            self.state.event_history.append("resident_housing_protest")
            self.state.political_support -= 0.03
            self.state.traces.append(TraceEntry(
                self.state.month, "resident_housing_protest", "political_support", -0.03,
                "housing pressure triggers organized resident opposition",
            ))

    def _clamp_state(self) -> None:
        self.state.institutional_trust = min(1.0, max(0.0, self.state.institutional_trust))
        self.state.political_support = min(1.0, max(0.0, self.state.political_support))
        self.state.economic_diversity = min(1.0, max(0.0, self.state.economic_diversity))
        for district in self.state.districts.values():
            district.residential_units = max(0, min(district.housing_units, district.residential_units))
            district.short_term_rental_units = max(0, district.housing_units - district.residential_units)
            district.transport_reliability = min(1.0, max(0.0, district.transport_reliability))
            district.average_rent = max(0.0, district.average_rent)
