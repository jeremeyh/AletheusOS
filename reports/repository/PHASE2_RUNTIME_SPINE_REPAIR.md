# Phase 2 Runtime Spine Repair

Date: 2026-07-19

## Scope

This phase implements the first task from the Architecture Repair Blueprint without changing domain behavior:

- Created a source-only working copy.
- Removed generated environments, caches, VCS metadata, and local restore points from production source.
- Preserved restore points and source backup snapshots outside the source tree.
- Made `aletheus/runtime/context.py` the sole `RuntimeContext` definition.
- Reduced `aletheus/runtime/core.py` to one `runtime_core` construction.
- Added `aletheus/version.py` as the canonical version source.
- Changed setuptools metadata to derive its version from `aletheus.version.__version__`.
- Added runtime singleton, version consistency, top-level allowlist, and generated-artifact architecture tests.
- Added the canonical product identity map.

## Deliberately deferred

- Domain manifest extraction.
- CardHawk package consolidation.
- Streamlit application relocation.
- Experience Gateway dependency and smoke-test repair.
- Strict top-level allowlist enforcement.

The allowlist remains warning-only because the repository still has transitional top-level packages.

## Validation results

- `python3 -m compileall -q aletheus`: PASS
- Architecture repair tests: **7 passed**
- `tests/test_aletheus_runtime_a3.py`: PASS
- `tests/test_aletheus_v421_runtime_integrity.py`: PASS
- `tests/regression_runner.py`: **4/4 passed; Runtime Healthy**
- Canonical runtime command surface remained operational.

## Current transition warning

The top-level allowlist test intentionally reports remaining non-canonical directories without failing CI. Consolidating those directories belongs to later phases and must be performed with compatibility shims and import validation.
