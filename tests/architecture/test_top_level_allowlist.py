import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_TOP_LEVEL = {
    "aletheus",
    "apps",
    "database",
    "docs",
    "nimble",
    "scripts",
    "tests",
    "tools",
}
IGNORED = {".github", "history", "reports"}


def test_top_level_allowlist_warning_mode():
    extras = sorted(
        p.name
        for p in ROOT.iterdir()
        if p.is_dir()
        and not p.name.startswith(".")
        and p.name not in ALLOWED_TOP_LEVEL
        and p.name not in IGNORED
    )
    if extras:
        warnings.warn(
            "Transition architecture warning: non-canonical top-level directories remain: "
            + ", ".join(extras),
            stacklevel=2,
        )
