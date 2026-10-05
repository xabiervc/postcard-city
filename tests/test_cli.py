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


def test_cli_integrates_decision_housing_land_and_reporting():
    result = run_cli(
        "--months", "6",
        "--decision", "renegotiate",
        "--decision-month", "2",
        "--start-social-housing", "10",
        "--land-parcel", "civic-edge",
        "--land-mode", "lease_ground",
    )
    assert result.returncode == 0, result.stderr
    assert "Month: 6" in result.stdout
    assert "Budget: EUR" in result.stdout
    assert "Public housing net cashflow:" in result.stdout
    assert "Events:" in result.stdout


def test_cli_trace_limit_counts_trace_lines():
    result = run_cli("--months", "2", "--show-trace", "--trace-limit", "2")
    assert result.returncode == 0, result.stderr
    trace_lines = [line for line in result.stdout.splitlines() if line.startswith("- Month ")]
    assert len(trace_lines) == 2


def test_cli_rejects_incomplete_land_arguments_and_non_positive_months():
    incomplete = run_cli("--months", "2", "--land-parcel", "civic-edge")
    assert incomplete.returncode != 0
    invalid_months = run_cli("--months", "0")
    assert invalid_months.returncode != 0
