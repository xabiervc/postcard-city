from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Decision:
    decision_id: str
    option_id: str


@dataclass(frozen=True)
class TraceEntry:
    month: int
    source: str
    target: str
    amount: float
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {"month": self.month, "source": self.source, "target": self.target, "amount": round(self.amount, 6), "reason": self.reason}


@dataclass
class DistrictState:
    id: str
    population: int
    housing_units: int
    residential_units: int
    short_term_rental_units: int
    average_rent: float
    jobs: int
    healthcare_capacity: int
    healthcare_staff: float
    transport_reliability: float
    tourist_pressure: float = 0.0


@dataclass
class ParcelState:
    id: str
    district_id: str
    area: float
    market_value: float
    public_control: bool
    tenure: str


@dataclass
class CohortState:
    id: str
    population: float
    mobility: float
    housing_sensitivity: float
    job_sensitivity: float
    service_sensitivity: float
    net_migration: float = 0.0


@dataclass
class SocialHousingState:
    units: int
    construction_progress: float
    construction_months: int
    monthly_operating_cost: float
    monthly_maintenance_cost: float
    monthly_target_rent: float
    arrears_rate: float
    essential_worker_share: float
    occupied_units: int = 0
    cumulative_arrears: float = 0.0
    cumulative_rent_income: float = 0.0
    cumulative_operating_cost: float = 0.0
    cumulative_maintenance_cost: float = 0.0


@dataclass
class RegionState:
    seed: int
    month: int
    budget: float
    tourism_visitors: float
    tourism_revenue: float
    institutional_trust: float
    political_support: float
    economic_diversity: float
    districts: dict[str, DistrictState]
    parcels: dict[str, ParcelState]
    migration: dict[str, CohortState]
    social_housing: SocialHousingState
    project_status: str = "proposed"
    decision_history: list[Decision] = field(default_factory=list)
    event_history: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)
    traces: list[TraceEntry] = field(default_factory=list)

    def snapshot(self) -> dict[str, Any]:
        return {"seed": self.seed, "month": self.month, "budget": round(self.budget, 4), "tourism_visitors": round(self.tourism_visitors, 4), "tourism_revenue": round(self.tourism_revenue, 4), "institutional_trust": round(self.institutional_trust, 4), "political_support": round(self.political_support, 4), "economic_diversity": round(self.economic_diversity, 4), "project_status": self.project_status, "districts": {k: vars(v) for k, v in sorted(self.districts.items())}, "parcels": {k: vars(v) for k, v in sorted(self.parcels.items())}, "migration": {k: vars(v) for k, v in sorted(self.migration.items())}, "social_housing": vars(self.social_housing), "decision_history": [vars(d) for d in self.decision_history], "event_history": self.event_history[:], "metrics": {k: round(v, 6) for k, v in sorted(self.metrics.items())}, "traces": [t.as_dict() for t in self.traces]}
