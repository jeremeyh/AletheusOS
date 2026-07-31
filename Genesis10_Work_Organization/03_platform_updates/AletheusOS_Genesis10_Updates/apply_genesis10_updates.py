#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path.cwd().resolve()

CANONICAL_DIRS = [
    "docs/architecture",
    "docs/constitution",
    "docs/governance",
    "docs/implementation",
    "docs/decisions",
    "reports/generated",
    "tools/doctor",
    "tools/migration",
    "tools/build",
    "tools/repair",
    "tools/audit",
    "tools/release",
    "tools/repository",
    "scripts",
    ".github/workflows",
    ".github/ISSUE_TEMPLATE",
    "tests/architecture",
]

FILE_MOVES = {
    "reports/runtime_core_decomposition_baseline.md": "docs/architecture/runtime_core_decomposition_baseline.md",
    "reports/runtime_v5_command_inventory.txt": "docs/architecture/runtime_v5_command_inventory.txt",
    "reports/release_cleanup_report.md": "docs/architecture/release_cleanup_report.md",
    "reports/architecture/crk_constitutional_ownership_map.md": "docs/architecture/crk_constitutional_ownership_map.md",
    "reports/architecture/crk_constitutional_ownership_map.json": "docs/architecture/crk_constitutional_ownership_map.json",
}

DIRECTORY_MOVES = {
    "reports/guardian": "reports/generated/guardian",
    "reports/sentinel": "reports/generated/sentinel",
    "reports/council": "reports/generated/council",
    "reports/conclave": "reports/generated/conclave",
    "reports/atlas": "reports/generated/atlas",
    "reports/lighthouse": "reports/generated/lighthouse",
    "reports/platform": "reports/generated/platform",
    "reports/platform_census": "reports/generated/platform_census",
    "reports/platform_inspection": "reports/generated/platform_inspection",
    "reports/spectrum": "reports/generated/spectrum",
    "reports/nimble": "reports/generated/nimble",
    "reports/release_certification": "reports/generated/release_certification",
    "reports/watch_tower": "reports/generated/watch_tower",
    "reports/repository_hygiene": "reports/generated/repository_hygiene",
    "reports/genesis_7_architecture_audit": "docs/architecture/genesis7/architecture_audit",
    "reports/genesis_7_structural_repair": "docs/architecture/genesis7/structural_repair",
    "reports/genesis_8_command_dispatch": "docs/architecture/genesis8/command_dispatch",
}

GITIGNORE_RULES = (
    """
# AletheusOS generated state and reports
runtime_state/
.aletheus_restore_points/
reports/generated/
nimble/reports/ux/playwright/

# Python generated artifacts
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
*.egg-info/

# Local environments and secrets
.venv/
venv/
env/
.env
.env.*
!.env.example

# Build/package output
build/
dist/
*.whl

# OS/editor state
.DS_Store
.idea/
.vscode/
""".strip()
    + "\n"
)

