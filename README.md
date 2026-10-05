# Postcard City

> Govern a living region. Build a destination. Decide what remains when the visitors leave.

## Status

**Preimplementation / deterministic simulation prototype**

The repository contains the first executable proof of the simulation contract. It is not yet a complete game or final production architecture.

## Game overview

Postcard City is a political regional city simulator about tourism, housing, employment, public services, economic diversification, power, media, and livability.

Every run begins with a different region: a coastal historic city, an inland provincial capital, a shrinking industrial area, a commuter belt, a newly planned city, a university town, a port, or another coherent urban case. Each region has its own history, initial condition, political landscape, opportunities, crises, and hidden liabilities.

The player governs as an elected regional or metropolitan leader. They must balance private investment, tourism, housing, worker accessibility, healthcare, transport, employment, institutional trust, public finances, political support, media pressure, and opposition.

The central question is not whether tourism is good or bad. It is whether a region can become a successful destination without becoming impossible to live in.

## Design north star

> **Turn a region into a destination without making it impossible to live there.**

## What makes it different

Postcard City is not a conventional empty-grid city builder and not a literal theme-park manager.

- Construction is a policy instrument, not the entire game.
- Tourism is a transforming force, not just an income source.
- Housing, jobs, services, and transport are connected.
- Economic opportunities can be beneficial, predatory, speculative, fraudulent, or simply misjudged.
- Elections, opposition, journalists, media funding, leaks, and scandals make information and legitimacy part of the simulation.
- Procedural variation creates coherent regional cases rather than random maps without context.
- Complexity can be reduced or expanded without removing the core fantasy.

## Core gameplay loop

1. Inspect the region and understand its visible and hidden pressures.
2. Consult residents, workers, institutions, companies, media, and opposition.
3. Evaluate opportunities, proposals, warnings, and incomplete information.
4. Choose a policy, investment, regulation, communication strategy, or compromise.
5. Advance time and let delayed effects emerge.
6. Observe changes in neighbourhoods, services, employment, housing, transport, trust, and politics.
7. Respond to protests, investigations, scandals, crises, elections, and new opportunities.
8. Review the mandate and decide what kind of region you are creating.

## Major systems planned

### Tourism and the postcard effect

Tourism brings visitors, jobs, tax revenue, investment, and cultural attention. It can also increase housing pressure, congestion, seasonal employment, service demand, and the conversion of homes and local businesses into visitor infrastructure.

The region can visually evolve from a living city to a mixed destination, a branded tourist district, or a polished but hollow postcard.

### Housing and displacement

Housing is divided between residential use, short-term rentals, worker accommodation, vacant units, and other uses. The player must decide whether to protect residential capacity, allow conversion, subsidise housing, regulate rents, build outward, or accept displacement.

### Work, services, and distance

A building does not automatically make a service functional. Hospitals, schools, transport, emergency services, and businesses require people who can afford to live within a workable distance.

The same policy that raises property values can make it harder to recruit nurses, teachers, cleaners, drivers, technicians, and other essential workers.

### Economic diversification

Industry, universities, technology, logistics, energy, culture, healthcare, and other sectors appear as context-sensitive opportunities. A healthy, connected, affordable region can attract better investments. A degraded region may attract only extractive, speculative, low-quality, or heavily subsidised projects.

### Politics and elections

The player governs through mandates and must maintain enough support to remain effective. Citizens, businesses, institutions, unions, media, and opposition parties care about different outcomes. Political identity emerges from the player’s pattern of decisions rather than a simple good-versus-evil selection.

### Media, journalists, and scandals

News organizations have resources, audiences, ownership, credibility, and editorial independence. A hidden fact may become a lead, then an investigation, then a verified story, then a political crisis. Public subsidies can strengthen local journalism and pluralism, or become a tool of dependence and capture.

### Projects and promises

Major projects arrive with public claims, private interests, infrastructure demands, legal requests, labour needs, uncertainty, and possible hidden liabilities. The player must distinguish private profit from public value and promised jobs from delivered jobs.

### Procedural regional cases

A region is generated through compatible templates, parameters, arcs, actors, opportunities, and crises. Replayability comes primarily from different causal situations and decision pressure, not only from cosmetic map variation.

## Game modes planned

- **Campaign:** authored scenarios introduce the systems progressively.
- **Scenario:** a complete regional problem with a defined evaluation horizon.
- **Sandbox:** indefinite governance with periodic reports and configurable crises.
- **Custom:** per-system complexity, information, crisis, and political settings.

