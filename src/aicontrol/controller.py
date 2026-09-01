from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .economics import calculate
from .evidence import receipt
from .incidents import diagnose
from .models import Provider, Telemetry, Workload
from .router import choose_provider


class ControlPlane:
    def __init__(self, providers: list[Provider]) -> None:
        if not providers:
            raise ValueError("at least one provider is required")
        self.providers = providers

    def evaluate(self, workload: Workload, telemetry: Telemetry, unavailable: set[str] | None = None) -> dict[str, Any]:
        decision = choose_provider(workload, self.providers, unavailable)
        observed_name = telemetry.provider or decision.provider
        observed_provider = next((item for item in self.providers if item.name == observed_name), None)
        economics = calculate(workload, observed_provider, telemetry).as_dict() if observed_provider else None
        incident = diagnose(workload, telemetry).as_dict()
        payload = {
            "workload": asdict(workload),
            "telemetry": asdict(telemetry),
            "observed_provider": observed_name,
            "routing_decision": decision.as_dict(),
            "economics": economics,
            "incident_decision": incident,
        }
        return receipt(payload)
