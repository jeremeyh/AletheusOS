# Verify GP-00036

Copy files from `merge/` into the repository root.

Then run:

```bash
python -m pytest tests/test_repository_dna_atlas_integration.py
```

Manual smoke test:

```bash
python - <<'PY'
from pathlib import Path
from aletheus.atlas.repository_dna_service import RepositoryAwareAtlasService

svc = RepositoryAwareAtlasService()
report = svc.discover_from_repository_dna(Path("aletheus"))
print(report.snapshot.subsystem_count)
print(report.snapshot.family_count)
PY
```
