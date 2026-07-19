# SPAN Runtime Integration

Genesis Drop 012B introduces a bounded runtime facade.

## Runtime contract

`SPANRuntimeService` owns only SPAN/SPARTAN lifecycle coordination. It does not own the platform registry, event bus, telemetry system, ledger, or council.

## Bootstrap

```python
from aletheus.strategic.runtime import install_span_runtime

span_service = install_span_runtime(
    runtime_registry,
    events=constitutional_events,
    telemetry=telemetry,
    ledger=constitutional_ledger,
    council=runtime_council,
)
```

Concrete AletheusOS authorities can be passed directly when their APIs expose the small methods expected by the adapter. If their method names differ, use a thin repository-specific adapter rather than changing authority ownership.
