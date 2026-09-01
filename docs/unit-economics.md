# Unit economics and business-case method

## Required inputs

- model input/output price or allocated GPU-hour price;
- observed execution duration and retry count;
- retrieval, database, tool, network and observability costs;
- workload success definition;
- evaluation quality floor and latency SLO;
- realized value attributable to a successful workflow;
- human review and rework cost.

## Decision hierarchy

1. Reject providers that violate residency, quality or latency constraints.
2. Reject unavailable or capacity-exhausted providers.
3. Compare full cost per successful workflow—not token price alone.
4. Prefer the highest expected margin within reliability constraints.
5. Escalate when no safe option exists.

## Example—not a customer result

Assume 100,000 monthly workflows, $8 attributable value per successful workflow, 90% baseline completion and $0.18 full cost per attempt. Improving completion to 95% while reducing cost to $0.14 would produce:

```text
baseline value  = 100,000 × 0.90 × $8.00 = $720,000
improved value  = 100,000 × 0.95 × $8.00 = $760,000
baseline cost   = 100,000 × $0.18 = $18,000
improved cost   = 100,000 × $0.14 = $14,000
modeled delta   = ($760,000 - $14,000) - ($720,000 - $18,000) = $44,000/month
```

This is a sensitivity example. A real ROI claim requires customer volume, attribution, observed success and fully loaded cost.

## ROI contract

```text
annual net benefit = avoided cost + incremental gross profit - operating cost
ROI = (annual net benefit - implementation cost) / implementation cost
payback months = implementation cost / monthly net benefit
```

Present low, expected and high cases, with each assumption independently editable.

