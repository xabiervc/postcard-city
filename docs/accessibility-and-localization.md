# Accessibility and Localization

## Accessibility goals
Accessibility is a product requirement, not a post-production checklist.

## Required features
- UI scale.
- Readable default typography.
- High-contrast mode.
- Color-blind-safe palettes and non-color indicators.
- Remappable controls.
- Keyboard and controller support where applicable.
- Pause and adjustable simulation speed.
- Full subtitles and captions.
- Reduced motion mode.
- Reduced flashing and screen effects.
- Screen-reader-aware UI structure where supported.
- Clear notification priority.
- Executive and detailed information views.
- Tooltips with plain-language explanations.

## Complexity accessibility
Casual mode summarizes systems. Advanced modes expose detail. Players can inspect causes without being forced to manage every variable.

## Localization architecture
All player-facing text uses stable localization keys. No user-facing string is hardcoded in gameplay logic. Variables, pluralization, gender, date, time, currency, and number formatting are locale-aware.

## Initial language plan
English and Spanish are first-class launch candidates. Additional languages should be added through the same key contract and reviewed by native-language editors. Machine translation may assist drafting but cannot be the final quality gate.

## Text design
UI must tolerate expansion. Event text must include speaker, tone, context, and variable metadata. Avoid embedding assumptions about grammar or word order in concatenated strings.

## Localization QA
- Missing-key scans.
- Placeholder validation.
- Length and overflow checks.
- Pseudolocalization.
- Native review.
- Screenshot review for major screens.
- Audio/subtitle synchronization where voice exists.
