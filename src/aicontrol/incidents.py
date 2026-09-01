from __future__ import annotations

from dataclasses import dataclass

from .models import Telemetry, Workload


@dataclass(frozen=True)
class IncidentDecision:
    severity: str
    diagnosis: str
    action: str
    approval_required: bool
    revenue_at_risk_usd: float

    def as_dict(self) -> dict[str, str | bool | float]:
        return self.__dict__.copy()


def diagnose(workload: Workload, telemetry: Telemetry) -> IncidentDecision:
    revenue = workload.value_usd
    if telemetry.provider_error:
        return IncidentDecision("critical", "model provider unavailable", "failover-provider", workload.criticality == "critical", revenue)
    if telemetry.gpu_utilization >= 0.95 and telemetry.latency_ms > workload.latency_slo_ms:
        return IncidentDecision("high", "GPU saturation is exhausting the latency budget", "scale-or-reroute", False, revenue)
    if telemetry.quality_score < workload.quality_floor:
        return IncidentDecision("high", "quality regression below release floor", "rollback-model-prompt", True, revenue)
    if telemetry.latency_ms > workload.latency_slo_ms:
        return IncidentDecision("medium", "dependency or inference latency exceeded SLO", "inspect-trace-and-degrade", False, revenue)
    if not telemetry.success:
        return IncidentDecision("high", "workflow failed without a classified infrastructure symptom", "pause-and-escalate", True, revenue)
    return IncidentDecision("none", "workflow healthy", "observe", False, 0.0)

