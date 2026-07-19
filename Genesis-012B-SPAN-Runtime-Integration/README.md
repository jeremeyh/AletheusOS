# Genesis Engineering Drop 012B — SPAN Runtime Integration

This drop makes SPAN/SPARTAN available through a bounded runtime integration layer without replacing AletheusOS runtime authorities.

## Install

From the AletheusOS repository root:

```bash
unzip Genesis-012B-SPAN-Runtime-Integration.zip
cd Genesis-012B-SPAN-Runtime-Integration
bash genesis_012B_install.sh
```

## Validate

```bash
PYTHONPATH=. python -m pytest tests/strategic/runtime -q
python -m compileall aletheus/strategic/runtime
```

## Design

The integration is adapter-first:

- It does not create a second runtime.
- It does not create a second registry.
- It accepts existing registry, event publisher, telemetry, health, ledger, and council authorities through small protocols.
- SPAN remains advisory and cannot directly mutate runtime state.
