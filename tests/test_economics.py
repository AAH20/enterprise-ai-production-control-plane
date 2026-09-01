import unittest

from aicontrol.economics import calculate, estimate_cost
from aicontrol.models import Provider, Telemetry, Workload


class EconomicsTests(unittest.TestCase):
    def test_token_and_infrastructure_cost_are_combined(self):
        provider = Provider("p", "m", 1.0, 2.0, 3.6, 100, 1000, 0.9)
        workload = Workload("w", "t", 1_000_000, 1_000_000, 10.0, 0.8, 2000)
        self.assertEqual(estimate_cost(workload, provider, 1000), 3.001)

    def test_failed_quality_has_no_realized_value(self):
        provider = Provider("p", "m", 1.0, 1.0, 0.0, 100, 100, 0.9)
        workload = Workload("w", "t", 1000, 1000, 5.0, 0.9, 1000)
        result = calculate(workload, provider, Telemetry(100, 0.7, True, 0.2))
        self.assertEqual(result.realized_value_usd, 0.0)
        self.assertIsNone(result.cost_per_success_usd)


if __name__ == "__main__":
    unittest.main()

