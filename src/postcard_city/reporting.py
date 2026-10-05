from __future__ import annotations

from .model import RegionState


def executive_report(state: RegionState) -> str:
    metrics = state.metrics
    return "\n".join([
        f"Month: {state.month}",
        f"Project: {state.project_status}",
        f"Budget: €{state.budget / 1_000_000:.1f}M",
        f"Tourist visitors/month: {state.tourism_visitors:,.0f}",
        f"Housing affordability: {metrics.get('housing_affordability', 0):.0%}",
        f"Worker accessibility: {metrics.get('worker_accessibility', 0):.0%}",
        f"Healthcare staffing: {metrics.get('healthcare_staffing', 0):.0%}",
        f"Tourism pressure: {metrics.get('tourism_pressure', 0):.0%}",
        f"Institutional trust: {state.institutional_trust:.0%}",
        f"Political support: {state.political_support:.0%}",
        f"Events: {', '.join(state.event_history) or 'none'}",
    ])
