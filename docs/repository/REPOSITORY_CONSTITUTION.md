# AletheusOS Repository Constitution

## Purpose

The AletheusOS repository must grow through bounded, traceable, and reversible structural evolution.

Repository organization is governed by explicit policy rather than ad hoc movement.

## Constitutional Rules

### 1. One Owner Per Concept

Every sovereign architectural concept must have one canonical ownership boundary.

Parallel implementations may exist only when their relationship is explicitly documented as:

- canonical,
- compatibility,
- versioned,
- application-specific,
- experimental,
- migration-only,
- archived, or
- superseded.

### 2. No Automatic Guessing

Repository Steward may automatically move an artifact only when:

- an explicit deterministic rule exists,
- the destination is unambiguous,
- no destination conflict exists,
- the operation is recorded in a rollback manifest.

Low-confidence recommendations remain advisory.

### 3. Root Integrity

The repository root is reserved for:

- canonical documentation,
- build and environment configuration,
- explicitly approved entry points,
- canonical source namespaces,
- repository-governance state.

Unclassified scripts, reports, migrations, generated artifacts, and temporary files are prohibited.

### 4. Bounded Growth

New functionality must be added within an explicit package boundary.

The root and `aletheus/runtime/core.py` must not become accumulation zones.

### 5. Architectural Proof Before Movement

A module must not be relocated across package boundaries until:

- imports are inspected,
- entry-point ownership is verified,
- tests or compilation checks exist,
- migration risk is understood.

### 6. Reversible Stewardship

Every applied structural operation must produce a timestamped manifest.

No destructive change should occur without a traceable record.

### 7. Drift Awareness

Repository Doctor maintains structural snapshots and reports:

- new and removed files,
- new and removed directories,
- root-entry changes,
- naming violations,
- namespace collisions,
- policy violations.

### 8. Sovereign Authority Boundaries

The following families require explicit authority mapping and must not be flattened:

- runtime,
- kernel,
- registry,
- event bus,
- engine,
- governance,
- memory,
- storage,
- Watch Tower,
- Sentinel,
- Guardian,
- Council,
- Spectrum Platform Analyzer.

### 9. Repository Governance Relationship

Repository Doctor observes and diagnoses.

Repository Steward proposes and executes deterministic structural operations.

Spectrum Platform Analyzer evaluates deeper architectural relationships, dependencies, coupling, duplication, and boundary integrity.

Watch Tower observes operational and repository health over time.

Council governs architecture decisions that affect sovereign authority boundaries.
