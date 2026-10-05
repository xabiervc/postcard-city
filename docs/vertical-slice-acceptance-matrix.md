# Vertical Slice Acceptance Matrix

## Purpose

This matrix prevents the project from treating a documented intention as an implemented player experience. Each requirement has an evidence type and a closure condition.

| Requirement | Current evidence | Closure evidence | Status |
|---|---|---|---|
| Player fantasy is explicit | `player-fantasy-and-gameplay-loop.md` | Playtesters can describe their role and limits without coaching | Design-ready; prototype pending |
| Observe → interpret → prioritize → intervene → resolve → remember loop | Gameplay-loop document and CLI/simulation flow | A playable cycle exposes each phase to the player | Design-ready; prototype pending |
| One district under visible pressure | Scenario and simulation state | Visual or interactive district view shows pressure | Simulation-backed; presentation pending |
| Four recurring perspectives | `character-bible.md` | Four characters provide contextual testimony in a build | Design-ready; content implementation pending |
| Two meaningful interventions | `campaign-structure.md` and simulation APIs | Player chooses two interventions with visible trade-offs | Partly simulation-backed; prototype pending |
| One crisis requiring a priority choice | Crisis catalog and campaign structure | Crisis UI presents incompatible protections and records the choice | Content-backed; gameplay validation pending |
| Delayed consequence | Simulation events, metrics, and traces | Player notices and attributes the consequence without debug tools | Simulation-backed; playtest pending |
| Two postcards of the same place | `postcard-memory-system.md` | Build creates, stores, and compares two readable postcard records | Design-ready; implementation pending |
| Causal explanation | Reporting and trace output | Player-readable causal summary identifies dominant links and uncertainty | Reporting-backed; UI and playtest pending |
| Explicit success condition | Campaign structure | Build evaluates and communicates success | Design-defined; implementation pending |
| Explicit failure condition | Campaign structure | Build evaluates and communicates failure without moral simplification | Design-defined; implementation pending |
| Information accessibility | `information-accessibility-spec.md` | Build passes keyboard, controller, scaling, contrast, text alternative, and reduced-motion checks | Specification-ready; implementation pending |
| Complexity budget | `complexity-budget.md` | Prototype stays within metric, character, crisis, decision, and performance limits | Constraint-defined; profiling pending |
| Calibration and replay value | `simulation-calibration-plan.md` | Reference runs plus five or more structured playtests show viable imperfect strategies | Plan-ready; prototype pending |
| Automated simulation integrity | Existing pytest suite | CI remains green and reference seeds remain reproducible | Implemented for current simulation |

## Evidence classes

- **Documented**: a rule or intent is written down.
- **Simulation-backed**: code and automated tests exercise the underlying state or causal behaviour.
- **Prototype pending**: the requirement needs an interactive build or presentation layer.
- **Playtest pending**: the requirement cannot be validated by code alone.
- **Implemented**: automated or manual acceptance evidence exists for the current scope.

## Release gate

The vertical slice is not ready for expansion until every row is either:

- `Implemented`; or
- explicitly marked `Prototype pending` with an owner, test plan, and scheduled validation.

No additional systemic layer should be added to compensate for an unvalidated player-facing requirement.
