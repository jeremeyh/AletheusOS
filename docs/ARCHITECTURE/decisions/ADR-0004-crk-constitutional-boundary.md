# ADR-0004: Constitutional Runtime Kernel Boundary

- **Status:** Proposed
- **Decision type:** Constitutional architecture
- **Permanence:** Enduring
- **Owner:** Constitutional Runtime

## Context

A Constitutional Runtime Kernel™ has been proposed to enforce platform invariants. The repository already contains runtime, registry, governance, ledger, event, lifecycle, security, civilization, and application authorities.

Creating another implementation without first resolving those authorities would introduce duplicate ownership and risk creating a second composition root.

## Decision

The CRK shall be a lightweight constitutional admission and invariant boundary.

### The CRK may own

- Constitutional capability admission contracts.
- Kernel-level invariant evaluation.
- Typed admission and rejection results.
- Composition of existing constitutional authorities.
- Kernel admission-event requests through the existing event authority.

### The CRK shall not own

- Domain business logic.
- Application authorization.
- Lifecycle execution already owned by runtime and application managers.
- A second application, service, runtime, or civilization registry.
- Evidence persistence.
- Replay persistence.
- Ledger persistence.
- Event-bus implementation.
- Mission execution.
- Governance deliberation.
- Security-domain policy.

## Consequences

- Existing constitutional authorities remain authoritative.
- The CRK composes those authorities through bounded contracts.
- The CRK must remain deterministic, typed, small, and independently testable.
- Unresolved ownership conflicts must be reviewed before kernel implementation.

## Evidence

- `reports/architecture/crk_constitutional_ownership_map.md`
- `reports/architecture/crk_constitutional_ownership_map.json`

## Constitutional Alignment

- One Owner Per Concept.
- Composition Before Creation.
- Bounded Growth.
- Constitutional Restraint.
- No Orphan Architecture.
