# Evidence Registry

## Purpose
The evidence registry records what the simulation claims to know, how it knows it, where the evidence applies, and how uncertain the conclusion is. It prevents unsupported numbers from silently becoming game rules.

## Evidence labels
- `high`: repeated, directly relevant, low-bias evidence with consistent results.
- `moderate`: useful evidence with limitations, indirectness, inconsistency, or imprecision.
- `low`: plausible but limited evidence, weak identification, narrow context, or substantial uncertainty.
- `very_low`: projections, expert judgement, contested evidence, or evidence with major unresolved limitations.
- `disputed`: credible sources reach materially different conclusions.
- `assumed`: a design assumption used to make the simulation playable; it is not presented as empirical fact.

These labels are an internal adaptation inspired by certainty-of-evidence frameworks. They are not a formal GRADE assessment.

## Rules
1. Every quantitative effect must reference an evidence record or set `assumed: true`.
2. Evidence is attached to an outcome in a context, not to a policy in the abstract.
3. A source does not automatically validate a causal claim; study design and limitations are recorded.
4. Results from a different country, market, time period, or legal system are marked indirect.
5. Conflicting evidence produces alternative configurations instead of an averaged truth.
6. The game must distinguish empirical findings, model assumptions, and player-defined objectives.
7. Values used for balance but not claimed as real-world estimates are explicitly labelled `design_calibration`.

## Current registry
The machine-readable registry is `data/evidence/evidence-registry.json`. The policy mechanism cards are in `data/mechanisms/housing-policy-cards.json`.

## Current evidence boundary
The first registry deliberately avoids treating unverified figures as facts. It includes verified or directly retrieved records for:
- Short-term-rental effects in Barcelona and Madrid.
- The 180-day short-term-rental cap study in New South Wales.
- Social-housing arrears evidence review and tenant-payment risk reporting.
- Right to Buy history and replacement evidence.
- Madrid public-housing disposal reporting.
- Public-land lease and sale practice examples.
- Conflicting rent-regulation findings.
- Conflicting upzoning findings.
- Berlin expropriation projections and regulatory-risk evidence.

It does not claim that these sources establish universal laws. They are inputs for context-dependent configurations.
