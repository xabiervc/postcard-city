# Godot playable demo

This branch now contains the first complete playable crisis loop for Postcard City.

## Playable slice

1. Begin with a dated postcard and a stylised district map.
2. Advance to month 1 to reveal a hospital staffing crisis at a named location.
3. Compare two interventions with explicit cost, benefit and risk.
4. Confirm one decision through the simulation session adapter.
5. Advance time to reveal changes in budget, housing, staffing and district health.
6. Read differentiated reactions from a resident, a healthcare worker and an archivist.
7. Review the causal event log.
8. Compare the before and after postcards with the recorded decision.
9. Reach a provisional outcome after the six-month slice.

## Controls and accessibility baseline

- The flow is driven by focusable Godot buttons and can be completed with keyboard navigation.
- The timeline exposes advance and pause controls.
- The event log and testimony panel provide text alternatives for map and outcome changes.
- The demo keeps cause and consequence in readable text rather than relying only on colour.

## Architecture boundary

The current `SimulationSession` is a deterministic local adapter for this slice. It is not yet the authoritative Python simulation. The intended production boundary is:

```text
Python simulation core → versioned session adapter → Godot view model → UI
```

The next integration should replace the local transition rules with the Python gateway without changing the decision, event, map or postcard contracts.
