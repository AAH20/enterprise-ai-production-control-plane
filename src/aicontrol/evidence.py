from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def receipt(payload: dict[str, Any], evidence_class: str = "simulated") -> dict[str, Any]:
    envelope = {
        "schema": "aicontrol.evidence.v1",
        "evidence_class": evidence_class,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    canonical = json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode()
    envelope["sha256"] = hashlib.sha256(canonical).hexdigest()
    envelope["integrity_note"] = "Tamper-evident digest; not identity, custody or non-repudiation proof."
    return envelope

