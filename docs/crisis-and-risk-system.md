# Crisis and Risk System

Status: normative pre-implementation design.
Version: 1.0.

## Purpose

Postcard City represents that cities face housing, tourism, economic, infrastructural, health, social, and geopolitical risks. Crises are governance problems: the player prepares, communicates, prioritizes scarce resources, protects residents, restores services, and manages long-term consequences.

The system must remain respectful, non-sensationalist, explainable, accessible, and playable. It must not turn real suffering into spectacle or reduce complex events to a single random punishment.

## Event families

The catalog may include natural hazards, infrastructure and building failures, transport and industrial accidents, public-health events, deliberate violence, geopolitical shocks, social and economic shocks, housing crises, demographic shifts, cyber incidents, corruption, institutional failures, and slow environmental emergencies.

Biological hazards are represented at a high level, without operational pathogen or attack instructions. Terrorism and war are governance scenarios, not tactical combat simulations.

## Complexity levels

| Level | Intended audience | Crisis behavior |
|---|---|---|
| Relaxed | first play and accessibility | Major, readable events; generous warnings; simplified response choices; biological, war, and terrorism events disabled by default |
| Standard | default experience | Natural hazards, accidents, infrastructure failures, epidemics, and economic shocks with warnings and recovery windows |
| Advanced | experienced players | Adds terrorism, organized violence, refugee shocks, cascading failures, misinformation, and tighter budgets |
| Expert | simulation-focused players | Adds correlated risks, compound crises, uncertain information, long recovery, regional spillovers, geopolitical shocks, and irreversible trade-offs |

Players may enable or disable event families separately. Difficulty must not hide essential information from players with accessibility needs.

## Risk lifecycle

Every implemented crisis follows four phases:

1. Prevention: inspections, reserves, redundancy, planning, public-health capacity, building standards, and economic preparation.
2. Preparedness: alerts, stockpiles, staffing, shelters, evacuation plans, communications, mutual-aid agreements, and continuity plans.
3. Response: protect life, maintain essential services, allocate emergency funds, communicate, coordinate agencies, and avoid disproportionate harm.
4. Recovery: rebuild, compensate, investigate, reform weak systems, restore trust, support displaced residents, and learn from the event.

A crisis may be mitigated, worsened, or redirected by earlier policy. It must not be a context-free dice roll.

## Consequences and information

Consequences are tracked separately across people and displacement, housing and infrastructure, health and essential services, budget and debt, tourism and employment, trust and institutional legitimacy, migration, regional spillovers, and public memory.

The model distinguishes direct damage, prevented damage, response cost, recovery cost, distributional impact, uncertainty, and avoidable contribution from prior policy. No crisis is scored only as win or lose.

Before an event, signals are proportional to preparedness and information quality. During response, reports may be incomplete but must identify uncertainty. After recovery, the game explains what happened, what was known, which preparations helped, who bore the costs, and what remains unresolved.

## Safety and representation

- No gore or graphic imagery is required for gameplay.
- No event produces arbitrary instant death as a difficulty mechanic.
- Biological hazards remain abstract and high-level.
- Terrorism and war are governance scenarios, not tactical combat simulations.
- The system supports content filtering and event-family opt-outs.
- A crisis never targets protected groups through hidden deterministic bias.
- Accessibility mode may pause, simplify, or defer crisis decisions without penalizing the player.

## First vertical slice

The first vertical slice uses one non-deliberate crisis, such as a heat wave, flood, or unsafe-building incident. It must exercise prevention, preparedness, response, recovery, player-readable causal explanation, bounded consequences, and deterministic tests.

Deliberate violence, biological hazards, and war belong to later validated scenarios, not the first vertical slice.

## Implementation gate

Before adding crisis code, each event family requires a catalog entry, lifecycle decisions, bounded consequences, deterministic tests, an explanation report, complexity and opt-in rules, sensitivity review, localization keys, and respectful content review.
