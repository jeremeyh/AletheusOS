# AletheusOS Reconstructed Authority Receipt — PROJECT_LOCAL_TOOLCHAIN

## Receipt classification

- Receipt type: RECONSTRUCTED_AUTHORITY_RECEIPT
- Authority origin: PRIOR_EXPLICIT_USER_ADJUDICATION
- Original source specification recovered: NO
- Canonical promotion performed by this receipt: NO
- Repository mutation performed: NO

## Adjudicated authority preserved

AletheusOS Genesis release verification must use the project-local toolchain
rather than relying on globally installed binaries or the user's PATH.

TypeScript verification must resolve the compiler from the project's
`node_modules` or equivalent project-local toolchain location instead of
invoking an uncontrolled global `tsc`.

Genesis release packaging should pin compatible toolchain versions so release
verification is reproducible and does not silently depend on workstation-
global compiler state.

## Provenance statement

Passes 2G–2I searched the repository, Desktop artifacts, ZIP contents, and
reachable Git history.

Pass 2I found multiple primary implementation-evidence scripts that exercise
the project-local toolchain rule, but no surviving non-circular authority-spec
document suitable for designation as the original source.

This receipt preserves the prior explicit adjudication while retaining those
scripts only as implementation evidence.

## Build posture

This receipt does not authorize source modification, release execution,
canonical promotion, merge, GitHub push, F4E implementation, or cleanup.
