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
    parser.add_argument("--start-social-housing", type=int, default=0)
    parser.add_argument("--land-parcel", default=None)
    parser.add_argument("--land-mode", choices=["sale_freehold", "sale_restricted", "lease_ground"], default=None)
    parser.add_argument("--show-trace", action="store_true")
    parser.add_argument("--trace-limit", type=int, default=None)
    args = parser.parse_args()
    if args.months < 1: parser.error("--months must be at least 1")
    if bool(args.land_parcel) != bool(args.land_mode): parser.error("--land-parcel and --land-mode must be supplied together")
    if args.decision and not 1 <= args.decision_month <= args.months: parser.error("--decision-month must be within the simulated month range")
    simulation = Simulation.from_default_slice(args.seed)
    if args.start_social_housing:
        simulation.start_social_housing(args.start_social_housing)
    if args.land_parcel:
        simulation.apply_land_decision(args.land_parcel, args.land_mode)
    scheduled = []
    if args.decision: scheduled.append((args.decision_month, Decision("aurora_leisure_proposal", args.decision)))
    simulation.run(args.months, scheduled)
    print(executive_report(simulation.state))
    if args.show_trace: print("\n" + causal_report(simulation.state, args.trace_limit))


if __name__ == "__main__":
    main()
