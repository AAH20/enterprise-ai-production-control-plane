from __future__ import annotations

from .economics import estimate_cost
from .models import Decision, Provider, Workload


def choose_provider(workload: Workload, providers: list[Provider], unavailable: set[str] | None = None) -> Decision:
    unavailable = unavailable or set()
    feasible: list[tuple[float, Provider, tuple[str, ...]]] = []
    rejected: list[str] = []
    for provider in providers:
        constraints: list[str] = []
        if provider.name in unavailable:
            rejected.append(f"{provider.name}:unavailable")
            continue
        if provider.quality_score < workload.quality_floor:
            rejected.append(f"{provider.name}:quality")
            continue
        if provider.base_latency_ms > workload.latency_slo_ms:
            rejected.append(f"{provider.name}:latency")
            continue
        if workload.residency != "any" and provider.locality not in {workload.residency, "sovereign"}:
            rejected.append(f"{provider.name}:residency")
            continue
        cost = estimate_cost(workload, provider)
        if provider.availability < 0.999:
            constraints.append("availability-below-three-nines")
        feasible.append((cost, provider, tuple(constraints)))

    if not feasible:
        return Decision(
            workflow_id=workload.workflow_id,
            provider="none",
            model="none",
            action="escalate",
            reason="no provider satisfies hard constraints: " + ", ".join(rejected),
            estimated_cost_usd=0.0,
            expected_margin_usd=0.0,
            constraints=tuple(rejected),
        )

    cost, provider, constraints = min(feasible, key=lambda row: (row[0], -row[1].quality_score))
    return Decision(
        workflow_id=workload.workflow_id,
        provider=provider.name,
        model=provider.model,
        action="route",
        reason="lowest estimated cost among providers satisfying quality, latency and residency",
        estimated_cost_usd=cost,
        expected_margin_usd=round(workload.value_usd - cost, 8),
        constraints=constraints,
    )

