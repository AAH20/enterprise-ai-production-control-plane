from __future__ import annotations

import argparse
import json
from pathlib import Path

from .controller import ControlPlane
from .io import load_scenario


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate an AI production routing and incident scenario")
    parser.add_argument("scenario", help="JSON scenario file")
    parser.add_argument("--output", help="write the evidence receipt to a file")
    args = parser.parse_args()
    providers, workload, telemetry, unavailable = load_scenario(args.scenario)
    result = ControlPlane(providers).evaluate(workload, telemetry, unavailable)
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

