# Housing, Land, and Migration

## Design intent
Housing is a public service, a household expense, an asset market, a worker-access mechanism, and a long-term fiscal commitment. It is not assumed to be profitable for government.

## Public land
Each parcel is finite and has a tenure mode:
- `sale_freehold`: immediate receipt, no future ownership or control.
- `sale_restricted`: immediate receipt with enforceable affordability or use conditions.
- `lease_ground`: recurring income and retained ownership, with administrative and enforcement obligations.

A sale is irreversible in the current prototype. A lease can expire, be renewed, or fail if the authority cannot administer its conditions.

## Social housing
Social-housing projects have:
- Land requirement.
- Construction delay.
- Capital cost.
- Operating and maintenance cost.
- Below-market rent.
- Household eligibility.
- Arrears probability.
- Essential-worker allocation policy.
- Completion and occupancy states.

The fiscal ledger separates rent income, arrears, maintenance, staffing, construction, and avoided emergency-service costs. A project can improve affordability and healthcare staffing while producing a negative public cash flow.

## Migration
The prototype uses cohorts rather than individual citizens:
- Essential workers.
- Families.
- Students.
- Retirees.

Each cohort evaluates the region through affordability, employment, services, transport, tourism pressure, and quality of life. Arrival and departure rates have inertia: residents do not instantly appear or disappear after one policy tick.

Tourism increases demand and jobs but can reduce affordability, worker access, and permanent-resident inflows if housing conversion outpaces supply.

## Transparency
Player-facing reports must distinguish:
- Observed state.
- Model estimate.
- Evidence-backed mechanism.
- Prototype calibration.
- Uncertain or disputed outcome.
