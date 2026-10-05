import copy

import pytest

from postcard_city.scenario import (
    DEFAULT_SCENARIO_PATH,
    ScenarioValidationError,
    load_scenario,
    validate_scenario,
)
from postcard_city.simulation import Simulation

MUTATIONS = {
    "unsupported_schema_version": lambda s: s.update(schema_version=1),
    "unknown_initial_status": lambda s: s["initial_state"].update(project_status="nonexistent"),
    "parcel_unknown_district": lambda s: s["parcels"][0].update(district_id="nowhere"),
    "duplicate_parcel": lambda s: s["parcels"].append(copy.deepcopy(s["parcels"][0])),
    "duplicate_cohort": lambda s: s["migration"]["cohorts"].append(copy.deepcopy(s["migration"]["cohorts"][0])),
    "arrears_above_one": lambda s: s["housing"]["social_housing"].update(arrears_rate=1.5),
    "negative_worker_share": lambda s: s["housing"]["social_housing"].update(essential_worker_share=-0.1),
    "transport_above_one": lambda s: s["region"]["districts"][0].update(transport_reliability=1.5),
    "overallocated_housing": lambda s: s["region"]["districts"][0].update(residential_units=105000),
    "negative_units": lambda s: s["region"]["districts"][0].update(residential_units=-1),
    "boolean_units": lambda s: s["region"]["districts"][0].update(residential_units=True),
    "third_district": lambda s: s["region"]["districts"].append(copy.deepcopy(s["region"]["districts"][0])),
    "unknown_effect_second_option": lambda s: s["decisions"][0]["options"][1]["effects"].update(unknown_effect=1),
    "invalid_status_second_option": lambda s: s["decisions"][0]["options"][1]["effects"].update(project_status="nonexistent"),
}


@pytest.mark.parametrize("mutate", list(MUTATIONS.values()), ids=list(MUTATIONS))
def test_invalid_scenario_content_is_rejected_by_validator(mutate):
    scenario = load_scenario(DEFAULT_SCENARIO_PATH)
    mutate(scenario)
    with pytest.raises(ScenarioValidationError):
        validate_scenario(scenario)


@pytest.mark.parametrize("mutate", list(MUTATIONS.values()), ids=list(MUTATIONS))
def test_simulation_refuses_invalid_scenarios(mutate):
    scenario = load_scenario(DEFAULT_SCENARIO_PATH)
    mutate(scenario)
    with pytest.raises(ScenarioValidationError):
        Simulation(scenario)


def test_default_scenario_is_valid_and_validation_does_not_mutate_it():
    scenario = load_scenario(DEFAULT_SCENARIO_PATH)
    before = copy.deepcopy(scenario)
    validate_scenario(scenario)
    assert scenario == before
