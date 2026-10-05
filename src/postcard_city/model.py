from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Decision:
    """A player decision applied at the start of a simulation month."""

    decision_id: str
    option_id: str


@dataclass(frozen=True)
class TraceEntry:
    """A player-readable explanation of a state transition."""

    month: int
    source: str
    target: str
    amount: float
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "month": self.month,
            "source": self.source,
            "target": self.target,
            "amount": round(self.amount, 6),
            "reason": self.reason,
        }


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
    healthcare_staff: int
    transport_reliability: float
    tourist_pressure: float = 0.0


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
    project_status: str = "proposed"
    decision_history: list[Decision] = field(default_factory=list)
    event_history: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)
    traces: list[TraceEntry] = field(default_factory=list)

    def snapshot(self) -> dict[str, Any]:
        return {
            "seed": self.seed,
            "month": self.month,
            "budget": round(self.budget, 4),
            "tourism_visitors": round(self.tourism_visitors, 4),
            "tourism_revenue": round(self.tourism_revenue, 4),
            "institutional_trust": round(self.institutional_trust, 4),
            "political_support": round(self.political_support, 4),
            "economic_diversity": round(self.economic_diversity, 4),
            "project_status": self.project_status,
            "districts": {
                key: {
                    "population": value.population,
                    "housing_units": value.housing_units,
                    "residential_units": value.residential_units,
                    "short_term_rental_units": value.short_term_rental_units,
                    "average_rent": round(value.average_rent, 4),
                    "jobs": value.jobs,
                    "healthcare_capacity": value.healthcare_capacity,
                    "healthcare_staff": value.healthcare_staff,
                    "transport_reliability": round(value.transport_reliability, 4),
                    "tourist_pressure": round(value.tourist_pressure, 4),
                }
                for key, value in sorted(self.districts.items())
            },
            "decision_history": [decision.__dict__ for decision in self.decision_history],
            "event_history": self.event_history[:],
            "metrics": {key: round(value, 4) for key, value in sorted(self.metrics.items())},
            "traces": [trace.as_dict() for trace in self.traces],
        }
