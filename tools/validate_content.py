from pathlib import Path

from postcard_city.scenario import load_scenario


if __name__ == "__main__":
    root = Path(__file__).parents[1]
    scenario = load_scenario(root / "data/scenarios/the-overheated-destination.json")
    print(f"Validated scenario: {scenario['id']}")
