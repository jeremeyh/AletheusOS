#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "nimble/orchestrator"
TEST = ROOT / "tests/nimble/test_nimble_orchestrator.py"
VALIDATOR = ROOT / "validate_nimble_orchestrator.py"


FILES: dict[str, str] = {
    "__init__.py": '''"""Nimble Build Orchestrator™."""

from .discovery import discover_capabilities
from .planner import create_build_plan
from .readiness import analyze_readiness

__all__ = [
    "analyze_readiness",
    "create_build_plan",
    "discover_capabilities",
]
''',

    "models.py": '''from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


CapabilityState = Literal[
    "implemented",
    "partial",
    "planned",
    "blocked",
    "missing",
]


@dataclass(frozen=True)
class CapabilityDefinition:
    capability_id: str
    display_name: str
    required_paths: tuple[str, ...]
    dependencies: tuple[str, ...] = ()
    constitutional: bool = False


@dataclass(frozen=True)
class CapabilityStatus:
    capability_id: str
    display_name: str
    state: CapabilityState
    readiness_percent: int
    existing_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]
    dependencies: tuple[str, ...]
    blocked_by: tuple[str, ...]
    constitutional: bool


@dataclass(frozen=True)
class BuildPlanItem:
    order: int
    capability_id: str
    display_name: str
    state: CapabilityState
    action: str
    reason: str
''',

    "manifest.py": '''from __future__ import annotations

from .models import CapabilityDefinition


CAPABILITIES: tuple[CapabilityDefinition, ...] = (
    CapabilityDefinition(
        capability_id="experience-constitution",
        display_name="Experience Constitution™",
        required_paths=(
            "aletheus/constitution/ARCHITECTURAL_CONSTITUTION.md",
            "aletheus/constitution/EXPERIENCE_EVOLUTION.md",
            "aletheus/constitution/FOUNDERS_VISION.md",
        ),
        constitutional=True,
    ),
    CapabilityDefinition(
        capability_id="experience-core",
        display_name="Experience Core™",
        required_paths=(
            "nimble/packages/core/src/experience/contracts.ts",
            "nimble/packages/core/src/experience/index.ts",
            "nimble/packages/core/src/experience/tokens/index.ts",
            "nimble/packages/core/src/experience/theme/index.ts",
            "validate_nimble_experience_core.py",
            "tests/nimble/test_experience_core.py",
        ),
        dependencies=("experience-constitution",),
        constitutional=True,
    ),
    CapabilityDefinition(
        capability_id="react-primitives",
        display_name="Primitive Experience Library™",
        required_paths=(
            "nimble/packages/react/src/primitives/Surface.tsx",
            "nimble/packages/react/src/primitives/Stack.tsx",
            "nimble/packages/react/src/primitives/Grid.tsx",
            "nimble/packages/react/src/primitives/Text.tsx",
            "nimble/packages/react/src/primitives/Instrument.tsx",
            "nimble/packages/react/src/primitives/reserved.tsx",
            "validate_nimble_primitive_experience.py",
            "tests/nimble/test_primitive_experience.py",
        ),
        dependencies=("experience-core",),
    ),
    CapabilityDefinition(
        capability_id="workspace-engine",
        display_name="Workspace Engine™",
        required_paths=(
            "nimble/packages/workspace/src/engine/contracts.ts",
            "nimble/packages/workspace/src/engine/founder.ts",
            "nimble/packages/workspace/src/engine/layout.ts",
            "nimble/packages/workspace/src/engine/registry.ts",
            "nimble/packages/workspace/src/engine/persistence.ts",
            "validate_nimble_workspace_engine.py",
            "tests/nimble/test_workspace_engine.py",
        ),
        dependencies=("experience-core",),
    ),
    CapabilityDefinition(
        capability_id="instrumentation-preview",
        display_name="Intelligence Instrumentation™ Preview",
        required_paths=(
            "nimble/apps/platform-shell/instrumentation.html",
            "nimble/apps/platform-shell/src/instrumentation-preview.tsx",
            "nimble/apps/platform-shell/src/nimble/showcase/IntelligenceInstrumentationShowcase.tsx",
            "validate_nimble_instrumentation_preview.py",
            "tests/nimble/test_instrumentation_preview.py",
        ),
        dependencies=("react-primitives",),
    ),
    CapabilityDefinition(
        capability_id="founder-console",
        display_name="Founder Console™",
        required_paths=(
            "nimble/apps/platform-shell/founder-console.html",
            "nimble/apps/platform-shell/src/founder-console.tsx",
            "nimble/apps/platform-shell/src/nimble/founder-console/FounderConsoleShell.tsx",
            "validate_nimble_founder_console_shell.py",
            "tests/nimble/test_founder_console_shell.py",
        ),
        dependencies=(
            "react-primitives",
            "workspace-engine",
        ),
    ),
)
''',

    "discovery.py": '''from __future__ import annotations

from pathlib import Path

from .manifest import CAPABILITIES
from .models import CapabilityStatus


def discover_capabilities(
    root: Path,
) -> tuple[CapabilityStatus, ...]:
    provisional: dict[str, CapabilityStatus] = {}

    for definition in CAPABILITIES:
        existing = tuple(
            path
            for path in definition.required_paths
            if (root / path).exists()
        )

        missing = tuple(
            path
            for path in definition.required_paths
            if not (root / path).exists()
        )

        required_count = len(
            definition.required_paths
        )

        readiness = (
            round(
                len(existing)
                / required_count
                * 100
            )
            if required_count
            else 100
        )

        if readiness == 100:
            state = "implemented"
        elif readiness == 0:
            state = "missing"
        else:
            state = "partial"

        provisional[
            definition.capability_id
        ] = CapabilityStatus(
            capability_id=definition.capability_id,
            display_name=definition.display_name,
            state=state,
            readiness_percent=readiness,
            existing_paths=existing,
            missing_paths=missing,
            dependencies=definition.dependencies,
            blocked_by=(),
            constitutional=definition.constitutional,
        )

    resolved: list[CapabilityStatus] = []

    for definition in CAPABILITIES:
        status = provisional[
            definition.capability_id
        ]

        blocked_by = tuple(
            dependency
            for dependency in definition.dependencies
            if provisional[
                dependency
            ].state != "implemented"
        )

        state = status.state

        if (
            state != "implemented"
            and blocked_by
        ):
            state = "blocked"

        resolved.append(
            CapabilityStatus(
                capability_id=status.capability_id,
                display_name=status.display_name,
                state=state,
                readiness_percent=status.readiness_percent,
                existing_paths=status.existing_paths,
                missing_paths=status.missing_paths,
                dependencies=status.dependencies,
                blocked_by=blocked_by,
                constitutional=status.constitutional,
            )
        )

    return tuple(resolved)
''',

    "readiness.py": '''from __future__ import annotations

from pathlib import Path

from .discovery import discover_capabilities
from .models import CapabilityStatus


def analyze_readiness(
    root: Path,
) -> dict[str, object]:
    capabilities = discover_capabilities(
        root
    )

    implemented = sum(
        item.state == "implemented"
        for item in capabilities
    )

    partial = sum(
        item.state == "partial"
        for item in capabilities
    )

    blocked = sum(
        item.state == "blocked"
        for item in capabilities
    )

    missing = sum(
        item.state == "missing"
        for item in capabilities
    )

    overall = round(
        sum(
            item.readiness_percent
            for item in capabilities
        )
        / len(capabilities)
    )

    return {
        "overall_readiness_percent": overall,
        "implemented": implemented,
        "partial": partial,
        "blocked": blocked,
        "missing": missing,
        "capabilities": capabilities,
    }
''',

    "planner.py": '''from __future__ import annotations

from pathlib import Path

from .discovery import discover_capabilities
from .models import BuildPlanItem


def create_build_plan(
    root: Path,
) -> tuple[BuildPlanItem, ...]:
    statuses = discover_capabilities(root)

    order_lookup = {
        status.capability_id: index
        for index, status in enumerate(
            statuses,
            start=1,
        )
    }

    plan: list[BuildPlanItem] = []

    for status in statuses:
        if status.state == "implemented":
            continue

        if status.state == "blocked":
            reason = (
                "Blocked by: "
                + ", ".join(status.blocked_by)
            )
            action = "resolve dependencies"
        elif status.state == "partial":
            reason = (
                f"{len(status.missing_paths)} "
                "required path(s) missing"
            )
            action = "complete capability"
        else:
            reason = "Capability not yet implemented"
            action = "build capability"

        plan.append(
            BuildPlanItem(
                order=order_lookup[
                    status.capability_id
                ],
                capability_id=status.capability_id,
                display_name=status.display_name,
                state=status.state,
                action=action,
                reason=reason,
            )
        )

    return tuple(
        sorted(
            plan,
            key=lambda item: (
                item.state == "blocked",
                item.order,
            ),
        )
    )
''',

    "drift.py": '''from __future__ import annotations

from pathlib import Path

from .manifest import CAPABILITIES


def detect_drift(
    root: Path,
) -> tuple[str, ...]:
    failures: list[str] = []

    canonical_terms = {
        "Aletheum™":
            "Retired runtime name detected.",
        "Council Consensus":
            "Council consensus should not replace individual engine instrumentation.",
    }

    scan_roots = [
        root / "nimble",
        root / "aletheus",
    ]

    for scan_root in scan_roots:
        if not scan_root.exists():
            continue

        for path in scan_root.rglob("*"):
            if (
                not path.is_file()
                or path.suffix
                not in {
                    ".py",
                    ".ts",
                    ".tsx",
                    ".md",
                    ".json",
                }
            ):
                continue

            try:
                text = path.read_text(
                    encoding="utf-8"
                )
            except UnicodeDecodeError:
                continue

            for term, message in (
                canonical_terms.items()
            ):
                if term in text:
                    failures.append(
                        f"{message} "
                        f"File: {path.relative_to(root)}"
                    )

    capability_ids = {
        item.capability_id
        for item in CAPABILITIES
    }

    if len(capability_ids) != len(
        CAPABILITIES
    ):
        failures.append(
            "Duplicate capability id in orchestrator manifest."
        )

    return tuple(failures)
''',

    "report.py": '''from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .drift import detect_drift
from .planner import create_build_plan
from .readiness import analyze_readiness


def generate_report(
    root: Path,
    output: Path,
) -> dict[str, object]:
    readiness = analyze_readiness(root)
    plan = create_build_plan(root)
    drift = detect_drift(root)

    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "overall_readiness_percent":
            readiness[
                "overall_readiness_percent"
            ],
        "summary": {
            "implemented":
                readiness["implemented"],
            "partial":
                readiness["partial"],
            "blocked":
                readiness["blocked"],
            "missing":
                readiness["missing"],
            "drift_findings": len(drift),
        },
        "capabilities": [
            asdict(item)
            for item in readiness[
                "capabilities"
            ]
        ],
        "build_plan": [
            asdict(item)
            for item in plan
        ],
        "drift_findings": list(drift),
    }

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\\n",
        encoding="utf-8",
    )

    return payload
''',

    "cli.py": '''from __future__ import annotations

import argparse
from pathlib import Path

from .report import generate_report


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect AletheusOS build readiness "
            "without mutating source code."
        )
    )

    parser.add_argument(
        "--root",
        default=".",
    )

    parser.add_argument(
        "--report",
        default=(
            "reports/nimble/orchestrator/"
            "build-state-latest.json"
        ),
    )

    arguments = parser.parse_args()

    root = Path(
        arguments.root
    ).resolve()

    report_path = Path(
        arguments.report
    )

    if not report_path.is_absolute():
        report_path = (
            root / report_path
        )

    report = generate_report(
        root,
        report_path,
    )

    print("=" * 72)
    print("NIMBLE™ BUILD ORCHESTRATOR")
    print("=" * 72)
    print(
        "Overall readiness:",
        f"{report['overall_readiness_percent']}%",
    )

    summary = report["summary"]

    print(
        "Implemented:",
        summary["implemented"],
    )
    print(
        "Partial:",
        summary["partial"],
    )
    print(
        "Blocked:",
        summary["blocked"],
    )
    print(
        "Missing:",
        summary["missing"],
    )
    print(
        "Drift findings:",
        summary["drift_findings"],
    )

    print()
    print("Capability state:")

    for capability in report[
        "capabilities"
    ]:
        print(
            f"- {capability['display_name']}: "
            f"{capability['state']} "
            f"({capability['readiness_percent']}%)"
        )

        if capability["blocked_by"]:
            print(
                "  blocked by:",
                ", ".join(
                    capability[
                        "blocked_by"
                    ]
                ),
            )

    print()
    print("Recommended build plan:")

    if not report["build_plan"]:
        print("- No remaining build work.")
    else:
        for item in report[
            "build_plan"
        ]:
            print(
                f"- {item['display_name']}: "
                f"{item['action']} "
                f"({item['reason']})"
            )

    print()
    print(
        "Report:",
        report_path.relative_to(root),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',

    "__main__.py": '''from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
''',
}


def write_new(
    path: Path,
    content: str,
) -> None:
    if path.exists():
        raise RuntimeError(
            "Refusing to overwrite existing file: "
            + str(path.relative_to(ROOT))
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content.rstrip() + "\n",
        encoding="utf-8",
    )


def write_validator() -> None:
    write_new(
        VALIDATOR,
        '''#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REPORT = (
    ROOT
    / "reports/nimble/orchestrator/"
    "build-state-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required = [
        "nimble/orchestrator/__init__.py",
        "nimble/orchestrator/__main__.py",
        "nimble/orchestrator/cli.py",
        "nimble/orchestrator/discovery.py",
        "nimble/orchestrator/drift.py",
        "nimble/orchestrator/manifest.py",
        "nimble/orchestrator/models.py",
        "nimble/orchestrator/planner.py",
        "nimble/orchestrator/readiness.py",
        "nimble/orchestrator/report.py",
    ]

    for relative in required:
        if not (ROOT / relative).is_file():
            failures.append(
                f"Missing orchestrator file: {relative}"
            )

    result = subprocess.run(
        [
            "python",
            "-m",
            "nimble.orchestrator",
            "--root",
            str(ROOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    if result.returncode != 0:
        failures.append(
            "Nimble Build Orchestrator execution failed."
        )

    if not REPORT.is_file():
        failures.append(
            "Orchestrator state report was not generated."
        )
        report = {}
    else:
        report = json.loads(
            REPORT.read_text(
                encoding="utf-8"
            )
        )

        if (
            report.get("schema_version")
            != "1.0"
        ):
            failures.append(
                "Invalid orchestrator report schema."
            )

        capability_ids = {
            item["capability_id"]
            for item in report.get(
                "capabilities",
                [],
            )
        }

        expected = {
            "experience-core",
            "react-primitives",
            "workspace-engine",
            "founder-console",
        }

        missing = expected - capability_ids

        if missing:
            failures.append(
                "Missing orchestrator capabilities: "
                + ", ".join(sorted(missing))
            )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    print("=" * 72)
    print("NIMBLE™ BUILD ORCHESTRATOR VALIDATION")
    print("=" * 72)
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    if result.stdout.strip():
        print()
        print(result.stdout.strip())

    if result.stderr.strip():
        print()
        print(result.stderr.strip())

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )


def write_tests() -> None:
    write_new(
        TEST,
        '''from __future__ import annotations

import json
import subprocess
from pathlib import Path

from nimble.orchestrator.discovery import (
    discover_capabilities,
)
from nimble.orchestrator.planner import (
    create_build_plan,
)


ROOT = Path(__file__).resolve().parents[2]


def test_discovery_finds_known_capabilities() -> None:
    statuses = discover_capabilities(ROOT)

    identifiers = {
        status.capability_id
        for status in statuses
    }

    assert "experience-core" in identifiers
    assert "react-primitives" in identifiers
    assert "workspace-engine" in identifiers
    assert "founder-console" in identifiers


def test_founder_console_depends_on_primitives() -> None:
    statuses = {
        status.capability_id: status
        for status in discover_capabilities(
            ROOT
        )
    }

    founder = statuses["founder-console"]

    assert "react-primitives" in (
        founder.dependencies
    )

    assert "workspace-engine" in (
        founder.dependencies
    )


def test_missing_dependencies_block_capabilities() -> None:
    statuses = {
        status.capability_id: status
        for status in discover_capabilities(
            ROOT
        )
    }

    primitives = statuses[
        "react-primitives"
    ]

    founder = statuses[
        "founder-console"
    ]

    if primitives.state != "implemented":
        assert (
            founder.state == "blocked"
            or founder.state == "implemented"
        )


def test_build_plan_is_dependency_aware() -> None:
    plan = create_build_plan(ROOT)

    identifiers = [
        item.capability_id
        for item in plan
    ]

    if (
        "react-primitives"
        in identifiers
        and "founder-console"
        in identifiers
    ):
        assert (
            identifiers.index(
                "react-primitives"
            )
            < identifiers.index(
                "founder-console"
            )
        )


def test_cli_generates_report() -> None:
    result = subprocess.run(
        [
            "python",
            "-m",
            "nimble.orchestrator",
            "--root",
            str(ROOT),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    report_path = (
        ROOT
        / "reports/nimble/orchestrator/"
        "build-state-latest.json"
    )

    assert report_path.is_file()

    report = json.loads(
        report_path.read_text(
            encoding="utf-8"
        )
    )

    assert (
        report["schema_version"]
        == "1.0"
    )

    assert "build_plan" in report


def test_orchestrator_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_orchestrator.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    assert "Status: PASS" in result.stdout
''',
    )


def run(
    command: list[str],
) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            result.returncode
        )


def main() -> int:
    if PACKAGE.exists():
        existing = [
            path
            for path in PACKAGE.rglob("*")
            if path.is_file()
        ]

        if existing:
            raise RuntimeError(
                "Refusing to overwrite existing "
                "Nimble Build Orchestrator."
            )

    for relative, content in FILES.items():
        write_new(
            PACKAGE / relative,
            content,
        )

    write_validator()
    write_tests()

    run(
        [
            "python",
            "-m",
            "py_compile",
            *[
                str(path)
                for path in PACKAGE.rglob(
                    "*.py"
                )
            ],
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            "-m",
            "pytest",
            "-q",
            str(TEST),
        ]
    )

    print()
    print("=" * 72)
    print("NIMBLE BUILD ORCHESTRATOR COMPLETE")
    print("=" * 72)
    print(
        "Run anytime:"
    )
    print(
        "python -m nimble.orchestrator"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