DOCS = {
    "docs/REPOSITORY_CONSTITUTION.md": """# AletheusOS Repository Constitution

## Canonical identity
- **AletheusOS** is the platform.
- **Card Hawk** is the flagship product and reference application.
- **Nimble** is the universal experience runtime and frontend layer.
- **Genesis** names historical development eras and migrations.

## Constitutional rules
1. AletheusOS has one canonical runtime identity.
2. Version information has one authoritative source.
3. `aletheus/runtime/core.py` is a composition root, not an implementation warehouse.
4. Generated output belongs under `reports/generated/`.
5. Long-lived architectural knowledge belongs under `docs/`.
6. New capabilities require explicit ownership, boundaries, tests, and registration paths.
7. Architectural changes must preserve provenance through Git.

## Directory ownership
- `aletheus/`: platform and product source.
- `nimble/`: experience runtime and UI source.
- `tests/`: all test suites and architecture guardrails.
- `docs/`: canonical documentation.
- `reports/generated/`: reproducible diagnostics and generated reports.
- `tools/`: reusable development tooling.
- `scripts/`: thin executable entry points.

## Runtime policy
The runtime core remains small, stable, and focused on construction, wiring, startup,
shutdown, and delegation. Sophistication belongs in bounded components.
""",
    "docs/DIRECTORY_STRUCTURE.md": """# Directory Structure

```text
AletheusOS/
├── aletheus/
├── nimble/
├── tests/
├── docs/
├── reports/
│   └── generated/
├── tools/
├── scripts/
├── pyproject.toml
├── README.md
└── LICENSE
```

Source packages named `reports` inside application modules are valid code. For example,
`aletheus/card_hawk/reports/` must remain tracked.
""",
    "docs/DEVELOPMENT_GUIDE.md": """# Development Guide

```bash
./scripts/bootstrap.sh
python tools/doctor/doctor.py
pytest tests/architecture
```

Keep changes bounded and independently testable. Generated diagnostics belong under
`reports/generated/`; enduring findings belong under `docs/`.
""",
    "docs/RELEASE_PROCESS.md": """# Release Process

1. Confirm a clean Git working tree.
2. Run the repository doctor.
3. Run architecture, regression, and runtime integrity tests.
4. Verify canonical version consistency.
5. Generate release certification.
6. Review migration and architecture manifests.
7. Tag only after validation passes.
""",
    "docs/CONTRIBUTING.md": """# Contributing

Before submitting changes:

```bash
python tools/doctor/doctor.py
pytest tests/architecture
```

Do not commit caches, local runtime snapshots, restore points, or generated reports.
""",
    "docs/ARCHITECTURE_OVERVIEW.md": """# Architecture Overview

AletheusOS is a constitutional intelligence platform. Card Hawk is its flagship proof
application. Nimble provides the universal experience layer.

The runtime is compositional: `core.py` constructs and delegates, while bounded managers
and services own implementation responsibilities.
""",
}

DOCTOR = """#!/usr/bin/env python3
from __future__ import annotations
import ast, os, subprocess, sys
from dataclasses import dataclass
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
@dataclass
class Check:
    name: str
    ok: bool
    detail: str

def run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return p.returncode, (p.stdout + p.stderr).strip()

def checks() -> list[Check]:
    out: list[Check] = []
    out.append(Check("Python", sys.version_info >= (3, 11), sys.version.split()[0]))
    active = sys.prefix != getattr(sys, "base_prefix", sys.prefix) or bool(os.getenv("VIRTUAL_ENV"))
    out.append(Check("Virtual environment", active, os.getenv("VIRTUAL_ENV", "not detected")))
    version = ROOT / "aletheus/version.py"
    out.append(Check("Canonical version", version.exists(), str(version.relative_to(ROOT)) if version.exists() else "missing"))
    core = ROOT / "aletheus/runtime/core.py"
    count = core.read_text(encoding="utf-8", errors="replace").count("runtime_core = AletheusRuntime(") if core.exists() else 0
    out.append(Check("Runtime singleton", count == 1, f"definitions={count}"))
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8", errors="replace") if (ROOT / ".gitignore").exists() else ""
    required = ["runtime_state/", ".aletheus_restore_points/", "reports/generated/"]
    missing = [x for x in required if x not in gi]
    out.append(Check("Generated artifact policy", not missing, "present" if not missing else f"missing={missing}"))
    code, detail = run([sys.executable, "-m", "compileall", "-q", "aletheus"])
    out.append(Check("Python compile", code == 0, detail[-250:] or "passed"))
    code, detail = run(["git", "status", "--porcelain"])
    out.append(Check("Git status", code == 0, "clean" if code == 0 and not detail else "working tree has changes"))
    return out

def main() -> int:
    results = checks()
    print("=" * 68)
    print("AletheusOS Repository Doctor")
    print("=" * 68)
    for c in results:
        print(f"[{'PASS' if c.ok else 'FAIL':4}] {c.name:<28} {c.detail}")
    passed = sum(c.ok for c in results)
    print("-" * 68)
    print(f"Health: {passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1
if __name__ == "__main__":
    raise SystemExit(main())
"""

