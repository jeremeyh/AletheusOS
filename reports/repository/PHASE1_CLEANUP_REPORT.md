# AletheusOS Repository Cleanup — Phase 1

Date: 2026-07-19

## Actions completed

- Preserved the original uploaded archive unchanged.
- Created a working cleanup copy.
- Archived 532 completed Genesis/post-Genesis/Xogenesis shell scripts under `history/genesis/scripts/`.
- Added `history/genesis/README.md` with historical execution guidance.
- Removed local/generated debris including `.venv`, Python bytecode caches, pytest caches, macOS metadata, and generated egg-info.
- Archived root backup files and malformed stray artifacts rather than deleting source history.
- Expanded `.gitignore` for local environments, caches, runtime snapshots, restore points, and generated package metadata.
- Added `tools/repository/doctor.py` for repeatable repository hygiene diagnostics.
- Added `tools/aletheus` with initial `doctor`, `compile`, and `test` commands.
- Generated a machine-readable cleanup manifest at `reports/repository/phase1_cleanup_manifest.json`.

## Measured improvement

| Metric | Before | After |
|---|---:|---:|
| Repository size | 559 MB | 179 MB |
| Root entries | 860 | 321 |
| Root shell scripts | 554 | 21 |
| Archived Genesis scripts | 0 | 532 |

## Verification

- `python -m compileall -q aletheus`: **PASS**
- Pytest discovery: **556 tests discovered**
- Pytest collection: **FAIL — 36 pre-existing import errors**

The collection failures are recorded in `reports/repository/pytest_collection.txt` and were not caused by moving the historical shell scripts. The principal failure families are:

1. Missing or incomplete exports from `aletheus.civilization`.
2. Missing or incomplete exports from `aletheus.institutional_civilization`.
3. Missing `aletheus.runtime.modules` package/module.
4. Platform Intelligence imports that no longer match the current package surface.
5. Application, mission, constitutional-ledger, and platform-surface tests importing obsolete or absent symbols.

## Intentionally deferred

The 134 root-level Python utilities were not moved automatically. They require dependency and invocation analysis before consolidation because some may still be active repair, validation, release, or build entry points.

## Next repair tranche

1. Produce an import-error matrix mapping every failed test to the missing symbol/module and its likely canonical replacement.
2. Repair package exports and compatibility shims without introducing architectural drift.
3. Restore clean pytest collection.
4. Consolidate root Python utilities into `tools/{build,validate,repair,audit,release,diagnostics}`.
5. Extend `tools/aletheus` into the unified platform CLI.
