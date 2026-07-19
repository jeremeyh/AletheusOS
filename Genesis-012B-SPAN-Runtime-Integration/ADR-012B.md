# ADR-012B: Bounded SPAN Runtime Integration

## Status

Accepted for installation.

## Decision

SPAN is integrated through a bounded adapter layer under `aletheus.strategic.runtime`.

Existing AletheusOS authorities remain authoritative for:

- service registration
- lifecycle orchestration
- event publication
- health
- telemetry
- constitutional records
- council review

The adapter uses structural protocols and dependency injection so it can compose with the repository's current authorities without importing or replacing their concrete implementations.

## Constitutional boundary

SPAN may analyze and recommend. It may not directly execute architectural mutations.
