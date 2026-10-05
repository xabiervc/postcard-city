from pathlib import Path

from postcard_city.scenario import load_scenario

if __name__ == "__main__":
    for path in sorted((Path(__file__).resolve().parents[1] / "data" / "scenarios").glob("*.json")):
        scenario = load_scenario(path)
        print(f"Validated scenario: {scenario['id']}")
