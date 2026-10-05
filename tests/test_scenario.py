from pathlib import Path

from postcard_city.scenario import load_scenario


def test_vertical_slice_content_is_valid():
    path = Path(__file__).parents[1] / "data/scenarios/the-overheated-destination.json"
    scenario = load_scenario(path)
    assert scenario["id"] == "the-overheated-destination"
    assert len(scenario["decisions"][0]["options"]) >= 2
