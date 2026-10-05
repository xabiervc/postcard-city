from __future__ import annotations

import argparse

from .model import Decision
from .reporting import causal_report, executive_report
from .simulation import Simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Postcard City simulation prototype")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--decision", choices=["approve", "reject", "renegotiate", "audit"], default=None)
    parser.add_argument("--decision-month", type=int, default=1)
    parser.add_argument("--show-trace", action="store_true")
    parser.add_argument("--trace-limit", type=int, default=None)
    args = parser.parse_args()
    if args.months < 1:
        parser.error("--months must be at least 1")
    scheduled = []
    if args.decision:
        if not 1 <= args.decision_month <= args.months:
            parser.error("--decision-month must be within the simulated month range")
        scheduled.append((args.decision_month, Decision("aurora_leisure_proposal", args.decision)))
    simulation = Simulation.from_default_slice(args.seed)
    simulation.run(args.months, scheduled)
    print(executive_report(simulation.state))
    if args.show_trace:
        print()
        print(causal_report(simulation.state, args.trace_limit))


if __name__ == "__main__":
    main()
