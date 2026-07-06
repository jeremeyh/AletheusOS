# Genesis 6 Integration Baseline 01

This patch stabilizes the runtime after the Runtime Kernel Bus / Composition Root work.

## Purpose

Remove references to manager modules that do not exist yet and keep only the Genesis 6 components that currently exist:

- Runtime Composition Root
- Runtime Kernel Bus
- Registry Circuit
- Execution Circuit
- Registry Manager
- Runtime Registry v2
- Health Monitor
- CTF v1
- Extracted command modules

## What was removed from `runtime/core.py`

Imports and direct initialization for not-yet-built managers such as:

- LifecycleManager
- ServiceManager
- PipelineManager
- WorkflowManager
- EngineManager
- HealthManager
- MetricsManager
- SecurityManager
- GovernanceManager
- SPAManager

These will be built and integrated later, one at a time.

## Verification

```bash
python -m py_compile aletheus/runtime/core.py
streamlit run app.py
```

## Notes

This is a stabilization baseline, not a feature expansion.