BOOTSTRAP = """#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if [[ ! -d ".venv" ]]; then "$PYTHON_BIN" -m venv .venv; fi
source .venv/bin/activate
python -m pip install --upgrade pip
if [[ -f "pyproject.toml" ]]; then
  python -m pip install -e ".[dev]" || python -m pip install -e .
fi
python -m compileall -q aletheus
python tools/doctor/doctor.py || true
echo "AletheusOS development environment prepared."
"""

ARCH_TESTS = {
    "tests/architecture/test_repository_policy.py": """from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def test_canonical_directories_exist():
    for rel in ("aletheus", "tests", "docs", "tools", "reports"):
        assert (ROOT / rel).exists(), f"Missing canonical directory: {rel}"
def test_generated_reports_are_ignored():
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "reports/generated/" in text
    assert "runtime_state/" in text
    assert ".aletheus_restore_points/" in text
""",
    "tests/architecture/test_runtime_composition_policy.py": """from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def test_single_runtime_singleton_definition():
    core = ROOT / "aletheus/runtime/core.py"
    text = core.read_text(encoding="utf-8")
    assert text.count("runtime_core = AletheusRuntime(") == 1
""",
}

GITHUB = {
    ".github/workflows/tests.yml": """name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m pip install --upgrade pip
      - run: python -m pip install -e ".[dev]" || python -m pip install -e .
      - run: python -m compileall -q aletheus
      - run: pytest tests/architecture
""",
    ".github/CODEOWNERS": "# Replace with GitHub usernames or teams when collaboration begins.\n* @OWNER\n",
    ".github/pull_request_template.md": """## Summary

## Architectural impact

## Validation
- [ ] Repository doctor
- [ ] Architecture tests
- [ ] Regression tests
- [ ] Generated artifacts excluded
""",
}


@dataclass
class Manifest:
    created: list[dict] = field(default_factory=list)
    moved: list[dict] = field(default_factory=list)
    skipped: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_file(
    path: Path, content: str, dry: bool, m: Manifest, executable: bool = False
) -> None:
    if path.exists() and path.stat().st_size > 0:
        m.skipped.append(
            {"path": str(path.relative_to(ROOT)), "reason": "existing_nonempty"}
        )
        return
    if dry:
        m.created.append({"path": str(path.relative_to(ROOT)), "dry_run": True})
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | 0o111)
    m.created.append({"path": str(path.relative_to(ROOT)), "sha256": sha256(path)})


def merge_gitignore(dry: bool, m: Manifest) -> None:
    p = ROOT / ".gitignore"
    existing = p.read_text(encoding="utf-8") if p.exists() else ""
    needed = [
        line
        for line in GITIGNORE_RULES.splitlines()
        if line and not line.startswith("#") and line not in existing.splitlines()
    ]
    if not needed:
        m.skipped.append({"path": ".gitignore", "reason": "rules_present"})
        return
    if dry:
        m.created.append(
            {"path": ".gitignore", "action": "append_rules", "dry_run": True}
        )
        return
    p.write_text(existing.rstrip() + "\n\n" + GITIGNORE_RULES, encoding="utf-8")
    m.created.append(
        {"path": ".gitignore", "action": "appended_rules", "sha256": sha256(p)}
    )


