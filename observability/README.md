# Observability contract

The Grafana dashboard defines the business-to-infrastructure views expected from a production adapter. It is not a screenshot of live telemetry.

Required metric families:

- `ai_workflow_total` and `ai_workflow_success_total`
- `ai_workflow_cost_usd`
- `ai_workflow_value_usd`
- `ai_workflow_latency_ms`
- `ai_evaluation_quality_score`
- `ai_gpu_allocated_ratio`
- NVIDIA DCGM metrics such as `DCGM_FI_DEV_GPU_UTIL`

Metrics must avoid customer payloads and high-cardinality workflow identifiers. Use traces for per-workflow correlation, with governed access and retention.
