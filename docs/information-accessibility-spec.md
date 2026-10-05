# Information Accessibility Specification

## Principle

Accessibility includes the ability to understand a dense, uncertain, causal simulation. Controls alone are insufficient.

## Required options

- full interface scaling;
- responsive panel reflow;
- high-contrast mode;
- reduced motion and reduced animation;
- pause at any time;
- configurable simulation speed;
- keyboard navigation for every action;
- complete controller navigation;
- visible focus state;
- no colour-only encoding;
- redundant icons, labels, patterns, or text for trends;
- configurable text size and line spacing;
- readable tables and charts with text alternatives;
- screen-reader labels for metrics, changes, and causal links;
- text log of events and testimonies;
- plain-language summaries of consequences;
- optional reduction of simultaneous information;
- controls and targets large enough for reliable selection.

## Causal information

Every major intervention must communicate:

- known immediate effect;
- plausible delayed effect;
- affected groups;
- uncertainty or confidence;
- reversibility;
- cost and opportunity cost.

The player must be able to access this information without relying on colour, animation, audio, or hover alone.

## Vertical-slice acceptance criteria

- All primary metrics have a text label and non-colour signal.
- Every chart has a text summary.
- Every major event appears in the event log.
- The causal summary can be read linearly by assistive technology.
- The player can pause before and after each high-consequence decision.
- Reduced-motion mode does not remove essential feedback.
