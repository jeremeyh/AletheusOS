# AletheusOS Genesis 10 Update Package

Copy `apply_genesis10_updates.py` into the root of your AletheusOS repository.

```bash
python apply_genesis10_updates.py --dry-run
python apply_genesis10_updates.py
python apply_genesis10_updates.py --verify
python tools/doctor/doctor.py
pytest tests/architecture
git status
```

The updater is idempotent and intentionally does not rewrite `aletheus/runtime/core.py`.
Runtime decomposition must be based on the actual current implementation and validated by tests.
