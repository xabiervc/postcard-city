from __future__ import annotations

import argparse

from .model import Decision
from .reporting import executive_report
from .simulation import Simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Postcard City simulation prototype")
    parser.add_argument("--months", type=int, default=12)
    parser.add_argument("--seed", type=int, default=4821)
    parser.add_argument("--decision", choices=["approve", "reject", "renegotiate", "audit"], default=None)
    args = parser.parse_args()
    simulation = Simulation.from_default_slice(args.seed)
    decisions = []
    if args.decision:
        decisions.append(Decision("aurora_leisure_proposal", args.decision))
    simulation.run(args.months, decisions)
    print(executive_report(simulation.state))


if __name__ == "__main__":
    main()
