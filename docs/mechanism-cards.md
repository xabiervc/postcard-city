# Mechanism Cards

## What a card represents
A mechanism card describes how an intervention could produce outcomes in a particular context. It is not a morality label and not a universal policy verdict.

Each card separates:
- Intervention parameters.
- Context variables.
- Actor mechanism.
- Outcomes and delays.
- Fiscal and social ledgers.
- Evidence and certainty.
- Alternative configurations.
- Expected behaviours used as tests.

The structure follows the context-mechanism-outcome logic used in realist evaluation: what works, for whom, in what respects, to what extent, in what contexts, and how. It is adapted for a deterministic game simulation.

## Player-facing presentation
Every decision can expose:

1. **Policy:** what the government is changing.
2. **Why it might work:** the actor behaviour expected to change.
3. **Conditions:** the local variables that enable or block that mechanism.
4. **Estimated effects:** central estimate plus low/high range and lag.
5. **Who gains and who pays:** fiscal and distributional ledgers.
6. **Evidence quality:** evidence level and limitations.
7. **Robustness:** robust, context-dependent, or fragile after parameter variation.

The casual mode collapses this into a clear summary. Advanced modes expose sources, alternative specifications, and sensitivity results.

## Initial card set
- `str-regulation`: regulate short-term rentals; enforcement determines whether owners change behaviour.
- `social-housing`: construct and operate social housing; affordability and arrears determine fiscal sustainability.
- `public-land-disposal`: sell or lease public parcels; immediate capital and long-term control trade off.
- `public-housing-disposal`: sell public housing; short-term receipts trade off against future stock and tenant security.
- `rent-regulation`: regulate rent growth; effects depend on coverage, enforcement, market tightness, and landlord exit.
- `upzoning`: relax density or land-use restrictions; added capacity depends on development feasibility and actual build-out.
- `expropriation`: acquire large private portfolios; effects depend on legal cost, compensation, management capacity, and construction alternatives.

The first vertical slice should wire `str-regulation`, `social-housing`, and `public-land-disposal`. The remaining cards stay available for later implementation and scenario authoring.
