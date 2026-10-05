import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from postcard_city.scenario import ScenarioValidationError, load_scenario, validate_scenario
from postcard_city.simulation import Simulation

ROOT = Path(__file__).parents[1]
SCENARIO = ROOT / "data/scenarios/the-overheated-destination.json"


def test_vertical_slice_content_is_valid():
    scenario = load_scenario(SCENARIO)
    assert scenario["id"] == "the-overheated-destination"
    assert scenario["region"]["template"] == "coastal-historic-metropolitan"
    assert len(scenario["decisions"][0]["options"]) >= 2


def test_scenario_conforms_to_json_schema():
    schema = json.loads((ROOT / "schemas/scenario.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(load_scenario(SCENARIO)))
    assert errors == []


def test_simulation_state_comes_from_content():
    scenario = load_scenario(SCENARIO)
    scenario["initial_state"]["budget"] = 1.0
    scenario["region"]["districts"][0]["average_rent"] = 999
    simulation = Simulation(scenario)
    assert simulation.state.budget == 1.0
    assert simulation.state.districts["historic_core"].average_rent == 999


def test_simulation_does_not_mutate_the_source_scenario():
    scenario = load_scenario(SCENARIO)
    before = copy.deepcopy(scenario)
    Simulation(scenario).run(6)
    assert scenario == before


@pytest.mark.parametrize("mutate", [
    lambda s: s.pop("events"),
    lambda s: s["region"]["districts"].pop(),
    lambda s: s["decisions"][0].update(options=s["decisions"][0]["options"][:1]),
    lambda s: s["decisions"][0]["options"][0]["effects"].update(unknown_effect=1),
    lambda s: s["decisions"][0]["options"][0]["effects"].update(project_status="nonexistent"),
    lambda s: s["region"]["districts"][0].update(residential_units=10**9),
    lambda s: s["region"]["districts"][1].update(id=s["region"]["districts"][0]["id"]),
    lambda s: s["events"].append(copy.deepcopy(s["events"][0])),
])
def test_invalid_content_is_rejected(mutate):
    scenario = load_scenario(SCENARIO)
    mutate(scenario)
    with pytest.raises(ScenarioValidationError):
        validate_scenario(scenario)
