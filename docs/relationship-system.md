# Relationship System

## Purpose

Relationships express political and social trust between the player and recurring perspectives. They make consequences persistent without adding a full dialogue-RPG layer.

## Relationship dimensions

Each relationship has three bounded dimensions from 0 to 1:

- trust: belief that the player is acting in good faith;
- alignment: agreement with current priorities;
- voice: willingness and ability to influence public decisions.

## Change rules

Relationships change through:

- decisions that affect a character's interests;
- whether promised mitigation is delivered;
- visible costs and delayed consequences;
- whether testimony is acknowledged in the record;
- crisis choices that allocate scarce protection.

## Player-facing feedback

The player should see:

- a short explanation of the relationship change;
- the affected interest;
- whether the change is temporary or persistent;
- a testimony or trace supporting the change.

## Design boundaries

- Relationships do not replace system metrics.
- Relationship changes must not be random when the causal reason is known.
- A high relationship score cannot erase material harm.
- A low relationship score does not make a character irrational or hostile by default.
- The vertical slice uses four relationships and no more than three visible dimensions.

## Minimal data shape

```json
{
  "character_id": "mara-soler",
  "trust": 0.5,
  "alignment": 0.5,
  "voice": 0.5,
  "last_change_reason": "..."
}
```
