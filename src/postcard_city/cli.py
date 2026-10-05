from __future__ import annotations

import argparse

from .model import Decision
from .reporting import causal_report, executive_report
from .simulation import Simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Postcard City simulation prototype")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--seed", type=int, default=4821)
    parser.add_argument("--decision", choices=["approve", "reject", "renegotiate", "audit"], default=None)
    parser.add_argument("--decision-month", type=int, default=1)
    parser.add_argument("--show-trace", action="store_true")
    parser.add_argument("--trace-limit", type=int, default=None)
    args = parser.parse_args()
    simulation = Simulation.from_default_slice(args.seed)
    decisions = []
    if args.decision:
        if args.decision_month < 1 or args.decision_month > args.months:
            parser.error("--decision-month must be within the simulated month range")
        decisions.append((args.decision_month, Decision("aurora_leisure_proposal", args.decision)))
    for month in range(1, args.months + 1):
        for scheduled_month, decision in decisions:
            if scheduled_month == month:
                simulation.apply_decision(decision)
        simulation.advance_month()
    print(executive_report(simulation.state))
    if args.show_trace:
        print()
        print(causal_report(simulation.state, args.trace_limit))


if __name__ == "__main__":
    main()
