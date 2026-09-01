from __future__ import annotations

from dataclasses import dataclass

from .models import Provider, Telemetry, Workload


@dataclass(frozen=True)
class Economics:
    model_cost_usd: float
    infrastructure_cost_usd: float
    retry_cost_usd: float
    total_cost_usd: float
    realized_value_usd: float
    margin_usd: float
    cost_per_success_usd: float | None

    def as_dict(self) -> dict[str, float | None]:
        return self.__dict__.copy()


def estimate_cost(workload: Workload, provider: Provider, duration_ms: int | None = None) -> float:
    token_cost = (
        workload.input_tokens * provider.input_per_million
        + workload.output_tokens * provider.output_per_million
    ) / 1_000_000
    elapsed = duration_ms if duration_ms is not None else provider.base_latency_ms
    infrastructure_cost = provider.infrastructure_per_hour * elapsed / 3_600_000
    return round(token_cost + infrastructure_cost, 8)


def calculate(workload: Workload, provider: Provider, telemetry: Telemetry) -> Economics:
    base = estimate_cost(workload, provider, telemetry.latency_ms)
    retry_cost = base * telemetry.retries
    total = base + retry_cost
    value = workload.value_usd if telemetry.success and telemetry.quality_score >= workload.quality_floor else 0.0
    return Economics(
        model_cost_usd=round((workload.input_tokens * provider.input_per_million + workload.output_tokens * provider.output_per_million) / 1_000_000, 8),
        infrastructure_cost_usd=round(provider.infrastructure_per_hour * telemetry.latency_ms / 3_600_000, 8),
        retry_cost_usd=round(retry_cost, 8),
        total_cost_usd=round(total, 8),
        realized_value_usd=round(value, 4),
        margin_usd=round(value - total, 8),
        cost_per_success_usd=round(total, 8) if value else None,
    )

