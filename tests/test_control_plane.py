import unittest

from aicontrol.controller import ControlPlane
from aicontrol.models import Provider, Telemetry, Workload
from aicontrol.router import choose_provider


def providers():
    return [
        Provider("premium", "large", 3.0, 12.0, 0.0, 1000, 800, 0.95, locality="eu"),
        Provider("nim", "open-70b", 0.0, 0.0, 4.0, 500, 600, 0.90, locality="eu"),
        Provider("small", "small", 0.2, 0.8, 0.0, 3000, 250, 0.80, locality="global"),
    ]


def workload():
    return Workload("wf-1", "tenant", 4000, 500, 10.0, 0.89, 1000, "eu")


class RoutingTests(unittest.TestCase):
    def test_chooses_cheapest_feasible_provider(self):
        decision = choose_provider(workload(), providers())
        self.assertEqual(decision.provider, "nim")
        self.assertGreater(decision.expected_margin_usd, 9.99)

    def test_failover_excludes_unavailable_provider(self):
        decision = choose_provider(workload(), providers(), {"nim"})
        self.assertEqual(decision.provider, "premium")

    def test_escalates_when_no_provider_meets_constraints(self):
        strict = Workload("wf-2", "tenant", 100, 100, 1.0, 0.99, 100, "eu")
        self.assertEqual(choose_provider(strict, providers()).action, "escalate")

    def test_receipt_contains_explicit_evidence_boundary(self):
        result = ControlPlane(providers()).evaluate(
            workload(), Telemetry(1800, 0.90, True, 0.97, retries=1)
        )
        self.assertEqual(result["evidence_class"], "simulated")
        self.assertEqual(result["payload"]["incident_decision"]["action"], "scale-or-reroute")
        self.assertEqual(result["payload"]["observed_provider"], "nim")
        self.assertEqual(len(result["sha256"]), 64)
        self.assertIn("not identity", result["integrity_note"])


if __name__ == "__main__":
    unittest.main()
