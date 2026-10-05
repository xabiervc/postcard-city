import os
import subprocess
import sys
from pathlib import Path

SRC = str(Path(__file__).parents[1] / "src")


def run_cli(*args):
    env = {**os.environ, "PYTHONPATH": SRC + os.pathsep + os.environ.get("PYTHONPATH", "")}
    return subprocess.run([sys.executable, "-m", "postcard_city.cli", *args],
                          capture_output=True, text=True, env=env)


def test_cli_runs_and_prints_report():
    result = run_cli("--months", "6", "--decision", "renegotiate", "--show-trace", "--trace-limit", "3")
    assert result.returncode == 0, result.stderr
    assert "Healthcare staffing" in result.stdout
    assert "Causal trace:" in result.stdout


def test_cli_rejects_decision_month_out_of_range():
    result = run_cli("--months", "6", "--decision", "audit", "--decision-month", "9")
    assert result.returncode != 0
