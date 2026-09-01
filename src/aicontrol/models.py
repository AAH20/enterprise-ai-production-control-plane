from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Provider:
    name: str
    model: str
    input_per_million: float
    output_per_million: float
    infrastructure_per_hour: float
    capacity_rpm: int
    base_latency_ms: int
    quality_score: float
    availability: float = 0.999
    locality: str = "cloud"


@dataclass(frozen=True)
class Workload:
    workflow_id: str
    tenant: str
    input_tokens: int
    output_tokens: int
    value_usd: float
    quality_floor: float
    latency_slo_ms: int
    residency: str = "any"
    criticality: str = "standard"


@dataclass(frozen=True)
class Telemetry:
    latency_ms: int
    quality_score: float
    success: bool
    gpu_utilization: float
    retries: int = 0
    cache_hit: bool = False
    provider_error: bool = False
    provider: str = ""


@dataclass(frozen=True)
class Decision:
    workflow_id: str
    provider: str
    model: str
    action: str
    reason: str
    estimated_cost_usd: float
    expected_margin_usd: float
    evidence_class: str = "simulated"
    constraints: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["constraints"] = list(self.constraints)
        return result
