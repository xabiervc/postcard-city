import json
from pathlib import Path

from postcard_city.robustness import run_vertical_slice_report


if __name__ == "__main__":
    report = run_vertical_slice_report()
    output = Path("reports/vertical-slice-robustness.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    for result in report["results"]:
        print(f"{result['context_id']}: {result['card_id']} -> {result['target']} = {result['classification']}")
