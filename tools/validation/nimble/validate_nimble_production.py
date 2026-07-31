from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)

NIMBLE_ROOT = ROOT / "nimble"
SHELL_ROOT = NIMBLE_ROOT / "apps" / "platform-shell"
DIST_ROOT = SHELL_ROOT / "dist"
ASSET_ROOT = DIST_ROOT / "assets"

PRIMARY_BUNDLE_LIMIT_BYTES = 500_000


@dataclass(frozen=True)
class Check:
    name: str
    command: tuple[str, ...]
    working_directory: Path


@dataclass(frozen=True)
class CheckResult:
    name: str
    command: tuple[str, ...]
    return_code: int
    elapsed_seconds: float


def run_check(
    check: Check,
    environment: dict[str, str],
) -> CheckResult:
    print()
    print("=" * 72)
    print(check.name.upper())
    print("=" * 72)
    print(
        "Command:",
        " ".join(check.command),
    )
    print(
        "Directory:",
        check.working_directory.relative_to(ROOT),
    )

    started = time.perf_counter()

    completed = subprocess.run(
        check.command,
        cwd=check.working_directory,
        env=environment,
        check=False,
    )

    elapsed = time.perf_counter() - started

    status = "PASS" if completed.returncode == 0 else "FAIL"

    print(f"{status}: {check.name} ({elapsed:.2f}s)")

    return CheckResult(
        name=check.name,
        command=check.command,
        return_code=completed.returncode,
        elapsed_seconds=elapsed,
    )


def require_path(
    path: Path,
    label: str,
) -> None:
    if not path.exists():
        raise RuntimeError(f"Missing {label}: {path.relative_to(ROOT)}")


def locate_primary_bundle() -> Path:
    candidates = sorted(
        ASSET_ROOT.glob("index-*.js"),
        key=lambda path: path.stat().st_size,
        reverse=True,
    )

    if not candidates:
        raise RuntimeError("No primary Nimble JavaScript bundle found.")

    return candidates[0]


def validate_bundle_budget() -> None:
    primary = locate_primary_bundle()
    size = primary.stat().st_size

    print()
    print("=" * 72)
    print("NIMBLE BUNDLE BUDGET")
    print("=" * 72)
    print(
        "Primary:",
        primary.relative_to(ROOT),
    )
    print(
        "Size:",
        f"{size:,} bytes",
    )
    print(
        "Limit:",
        f"{PRIMARY_BUNDLE_LIMIT_BYTES:,} bytes",
    )

    if size > PRIMARY_BUNDLE_LIMIT_BYTES:
        raise RuntimeError(
            "Primary Nimble bundle exceeded the "
            f"{PRIMARY_BUNDLE_LIMIT_BYTES:,}-byte budget."
        )

    secondary = [path for path in ASSET_ROOT.glob("*.js") if path != primary]

    print(
        "Secondary chunks:",
        len(secondary),
    )
    print("Status: PASS")


def build_environment() -> dict[str, str]:
    environment = dict(os.environ)

    environment.setdefault(
        "NODE_OPTIONS",
        "--use-system-ca",
    )

    environment.setdefault(
        "CI",
        "1",
    )

    return environment


def main() -> int:
    require_path(
        NIMBLE_ROOT / "package.json",
        "Nimble workspace package manifest",
    )

    require_path(
        SHELL_ROOT / "package.json",
        "Nimble shell package manifest",
    )

    require_path(
        ROOT / "validate_nimble_foundation.py",
        "foundation validator",
    )

    require_path(
        ROOT / "validate_nimble_tokens.py",
        "token validator",
    )

    require_path(
        ROOT / "validate_nimble_components.py",
        "component validator",
    )

    require_path(
        ROOT / "validate_nimble_reference_shell.py",
        "reference-shell validator",
    )

    require_path(
        ROOT / "validate_nimble_bundle_boundary.py",
        "bundle-boundary validator",
    )

    require_path(
        ROOT / "validate_nimble_route_splitting.py",
        "route-splitting validator",
    )

    require_path(
        ROOT / "validate_nimble_ci.py",
        "CI validator",
    )

    npm = shutil.which("npm")

    if npm is None:
        print("FAIL: npm is not available on PATH.")
        return 1

    python = sys.executable

    environment = build_environment()

    checks: Sequence[Check] = (
        Check(
            name="Frontend typecheck",
            command=(
                npm,
                "run",
                "typecheck",
            ),
            working_directory=NIMBLE_ROOT,
        ),
        Check(
            name="Frontend tests",
            command=(
                npm,
                "run",
                "test",
                "--",
                "--run",
            ),
            working_directory=NIMBLE_ROOT,
        ),
        Check(
            name="Frontend production build",
            command=(
                npm,
                "run",
                "build",
            ),
            working_directory=NIMBLE_ROOT,
        ),
        Check(
            name="Nimble foundation",
            command=(
                python,
                "validate_nimble_foundation.py",
            ),
            working_directory=ROOT,
        ),
        Check(
            name="Nimble tokens",
            command=(
                python,
                "validate_nimble_tokens.py",
            ),
            working_directory=ROOT,
        ),
        Check(
            name="Nimble components",
            command=(
                python,
                "validate_nimble_components.py",
            ),
            working_directory=ROOT,
        ),
        Check(
            name="Nimble reference shell",
            command=(
                python,
                "validate_nimble_reference_shell.py",
            ),
            working_directory=ROOT,
        ),
        Check(
            name="Nimble bundle boundary",
            command=(
                python,
                "validate_nimble_bundle_boundary.py",
            ),
            working_directory=ROOT,
        ),
        Check(
            name="Nimble route splitting",
            command=(
                python,
                "validate_nimble_route_splitting.py",
            ),
            working_directory=ROOT,
        ),
        Check(
            name="Nimble CI contract",
            command=(
                python,
                "validate_nimble_ci.py",
            ),
            working_directory=ROOT,
        ),
    )

    results: list[CheckResult] = []

    for check in checks:
        result = run_check(
            check,
            environment,
        )

        results.append(result)

        if result.return_code != 0:
            print()
            print("=" * 72)
            print("NIMBLE PRODUCTION GATE")
            print("=" * 72)
            print("Status: FAIL")
            print(
                "Failed check:",
                result.name,
            )
            return result.return_code

    try:
        validate_bundle_budget()
    except RuntimeError as error:
        print()
        print(
            "FAIL:",
            error,
        )
        return 1

    total_seconds = sum(result.elapsed_seconds for result in results)

    print()
    print("=" * 72)
    print("NIMBLE™ PRODUCTION GATE")
    print("=" * 72)
    print(
        "Checks completed:",
        len(results) + 1,
    )
    print("Frontend type safety: PASS")
    print("Frontend tests: PASS")
    print("Production build: PASS")
    print("Architecture contracts: PASS")
    print("Reference implementation: PASS")
    print("OIDC bundle isolation: PASS")
    print("Route splitting: PASS")
    print("Primary bundle budget: PASS")
    print(
        "Elapsed:",
        f"{total_seconds:.2f}s",
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