def merge_directory(src: Path, dst: Path, dry: bool, m: Manifest) -> None:
    if not src.exists() or src.resolve() == dst.resolve():
        return
    if not dst.exists():
        if dry:
            m.moved.append(
                {
                    "source": str(src.relative_to(ROOT)),
                    "destination": str(dst.relative_to(ROOT)),
                    "dry_run": True,
                }
            )
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            m.moved.append(
                {
                    "source": str(src.relative_to(ROOT)),
                    "destination": str(dst.relative_to(ROOT)),
                }
            )
        return
    for item in sorted(src.rglob("*")):
        rel, target = item.relative_to(src), dst / item.relative_to(src)
        if item.is_dir():
            if not dry:
                target.mkdir(parents=True, exist_ok=True)
            continue
        if target.exists():
            m.skipped.append(
                {"path": str(item.relative_to(ROOT)), "reason": "destination_exists"}
            )
        elif dry:
            m.moved.append(
                {
                    "source": str(item.relative_to(ROOT)),
                    "destination": str(target.relative_to(ROOT)),
                    "dry_run": True,
                }
            )
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(target))
            m.moved.append(
                {
                    "source": str(item.relative_to(ROOT)),
                    "destination": str(target.relative_to(ROOT)),
                }
            )
    if not dry:
        shutil.rmtree(src, ignore_errors=True)


def verify() -> int:
    checks = {
        "docs/architecture": (ROOT / "docs/architecture").is_dir(),
        "reports/generated": (ROOT / "reports/generated").is_dir(),
        "repository constitution": (ROOT / "docs/REPOSITORY_CONSTITUTION.md").is_file(),
        "doctor": (ROOT / "tools/doctor/doctor.py").is_file(),
        "bootstrap": (ROOT / "scripts/bootstrap.sh").is_file(),
        "architecture tests": (ROOT / "tests/architecture").is_dir(),
    }
    for name, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    return 0 if all(checks.values()) else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        return verify()
    if not (ROOT / "aletheus").exists():
        print("ERROR: Run from the AletheusOS repository root.", file=sys.stderr)
        return 2
    m = Manifest()
    for rel in CANONICAL_DIRS:
        p = ROOT / rel
        if args.dry_run and not p.exists():
            m.created.append({"path": rel, "kind": "directory", "dry_run": True})
        elif not args.dry_run:
            p.mkdir(parents=True, exist_ok=True)
    merge_directory(
        ROOT / "docs/ARCHITECTURE", ROOT / "docs/architecture", args.dry_run, m
    )
    for src_rel, dst_rel in FILE_MOVES.items():
        src, dst = ROOT / src_rel, ROOT / dst_rel
        if not src.exists():
            continue
        if dst.exists():
            m.skipped.append({"path": src_rel, "reason": "destination_exists"})
            continue
        if args.dry_run:
            m.moved.append({"source": src_rel, "destination": dst_rel, "dry_run": True})
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            m.moved.append({"source": src_rel, "destination": dst_rel})
    for src_rel, dst_rel in DIRECTORY_MOVES.items():
        merge_directory(ROOT / src_rel, ROOT / dst_rel, args.dry_run, m)
    merge_gitignore(args.dry_run, m)
    for rel, content in DOCS.items():
        write_file(ROOT / rel, content, args.dry_run, m)
    write_file(ROOT / "tools/doctor/doctor.py", DOCTOR, args.dry_run, m, True)
    write_file(ROOT / "scripts/bootstrap.sh", BOOTSTRAP, args.dry_run, m, True)
    for rel, content in ARCH_TESTS.items():
        write_file(ROOT / rel, content, args.dry_run, m)
    for rel, content in GITHUB.items():
        write_file(ROOT / rel, content, args.dry_run, m)
    if not args.dry_run:
        out = ROOT / "reports/generated/repository_updates_manifest.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps(
                {
                    "generated": datetime.now(UTC).isoformat(),
                    "created": m.created,
                    "moved": m.moved,
                    "skipped": m.skipped,
                    "warnings": m.warnings,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    print("=" * 72)
    print("AletheusOS Genesis 10 Repository Updates")
    print("=" * 72)
    print(f"Created/updated: {len(m.created)}")
    print(f"Moved:           {len(m.moved)}")
    print(f"Skipped:         {len(m.skipped)}")
    print("Dry run only." if args.dry_run else "Updates applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
