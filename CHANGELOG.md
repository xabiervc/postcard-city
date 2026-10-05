# Changelog

## Unreleased — Integration stabilization

### Fixed and verified
- Housing supply, migration, public land, and social housing now participate in one deterministic vertical-slice simulation.
- Short-term rentals no longer count as long-term residential supply when calculating housing pressure.
- Public-housing cash flow accounts separately for rent income, operating cost, maintenance, and arrears.
- Invalid land actions fail before mutating state.
- Social housing can be started explicitly and reaches occupancy only after its configured construction delay.
- Added full-slice integration and replay tests.

### Calibration boundary
Housing and migration coefficients remain prototype calibration. They must be replaced or parameterized through mechanism-card resolution and robustness analysis before production balance.
