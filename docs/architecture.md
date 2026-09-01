# Production architecture and trust boundaries

## Planes

1. **Transaction plane:** business workflow IDs, tenant, declared value and criticality.
2. **Execution plane:** agent graph, model calls, retrieval, tools, APIs and durable state.
3. **Infrastructure plane:** Kubernetes, GPU/CPU, network, storage and provider health.
4. **Decision plane:** constraint evaluation, routing, economics and incident diagnosis.
5. **Evidence plane:** evaluation results, releases, remediation approvals and receipts.

## Correlation contract

Every production span should carry `workflow.id`, `tenant.id`, `model.provider`, `model.name`, `prompt.version`, `evaluation.version`, `deployment.id`, `k8s.cluster`, `k8s.pod`, `gpu.profile`, `business.value_usd` and `evidence.class` where authorized. Sensitive values belong in governed systems, not span attributes.

## Failure containment

- Provider keys come from workload identity or a secret manager, never scenario files.
- Provider routing cannot weaken residency or quality floors.
- Critical workflow provider changes require approval.
- Generated remediation is advisory until a scoped automation identity and policy approve it.
- Write actions require idempotency keys and durable workflow state.
- A model cannot approve its own evaluation threshold reduction.
- Evidence storage requires authenticated signing and controlled custody before a digest can support non-repudiation claims.

## Availability design

The Kubernetes contract uses two replicas, readiness/liveness checks, a disruption budget and horizontal scaling. Production designs additionally require topology spread, multi-zone nodes, external state, tested backup/restore, capacity reservations and provider-specific failure drills.

## What is deliberately absent

The repository contains no provider credentials, fabricated Grafana screenshots, claimed GPU measurements or production customer data. Those artifacts must be generated from an authorized environment and labelled `deployed`.

