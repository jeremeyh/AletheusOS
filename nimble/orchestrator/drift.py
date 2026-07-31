from __future__ import annotations

from pathlib import Path

from .manifest import CAPABILITIES


def detect_drift(
    root: Path,
) -> tuple[str, ...]:
    failures: list[str] = []

    canonical_terms = {
        "Aletheum™": "Retired runtime name detected.",
        "Council Consensus": "Council consensus should not replace individual engine instrumentation.",
    }

    scan_roots = [
        root / "nimble",
        root / "aletheus",
    ]

    for scan_root in scan_roots:
        if not scan_root.exists():
            continue

        for path in scan_root.rglob("*"):
            if not path.is_file() or path.suffix not in {
                ".py",
                ".ts",
                ".tsx",
                ".md",
                ".json",
            }:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for term, message in canonical_terms.items():
                if term in text:
                    failures.append(f"{message} File: {path.relative_to(root)}")

    capability_ids = {item.capability_id for item in CAPABILITIES}

    if len(capability_ids) != len(CAPABILITIES):
        failures.append("Duplicate capability id in orchestrator manifest.")

    return tuple(failures)
