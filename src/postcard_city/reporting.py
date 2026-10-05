from __future__ import annotations

from .model import RegionState


def executive_report(state: RegionState) -> str:
    m = state.metrics
    return "\n".join([f"Month: {state.month}", f"Project: {state.project_status}", f"Budget: EUR {state.budget / 1_000_000:.1f}M", f"Permanent population: {m.get('permanent_population', 0):,.0f}", f"Essential-worker net migration: {m.get('essential_worker_net_migration', 0):+,.0f}", f"Housing affordability: {m.get('housing_affordability', 0):.0%}", f"Healthcare staffing: {m.get('healthcare_staffing', 0):.1%}", f"Tourism pressure: {m.get('tourism_pressure', 0):.0%}", f"Public housing net cashflow: EUR {m.get('public_housing_net_cashflow', 0):,.0f}", f"Institutional trust: {state.institutional_trust:.0%}", f"Political support: {state.political_support:.0%}", f"Events: {', '.join(state.event_history) or 'none'}"])


def causal_report(state: RegionState, limit: int | None = None) -> str:
    traces = state.traces if limit is None else state.traces[-limit:]
    return "\n".join(["Causal trace:"] + [f"- Month {t.month}: {t.source} -> {t.target} ({t.amount:+.4f}) because {t.reason}" for t in traces])
