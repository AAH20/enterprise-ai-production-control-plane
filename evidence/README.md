# Evidence directory

Generated JSON receipts are intentionally ignored. Reproduce them with:

```bash
PYTHONPATH=src python -m aicontrol.cli examples/customer-support-gpu-saturation.json --output evidence/gpu-saturation.json
```

Receipts label synthetic inputs as `simulated`. A SHA-256 digest detects changes to the serialized envelope; it does not prove identity, custody, deployment or non-repudiation.