## Complexity modes planned

- **Casual:** executive summaries, aggregated systems, clear recommendations, limited crisis pressure.
- **Standard:** housing, tourism, employment, services, transport, budget, basic politics, media, and opposition.
- **Advanced:** uncertainty, contracts, corruption, deeper factions, information asymmetry, and investigative chains.
- **Custom:** individual system resolution and rule configuration.

## Current vertical slice

### The Overheated Destination

A coastal historic metropolitan region has a profitable tourist centre, rising housing pressure, a car-dependent outer district, and an understaffed public hospital.

Aurora Leisure proposes a large hotel and entertainment district. The proposal promises visitors, jobs, tax income, and transport investment. Its hidden risks concern financing, worker quality, public infrastructure costs, legal exceptions, housing pressure, and long-term dependence.

The current prototype supports four initial approaches:

- Approve the proposal.
- Reject it.
- Renegotiate it with safeguards.
- Delay it for an audit.

The intended outcomes include a tourist boom with service stress, a slower but safer compromise, a rejected project with alternative development, and a political or institutional crisis.

## Prototype

The current prototype is deliberately engine-agnostic and focuses on causal simulation before final presentation.

Implemented:

- Deterministic monthly ticks.
- Seeded initial state.
- Aggregate districts.
- Tourism growth and tax revenue.
- Residential-to-short-term-rental conversion.
- Rent pressure.
- Worker accessibility proxy.
- Healthcare staffing pressure.
- Transport reliability.
- Budget updates.
- Aurora Leisure decision options.
- Delayed warnings and housing protests.
- Executive and causal reporting.
- Scenario content validation.
- Automated reproducibility tests.

Run locally:

```bash
python -m pip install -e ".[dev]"
pytest
python -m postcard_city.cli --months 12 --decision renegotiate
python tools/validate_content.py
```

The CLI also supports an explicit decision month and transition trace output in the current prototype.

## Repository structure

- `src/postcard_city/`: deterministic domain and simulation prototype.
- `data/`: authored scenario content.
- `docs/`: product, design, simulation, technical, accessibility, and quality documentation.
- `schemas/`: machine-readable content contracts.
- `config/`: design and vertical-slice configuration.
- `tests/`: automated tests.
- `tools/`: validation and prototype tools.
- `.github/workflows/`: continuous integration.

## Development principles

1. Protect the core fantasy: govern a living region under pressure.
2. Make causes and consequences inspectable.
3. Prefer systemic consequences over moral labels.
4. Do not make tourism automatically good or bad.
5. Treat corruption as institutional debt, not a binary morality switch.
6. Keep residents, workers, institutions, businesses, media, and opposition distinct.
7. Use authored arcs around procedural variation.
8. Scale complexity without removing the core experience.
9. Build accessibility and localization into the architecture from day one.
10. Require deterministic tests for major simulation rules.

## Quality target

The project aims for an award-level standard comparable with the design, narrative, accessibility, presentation, and technical polish expected by The Game Awards, the D.I.C.E. Awards, the BAFTA Games Awards, and the Game Developers Choice Awards.

That ambition is treated as a set of gates, not a slogan:

- Decisions must be understandable but not trivial.
- Multiple strategies must remain viable.
- Outcomes must be visible, traceable, and emotionally meaningful.
- Procedural scenarios must be coherent and recoverable.
- The interface must support both overview and deep inspection.
- Accessibility must be designed in, not patched in.
- Saves, seeds, content, and simulation results must be reliable and testable.

## Roadmap

### Phase 0 — Preimplementation
Product definition, simulation boundaries, schemas, vertical slice, technical risks, accessibility, localization, and quality gates.

### Phase 1 — Simulation prototype
Deterministic monthly simulation, causal traces, state inspection, serialization, and invariant tests.

### Phase 2 — Vertical slice
A small visual region, executive and detailed UI, media and opposition reaction, one election, complete evaluation, and accessibility baseline.

### Phase 3 — Systems expansion
Procedural scenario generation, industry opportunities, more crises, deeper political actors, scalable complexity, and authoring tools.

### Phase 4 — Production
Multiple regional templates, campaign scenarios, sandbox, art, audio, narrative content, additional languages, and extensive playtesting.

### Phase 5 — Polish
Performance, accessibility audit, localization QA, onboarding, UX refinement, stability, balance, and final quality review.

## License

All rights reserved. See `LICENSE.md`.
