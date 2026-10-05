# Changelog

## 0.2.0 — Review and content-driven simulation

### Defects found in review and fixed
- Healthcare staffing never changed: the monthly factor evaluated to exactly 1.0 and staff was truncated to an integer. The hospital mechanic that defines the vertical slice was inert and its trust/support penalty could never fire. Staffing is now continuous and depends on worker accessibility; a regression test covers it.
- The rent trace recorded the absolute rent instead of the monthly change.
- A rejected (unknown) decision was appended to the decision history before validation.
- A decision could be applied more than once; each decision can now be resolved once.
- LICENSE.md named a surname that was never provided; it now uses the GitHub handle.
- config/vertical-slice.yaml claimed 6 districts while the prototype has 2.
- Added the missing .gitignore.

### Added
- data/scenarios/the-overheated-destination.json is the single source of truth: region, initial state, parameters, project profiles, decisions with effects, and events.
- schemas/scenario.schema.json and stricter semantic validation in scenario.py.
- Simulation.from_scenario_file and Simulation.from_default_slice load validated content; no slice data is hardcoded in Python.
- 30 automated tests: determinism, invariants for five strategies over 60 months, schema conformance, invalid-content rejection, trace correctness, and CLI behaviour.

### Known balance issues (not yet addressed)
- Housing affordability falls to roughly 6% by month 36 under every strategy, because the baseline rent growth is independent of policy.
- Tourist visitors have no saturation feedback; approving the project reaches about 2.1M visitors by month 36 against a 900k saturation reference.
- Approving yields the highest budget by a wide margin, so the political and service costs are not yet strong enough to make the strategies genuinely competitive.
- Elections, media, opposition and the whistleblower described in the vertical slice specification are not implemented yet.
