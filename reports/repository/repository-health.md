# AletheusOS Repository Health

Generated: `2026-07-19T09:32:51.215966+00:00`

## Summary

- Overall health: **99.00%**
- Files: **9528**
- Directories: **2516**
- Errors: **0**
- Warnings: **0**
- Policy findings: **8**

## Health Dimensions

| Dimension | Score |
|---|---:|
| Organization | 100.00% |
| Policy | 96.00% |
| Naming | 100.00% |
| Drift | 100.00% |
| Hygiene | 100.00% |

## Repository Drift

- Baseline snapshot: **False**
- Files added: **1**
- Files removed: **0**
- Directories added: **2**
- Directories removed: **0**

## Findings

### POLICY — `__init__.py`

- Category: `classification`
- Finding: Protected artifact requires an explicit architecture decision: root-package-marker-review.
- Recommendation: Keep in place until imports and entry-point ownership are verified.

### POLICY — `card_hawk_console.py`

- Category: `classification`
- Finding: Protected artifact requires an explicit architecture decision: application-console-entrypoint.
- Recommendation: Keep in place until imports and entry-point ownership are verified.

### POLICY — `history.py`

- Category: `classification`
- Finding: Protected artifact requires an explicit architecture decision: repository-history-utility.
- Recommendation: Keep in place until imports and entry-point ownership are verified.

### POLICY — `event_bus ↔ eventbus`

- Category: `boundary`
- Finding: Parallel namespaces may represent duplicate ownership or historical lineage.
- Recommendation: Create an ADR identifying the canonical namespace and compatibility boundary.

### POLICY — `backup ↔ backups`

- Category: `boundary`
- Finding: Parallel namespaces may represent duplicate ownership or historical lineage.
- Recommendation: Create an ADR identifying the canonical namespace and compatibility boundary.

### POLICY — `card_hawk ↔ cardhawk`

- Category: `boundary`
- Finding: Parallel namespaces may represent duplicate ownership or historical lineage.
- Recommendation: Create an ADR identifying the canonical namespace and compatibility boundary.

### POLICY — `workflow ↔ workflows`

- Category: `boundary`
- Finding: Parallel namespaces may represent duplicate ownership or historical lineage.
- Recommendation: Create an ADR identifying the canonical namespace and compatibility boundary.

### POLICY — `engine ↔ engines`

- Category: `boundary`
- Finding: Parallel namespaces may represent duplicate ownership or historical lineage.
- Recommendation: Create an ADR identifying the canonical namespace and compatibility boundary.

### INFO — `architecture`

- Category: `boundary`
- Finding: High-authority root namespace exists outside the canonical aletheus package.
- Recommendation: Verify whether it is canonical, compatibility, application-specific, or legacy.

### INFO — `core`

- Category: `boundary`
- Finding: High-authority root namespace exists outside the canonical aletheus package.
- Recommendation: Verify whether it is canonical, compatibility, application-specific, or legacy.

### INFO — `engine`

- Category: `boundary`
- Finding: High-authority root namespace exists outside the canonical aletheus package.
- Recommendation: Verify whether it is canonical, compatibility, application-specific, or legacy.

### INFO — `engines`

- Category: `boundary`
- Finding: High-authority root namespace exists outside the canonical aletheus package.
- Recommendation: Verify whether it is canonical, compatibility, application-specific, or legacy.

### INFO — `kernel`

- Category: `boundary`
- Finding: High-authority root namespace exists outside the canonical aletheus package.
- Recommendation: Verify whether it is canonical, compatibility, application-specific, or legacy.

### INFO — `repository`

- Category: `boundary`
- Finding: High-authority root namespace exists outside the canonical aletheus package.
- Recommendation: Verify whether it is canonical, compatibility, application-specific, or legacy.

### INFO — `runtime`

- Category: `boundary`
- Finding: High-authority root namespace exists outside the canonical aletheus package.
- Recommendation: Verify whether it is canonical, compatibility, application-specific, or legacy.

### INFO — `tools/release`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `workspace`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `runtime/cache`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `tests/platform_intelligence/constitutional_runtime_observatory`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `.runtime/certificates`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `docs/decisions`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `docs/implementation`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `docs/governance`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `exports/csv`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `exports/reports`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `Genesis10_Work_Organization/01_repository_intelligence/docs`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `nimble/visualization`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `nimble/reference-shell/tests`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `watch_tower/reports`

- Category: `hygiene`
- Finding: Empty directory detected.
- Recommendation: Remove it if it is not an intentional namespace placeholder.

### INFO — `repository-root`

- Category: `drift`
- Finding: New root entries detected: archives
- Recommendation: Review whether each new root entry is constitutionally permitted.
