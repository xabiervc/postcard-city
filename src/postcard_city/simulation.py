from __future__ import annotations

from dataclasses import replace

from .model import SimulationState
from .scenario import Scenario


class Simulation:
    def __init__(self, state: SimulationState, scenario: Scenario | None = None):
        self.state = state
        self.scenario = scenario

    @classmethod
    def from_default_slice(cls):
        from .scenario import load_default_scenario

        scenario = load_default_scenario()
        return cls(state=SimulationState.from_scenario(scenario), scenario=scenario)

    def start_social_housing(self, units: int) -> None:
        housing = self.state.social_housing
        housing.units += units
        housing.construction_progress = 0.0
        housing.construction_months = 24

    def advance_month(self) -> None:
        housing = self.state.social_housing
        if housing.units > 0 and housing.construction_progress < 1.0:
            monthly_progress = 1.0 / housing.construction_months
            housing.construction_progress = min(
                1.0,
                housing.construction_progress + monthly_progress,
            )
            if housing.construction_progress >= 1.0:
                housing.construction_progress = 1.0
                housing.occupied_units = housing.units

        if housing.units > 0 and housing.construction_progress >= 1.0:
            housing.occupied_units = housing.units
            housing.cumulative_operating_cost += housing.monthly_operating_cost
            housing.cumulative_maintenance_cost += housing.monthly_maintenance_cost
            housing.cumulative_rent_income += (
                housing.occupied_units * housing.monthly_rent
            )

        self.state.month += 1
