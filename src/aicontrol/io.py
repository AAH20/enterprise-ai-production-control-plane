from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Provider, Telemetry, Workload


def load_scenario(path: str | Path) -> tuple[list[Provider], Workload, Telemetry, set[str]]:
    data: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
    providers = [Provider(**provider) for provider in data["providers"]]
    return providers, Workload(**data["workload"]), Telemetry(**data["telemetry"]), set(data.get("unavailable", []))

