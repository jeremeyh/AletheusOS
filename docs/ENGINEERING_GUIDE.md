# AletheusOS Engineering Guide

## Release Checklist

1. Compile runtime.
2. Run project hygiene.
3. Run regression suite.
4. Run Runtime Doctor.
5. Run Runtime Invariants.
6. Run Runtime Boot Validator.
7. Generate runtime documentation.
8. Update release notes.
9. Commit.
10. Tag.

## Validation Commands

PYTHONPATH=. python -m py_compile aletheus/runtime/core.py
PYTHONPATH=. python tools/maintenance/check_project_hygiene.py
PYTHONPATH=. python tests/regression_runner.py
PYTHONPATH=. python tests/test_aletheus_v411_foundation.py
PYTHONPATH=. python tests/test_aletheus_v421_runtime_integrity.py

## Repository Rules

- No patch scripts belong in the repository root.
- No verification scripts belong in the repository root.
- Runtime reports are generated artifacts.
- Every public command requires regression coverage.
- Compatibility aliases are public API.
- Runtime invariants must pass before release.
