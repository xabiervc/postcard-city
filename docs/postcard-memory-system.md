# Postcard Memory System

## Purpose

A postcard is a playable memory of a place, not merely decorative art or an end-of-session screenshot.

## Core interaction

1. The player receives or creates a postcard of a named place.
2. The postcard stores the place, time, visible state, selected testimony, and relevant causal context.
3. The player changes the city through decisions and interventions.
4. The player revisits the same place and compares the current state with the stored postcard.
5. The comparison exposes what improved, what was displaced, and what remains uncertain.

## Stored fields

- place identifier;
- simulation month;
- visible district state;
- selected characters or testimonies;
- relevant metrics and confidence ranges;
- causal trace references;
- player-authored caption or priority;
- unresolved questions.

## Player value

The postcard provides:

- long-term memory for delayed consequences;
- a human-readable record of trade-offs;
- a way to compare the same place across time;
- an archive of the player's values and choices;
- an end-of-slice artifact suitable for reflection and replay.

## Acceptance criteria for the vertical slice

- The player can create or receive a postcard before the first intervention.
- The player can create or receive a second postcard after the delayed consequence.
- The interface identifies at least one improvement and one cost, displacement, or unresolved risk.
- The comparison references at least one visible state, one social perspective, and one causal trace.
- The player can understand the comparison without opening a raw debug panel.

## Implementation boundary

The first prototype may implement postcards as structured records plus a readable comparison view. It does not need final art, sharing, or a complete archive system.

The following require playtesting rather than documentation:

- whether the comparison feels emotionally meaningful;
- whether the player remembers the earlier state;
- whether captions deepen agency rather than create busywork;
- whether the archive encourages replay.
