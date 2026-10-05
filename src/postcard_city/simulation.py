from __future__ import annotations

import copy
import random
from pathlib import Path
from typing import Any, Iterable

from .model import CohortState, Decision, DistrictState, ParcelState, RegionState, SocialHousingState, TraceEntry
from .scenario import DEFAULT_SCENARIO_PATH, load_scenario, validate_scenario


class Simulation:
    def __init__(self, scenario: dict[str, Any], seed: int | None = None):
        validate_scenario(scenario)
        self.scenario = copy.deepcopy(scenario)
        self.state = self._build_state(self.scenario, self.scenario["default_seed"] if seed is None else seed)
        self.rng = random.Random(self.state.seed)
        self.profiles = self.scenario["project_profiles"]
        self.parameters = self.scenario["parameters"]
        self.housing_parameters = self.scenario["housing"]["parameters"]
        self.migration_parameters = self.scenario["migration"]["parameters"]
        self._resolved_decisions: set[str] = set()
        self._update_metrics(False)

    @classmethod
    def from_default_slice(cls, seed: int | None = None) -> "Simulation":
        return cls.from_scenario_file(DEFAULT_SCENARIO_PATH, seed)

    @classmethod
    def from_scenario_file(cls, path: str | Path = DEFAULT_SCENARIO_PATH, seed: int | None = None) -> "Simulation":
        return cls(load_scenario(path), seed)

    @staticmethod
    def _build_state(scenario: dict[str, Any], seed: int) -> RegionState:
        districts = {d["id"]: DistrictState(**{**d, "healthcare_staff": float(d["healthcare_staff"])}) for d in scenario["region"]["districts"]}
        parcels = {p["id"]: ParcelState(**p) for p in scenario["parcels"]}
        migration = {c["id"]: CohortState(**c) for c in scenario["migration"]["cohorts"]}
        social = SocialHousingState(**scenario["housing"]["social_housing"])
        initial = scenario["initial_state"]
        return RegionState(seed, 0, float(initial["budget"]), float(initial["tourism_visitors"]), 0.0, initial["institutional_trust"], initial["political_support"], initial["economic_diversity"], districts, parcels, migration, social, initial["project_status"])

    def _trace(self, source: str, target: str, amount: float, reason: str) -> None:
        self.state.traces.append(TraceEntry(self.state.month, source, target, amount, reason))

    def _option(self, decision: Decision) -> dict[str, Any]:
        for d in self.scenario["decisions"]:
            if d["id"] == decision.decision_id:
                for option in d["options"]:
                    if option["id"] == decision.option_id: return option
                raise ValueError(f"Unknown option: {decision.option_id}")
        raise ValueError(f"Unknown decision: {decision.decision_id}")

    def apply_decision(self, decision: Decision) -> None:
        option = self._option(decision)
        if decision.decision_id in self._resolved_decisions: raise ValueError(f"Decision already resolved: {decision.decision_id}")
        self._resolved_decisions.add(decision.decision_id); self.state.decision_history.append(decision)
        e = option["effects"]; before = vars(self.state).copy()
        if "project_status" in e: self.state.project_status = e["project_status"]
        self.state.budget += e.get("budget_delta", 0); self.state.tourism_visitors *= e.get("tourism_multiplier", 1); self.state.political_support += e.get("political_support_delta", 0); self.state.institutional_trust += e.get("institutional_trust_delta", 0); self.state.economic_diversity += e.get("economic_diversity_delta", 0)
        self._clamp()
        for key in ("budget", "tourism_visitors", "political_support", "institutional_trust", "economic_diversity"):
            delta = getattr(self.state, key) - before[key]
            if delta: self._trace(f"decision:{decision.option_id}", key, delta, e.get("reason", "player decision"))

    def apply_land_decision(self, parcel_id: str, mode: str) -> None:
        parcel = self.state.parcels.get(parcel_id)
        if parcel is None: raise ValueError(f"Unknown parcel: {parcel_id}")
        if parcel.tenure != "available" or not parcel.public_control: raise ValueError(f"Parcel unavailable: {parcel_id}")
        if mode not in {"sale_freehold", "sale_restricted", "lease_ground"}: raise ValueError(f"Unknown land mode: {mode}")
        if mode.startswith("sale"):
            self.state.budget += parcel.market_value * (1.0 if mode == "sale_freehold" else 0.75)
            parcel.tenure = "sold"; parcel.public_control = False
            self._trace(f"land:{mode}", "budget", parcel.market_value, "public parcel sold; ownership and future control are lost")
        else:
            parcel.tenure = "leased"; self.state.budget += parcel.market_value * 0.03
            self._trace("land:lease_ground", "budget", parcel.market_value * 0.03, "ground lease retains ownership and creates recurring administrative obligations")

    def start_social_housing(self, units: int) -> None:
        if units <= 0: raise ValueError("units must be positive")
        if self.state.social_housing.construction_progress > 0 or self.state.social_housing.units > 0: raise ValueError("social housing project already exists")
        cost = units * self.housing_parameters["construction_cost_per_unit"]
        if cost > self.state.budget: raise ValueError("insufficient budget")
        self.state.budget -= cost; self.state.social_housing.units = units; self.state.social_housing.construction_progress = 0.0
        self._trace("social_housing_construction", "budget", -cost, "capital cost for a delayed public housing project")

    def advance_month(self) -> RegionState:
        self.state.month += 1
        profile = self.profiles[self.state.project_status]
        growth = self.parameters["monthly_base_tourist_growth"] + profile["growth_bonus"]
        before = self.state.tourism_visitors; self.state.tourism_visitors *= 1 + growth
        self._trace("tourism_demand", "tourism_visitors", self.state.tourism_visitors - before, "monthly demand and project profile")
        self.state.tourism_revenue = self.state.tourism_visitors * self.parameters["tourist_spend"] * self.parameters["tourism_tax_rate"]
        self.state.budget += self.state.tourism_revenue - self.parameters["monthly_public_cost"]
        self._update_housing(profile); self._update_migration(); self._update_social_housing(); self._update_metrics(True); self._resolve_events(); self._clamp()
        return self.state

    def run(self, months: int, scheduled: Iterable[tuple[int, Decision]] = ()) -> RegionState:
        schedule = {}
        for month, decision in scheduled:
            if not 1 <= month <= months: raise ValueError(f"Decision month {month} is outside 1..{months}")
            schedule.setdefault(month, []).append(decision)
        for month in range(1, months + 1):
            for decision in schedule.get(month, []): self.apply_decision(decision)
            self.advance_month()
        return self.state

    def _update_housing(self, profile: dict[str, float]) -> None:
        core = self.state.districts["historic_core"]; outer = self.state.districts["outer_district"]
        converted = int(core.residential_units * profile["conversion_rate"]); core.residential_units -= converted; core.short_term_rental_units += converted
        core.tourist_pressure = min(1, self.state.tourism_visitors / self.parameters["tourist_saturation_visitors"])
        total_supply = sum(d.residential_units + d.short_term_rental_units for d in self.state.districts.values()) + self.state.social_housing.occupied_units
        total_demand = sum(c.population for c in self.state.migration.values()) * (1 + self.migration_parameters["tourism_pressure_penalty"] * core.tourist_pressure)
        vacancy = max(0.0, total_supply - total_demand) / max(total_demand, 1)
        pressure = self.housing_parameters["rent_pressure_weight"] * max(0, 1 - vacancy) + self.housing_parameters["tourism_demand_weight"] * core.tourist_pressure - self.housing_parameters["supply_relief_weight"] * min(vacancy, 1)
        for district in self.state.districts.values():
            before = district.average_rent; district.average_rent *= max(0.995, 1 + 0.003 * pressure); self._trace("housing_market", f"{district.id}.average_rent", district.average_rent - before, "housing demand, tourism pressure, and available supply")
        outer.transport_reliability = max(0, min(1, outer.transport_reliability - 0.004 * core.tourist_pressure + profile["transport_bonus"]))

    def _update_social_housing(self) -> None:
        h = self.state.social_housing
        if h.units <= 0: return
        h.construction_progress = min(1, h.construction_progress + 1 / max(h.construction_months, 1))
        if h.construction_progress >= 1: h.occupied_units = h.units
        cost = h.monthly_operating_cost + h.monthly_maintenance_cost
        if h.occupied_units: cost -= h.occupied_units * h.monthly_target_rent * (1 - h.arrears_rate)
        arrears = h.occupied_units * h.monthly_target_rent * h.arrears_rate
        h.cumulative_arrears += arrears; self.state.budget -= cost + arrears
        self._trace("social_housing", "budget", -cost - arrears, "operating cost, maintenance, rent income, and arrears")

    def _update_migration(self) -> None:
        affordability = max(0, 1 - self.state.districts["historic_core"].average_rent / 2000)
        services = self.state.metrics.get("healthcare_staffing", 0.75)
        jobs = min(1, self.state.districts["outer_district"].jobs / 120000)
        tourism = self.state.districts["historic_core"].tourist_pressure
        for cohort in self.state.migration.values():
            attractiveness = (self.migration_parameters["housing_affordability_weight"] * affordability * cohort.housing_sensitivity + self.migration_parameters["jobs_weight"] * jobs * cohort.job_sensitivity + self.migration_parameters["services_weight"] * services * cohort.service_sensitivity - self.migration_parameters["tourism_pressure_penalty"] * tourism)
            net = cohort.population * cohort.mobility * (self.migration_parameters["base_arrival_rate"] * attractiveness - self.migration_parameters["base_departure_rate"] * max(0, 0.5 - attractiveness))
            cohort.population = max(0, cohort.population + net); cohort.net_migration = net
            self._trace("regional_attractiveness", f"migration.{cohort.id}", net, "housing, jobs, services, and tourism pressure change migration flows")

    def _update_metrics(self, record: bool) -> None:
        core = self.state.districts["historic_core"]; staff = sum(d.healthcare_staff for d in self.state.districts.values()); capacity = sum(d.healthcare_capacity for d in self.state.districts.values())
        ratio = staff / capacity; population = sum(c.population for c in self.state.migration.values())
        self.state.metrics.update({"housing_affordability": max(0, 1 - core.average_rent / 2000), "healthcare_staffing": ratio, "tourism_pressure": core.tourist_pressure, "permanent_population": population, "essential_worker_net_migration": self.state.migration["essential_workers"].net_migration, "public_housing_net_cashflow": -(self.state.social_housing.monthly_operating_cost + self.state.social_housing.monthly_maintenance_cost + self.state.social_housing.cumulative_arrears)})
        shortfall = self.parameters["healthcare_staffing_threshold"] - ratio
        if record and shortfall > 0:
            self.state.institutional_trust -= 0.2 * shortfall; self.state.political_support -= 0.15 * shortfall

    def _resolve_events(self) -> None:
        for event in self.scenario["events"]:
            when = event["when"]
            if when.get("project_status") and when["project_status"] != self.state.project_status: continue
            if when.get("month") and when["month"] != self.state.month: continue
            if when.get("month_multiple_of") and self.state.month % when["month_multiple_of"]: continue
            condition = when.get("metric_gt")
            if condition and self.state.metrics.get(condition["name"], 0) <= condition["value"]: continue
            self.state.event_history.append(event["id"])
            for key, attr in (("political_support_delta", "political_support"), ("institutional_trust_delta", "institutional_trust")):
                delta = event["effects"].get(key, 0); setattr(self.state, attr, getattr(self.state, attr) + delta)

    def _clamp(self) -> None:
        self.state.institutional_trust = max(0, min(1, self.state.institutional_trust)); self.state.political_support = max(0, min(1, self.state.political_support)); self.state.economic_diversity = max(0, min(1, self.state.economic_diversity))
        for d in self.state.districts.values(): d.residential_units = max(0, min(d.housing_units, d.residential_units)); d.short_term_rental_units = max(0, min(d.housing_units - d.residential_units, d.short_term_rental_units)); d.average_rent = max(0, d.average_rent); d.transport_reliability = max(0, min(1, d.transport_reliability))
