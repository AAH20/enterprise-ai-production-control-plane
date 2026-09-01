from __future__ import annotations

import json
import argparse
from dataclasses import fields
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .controller import ControlPlane
from .models import Provider, Telemetry, Workload


def _strict(cls: type[Any], value: dict[str, Any]) -> Any:
    allowed = {item.name for item in fields(cls)}
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"unknown {cls.__name__} fields: {sorted(unknown)}")
    return cls(**value)


class Handler(BaseHTTPRequestHandler):
    server_version = "AIControl/0.1"

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"/health", "/ready"}:
            self._send(200, {"status": "ok", "evidence": "runtime"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/evaluate":
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                raise ValueError("body size must be between 1 and 1000000 bytes")
            body = json.loads(self.rfile.read(length))
            providers = [_strict(Provider, item) for item in body["providers"]]
            workload = _strict(Workload, body["workload"])
            telemetry = _strict(Telemetry, body["telemetry"])
            result = ControlPlane(providers).evaluate(workload, telemetry, set(body.get("unavailable", [])))
            self._send(200, result)
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": str(exc)})

    def log_message(self, format: str, *args: Any) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    ThreadingHTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the AI production control-plane API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    serve(args.host, args.port)
