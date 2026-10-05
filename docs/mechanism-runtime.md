# Mechanism Runtime and Robustness

## Purpose
Mechanism cards are the auditable bridge between evidence, context, and runtime policy effects. This first implementation resolves a configuration and sweeps declared ranges; it does not yet replace the simulation's calibrated equations.

## Resolution
A card contains one or more context-mechanism-outcome configurations. The resolver scores configurations against the current regional context and selects the most specific matching configuration.

## Robustness labels
- `robust`: the declared direction holds across the sampled range.
- `context-dependent`: the sampled range includes both directions or materially different outcomes.
- `fragile`: the result is not stable under the sampled range.
- `not-evaluable`: there is no matching configuration or usable outcome.

These labels describe the model's sensitivity, not the certainty of the real-world evidence.

## Vertical-slice analysis
`tools/run_robustness.py` evaluates short-term-rental regulation, social housing, and public land disposal under low-capacity, balanced, and high-capacity contexts. It writes `reports/vertical-slice-robustness.json`, which is intentionally ignored from source control as a generated report.

## Boundary
Evidence certainty and model robustness are separate dimensions. A card can have moderate evidence but context-dependent model results, or very-low evidence with a stable prototype result. The player-facing UI must show both.

## Next integration step
Use the resolved card configuration and sampled effect ranges inside the simulation, then compare policy outcomes against counterfactual runs and expose the robustness report to the player.
