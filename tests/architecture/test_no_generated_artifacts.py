from pathlib import Path
import warnings

ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_DIR_NAMES = {"node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}


def test_generated_artifacts_warning_mode():
    found = []
    for path in ROOT.rglob("*"):
        if path.is_dir() and path.name in FORBIDDEN_DIR_NAMES:
            found.append(str(path.relative_to(ROOT)))
    if found:
        warnings.warn("Generated artifacts remain: " + ", ".join(found[:30]), stacklevel=2)
