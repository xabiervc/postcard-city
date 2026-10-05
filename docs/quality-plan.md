# Quality Plan

## Quality bar
The target is a polished, distinctive, award-caliber experience. Quality includes design coherence, systemic depth, emotional clarity, accessibility, technical reliability, and presentation.

## Design gates
- The core loop is enjoyable without advanced systems.
- Every major metric has inspectable causes.
- No single strategy dominates all scenarios.
- Procedural scenarios are coherent and recoverable.
- Consequences are visible, delayed where appropriate, and not arbitrary.

## Automated tests
- Unit tests for formulas and thresholds.
- Property tests for invariants.
- Integration tests for monthly ticks.
- Seed replay tests.
- Scenario solvability tests.
- Save/load round-trip tests.
- Localization key and placeholder tests.
- Performance regression tests.

## Invariants
Examples:
- Population cannot become negative.
- Budget changes reconcile with transactions.
- A project cannot operate before construction completes.
- A service cannot exceed its capacity without a documented overload state.
- The same seed and decisions produce the same state.
- Disabled systems do not silently affect outcomes.

## Playtesting
Test with strategy players, city-builder players, political simulation players, and newcomers. Measure comprehension, decision confidence, perceived agency, frustration, replay desire, and time-to-first-meaningful-decision.

## Accessibility testing
Use automated checks plus manual keyboard/controller, contrast, text scaling, reduced motion, captions, and color-vision testing. Include players with relevant access needs before content lock.

## Performance targets for prototype
Define budgets before production. The prototype must show stable frame time, predictable simulation tick duration, responsive UI, and reliable save/load under the slice's maximum state.

## Release gates
Prototype: core loop proven.
Vertical slice: complete representative experience.
Alpha: all major systems integrated.
Beta: content and localization complete enough for external testing.
Release: no critical blockers, stable saves, verified accessibility, and documented known issues.
