#!/usr/bin/env python3

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PRIMITIVE_TYPES = (
    ROOT
    / "nimble/packages/react/src/primitives/types.ts"
)

PRIMITIVE_INSTRUMENT = (
    ROOT
    / "nimble/packages/react/src/primitives/Instrument.tsx"
)

INSTRUMENTATION_CONTRACTS = (
    ROOT
    / "nimble/packages/react/src/instrumentation/contracts.ts"
)

REACT_INDEX = (
    ROOT
    / "nimble/packages/react/src/index.ts"
)

PRIMITIVES_INDEX = (
    ROOT
    / "nimble/packages/react/src/primitives/index.ts"
)

INSTRUMENTATION_INDEX = (
    ROOT
    / "nimble/packages/react/src/instrumentation/index.ts"
)

VALIDATOR = (
    ROOT
    / "validate_nimble_instrumentation_preview.py"
)

TEST_FILE = (
    ROOT
    / "tests/nimble/test_instrumentation_preview.py"
)

BACKUP_ROOT = (
    ROOT
    / ".repair-backups/instrument-status-collision"
)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require_file(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Required file is missing: {relative(path)}"
        )


def backup(path: Path) -> None:
    destination = BACKUP_ROOT / path.relative_to(ROOT)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        path,
        destination,
    )


def write_if_changed(
    path: Path,
    original: str,
    updated: str,
) -> bool:
    if updated == original:
        return False

    backup(path)

    path.write_text(
        updated,
        encoding="utf-8",
    )

    print(f"PATCHED: {relative(path)}")
    return True


def ensure_canonical_contract() -> None:
    path = INSTRUMENTATION_CONTRACTS
    original = path.read_text(encoding="utf-8")

    declaration = re.search(
        r"""
        export\s+type\s+InstrumentStatus\s*=\s*
        (?:
            \|\s*"[^"]+"\s*
        )+
        ;
        """,
        original,
        flags=re.VERBOSE | re.MULTILINE,
    )

    if declaration:
        print(
            "PASS: instrumentation/contracts.ts "
            "owns InstrumentStatus."
        )
        return

    insertion_marker = "export type InstrumentTrend ="

    if insertion_marker not in original:
        raise RuntimeError(
            "Could not locate a safe insertion point in "
            f"{relative(path)}"
        )

    canonical = '''export type InstrumentStatus =
  | "initializing"
  | "healthy"
  | "attention"
  | "review"
  | "critical"
  | "unavailable";


'''

    updated = original.replace(
        insertion_marker,
        canonical + insertion_marker,
        1,
    )

    write_if_changed(
        path,
        original,
        updated,
    )


def remove_primitive_status_declaration() -> None:
    path = PRIMITIVE_TYPES
    original = path.read_text(encoding="utf-8")

    pattern = re.compile(
        r"""
        \n?
        export\s+type\s+InstrumentStatus\s*=\s*
        (?:
            \|\s*"[^"]+"\s*
        )+
        ;
        \n*
        """,
        flags=re.VERBOSE | re.MULTILINE,
    )

    updated, count = pattern.subn(
        "\n",
        original,
        count=1,
    )

    if count == 0:
        if "export type InstrumentStatus" in original:
            raise RuntimeError(
                "Primitive InstrumentStatus declaration exists "
                "but could not be safely removed."
            )

        print(
            "PASS: primitives/types.ts no longer owns "
            "InstrumentStatus."
        )
        return

    write_if_changed(
        path,
        original,
        updated,
    )


def patch_primitive_instrument_imports() -> None:
    path = PRIMITIVE_INSTRUMENT
    original = path.read_text(encoding="utf-8")
    updated = original

    canonical_import = '''import type {
  InstrumentStatus,
} from "../instrumentation/contracts";

'''

    if (
        'from "../instrumentation/contracts"' not in updated
        or "InstrumentStatus" not in updated.split(
            'from "../instrumentation/contracts"', 1
        )[0].rsplit("import", 1)[-1]
    ):
        first_import = re.search(
            r"^import\b",
            updated,
            flags=re.MULTILINE,
        )

        if not first_import:
            raise RuntimeError(
                "Could not locate imports in "
                f"{relative(path)}"
            )

        updated = (
            updated[: first_import.start()]
            + canonical_import
            + updated[first_import.start() :]
        )

    types_import_pattern = re.compile(
        r"""
        import\s+type\s*\{
        (?P<body>[^}]*)
        \}\s*from\s*"\./types";
        """,
        flags=re.VERBOSE | re.MULTILINE,
    )

    match = types_import_pattern.search(updated)

    if match:
        names = [
            item.strip()
            for item in match.group("body").split(",")
            if item.strip()
        ]

        names = [
            name
            for name in names
            if name != "InstrumentStatus"
        ]

        if names:
            replacement = (
                "import type {\n"
                + "".join(
                    f"  {name},\n"
                    for name in names
                )
                + '} from "./types";'
            )
        else:
            replacement = ""

        updated = (
            updated[: match.start()]
            + replacement
            + updated[match.end() :]
        )

    updated = re.sub(
        r"\n{3,}",
        "\n\n",
        updated,
    )

    write_if_changed(
        path,
        original,
        updated,
    )


def ensure_barrel_exports() -> None:
    checks = [
        (
            REACT_INDEX,
            'export * from "./primitives";',
        ),
        (
            REACT_INDEX,
            'export * from "./instrumentation";',
        ),
        (
            INSTRUMENTATION_INDEX,
            'export * from "./contracts";',
        ),
    ]

    for path, export_line in checks:
        original = path.read_text(encoding="utf-8")

        if export_line in original:
            print(
                f"PASS: {relative(path)} exports "
                f"{export_line}"
            )
            continue

        updated = (
            original.rstrip()
            + "\n\n"
            + export_line
            + "\n"
        )

        write_if_changed(
            path,
            original,
            updated,
        )


def verify_public_api_ownership() -> None:
    primitive_files = [
        path
        for path in (
            PRIMITIVE_TYPES.parent.rglob("*")
        )
        if (
            path.is_file()
            and path.suffix in {".ts", ".tsx"}
        )
    ]

    violations: list[str] = []

    for path in primitive_files:
        text = path.read_text(encoding="utf-8")

        if re.search(
            r"\bexport\s+type\s+InstrumentStatus\b",
            text,
        ):
            violations.append(
                f"Primitive still exports InstrumentStatus: "
                f"{relative(path)}"
            )

        if re.search(
            r"\bexport\s*\{[^}]*\bInstrumentStatus\b",
            text,
            flags=re.DOTALL,
        ):
            violations.append(
                f"Primitive re-exports InstrumentStatus: "
                f"{relative(path)}"
            )

    contracts = INSTRUMENTATION_CONTRACTS.read_text(
        encoding="utf-8"
    )

    if not re.search(
        r"\bexport\s+type\s+InstrumentStatus\b",
        contracts,
    ):
        violations.append(
            "Instrumentation contracts do not export "
            "InstrumentStatus."
        )

    instrument = PRIMITIVE_INSTRUMENT.read_text(
        encoding="utf-8"
    )

    if not re.search(
        r"""
        import\s+type\s*\{
        [^}]*\bInstrumentStatus\b[^}]*
        \}\s*from\s*"\.\./instrumentation/contracts";
        """,
        instrument,
        flags=re.VERBOSE | re.DOTALL,
    ):
        violations.append(
            "Primitive Instrument.tsx does not import the "
            "canonical InstrumentStatus contract."
        )

    if violations:
        raise RuntimeError(
            "Public API ownership validation failed:\n- "
            + "\n- ".join(violations)
        )

    print(
        "PASS: InstrumentStatus has one canonical public owner."
    )


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
) -> None:
    print()
    print("$", " ".join(command))

    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Command failed with exit code "
            f"{result.returncode}: "
            + " ".join(command)
        )


def main() -> int:
    print("=" * 72)
    print("NIMBLE™ INSTRUMENT STATUS COLLISION REPAIR")
    print("=" * 72)

    required = [
        PRIMITIVE_TYPES,
        PRIMITIVE_INSTRUMENT,
        INSTRUMENTATION_CONTRACTS,
        REACT_INDEX,
        PRIMITIVES_INDEX,
        INSTRUMENTATION_INDEX,
        VALIDATOR,
        TEST_FILE,
    ]

    for path in required:
        require_file(path)

    ensure_canonical_contract()
    remove_primitive_status_declaration()
    patch_primitive_instrument_imports()
    ensure_barrel_exports()
    verify_public_api_ownership()

    run(
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-react",
        ],
        cwd=ROOT / "nimble",
    )

    run(
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-shell",
        ],
        cwd=ROOT / "nimble",
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
            str(TEST_FILE),
        ]
    )

    run(
        [
            "python",
            "-m",
            "nimble.orchestrator",
        ]
    )

    print()
    print("=" * 72)
    print("INSTRUMENT STATUS COLLISION REPAIR COMPLETE")
    print("=" * 72)
    print(
        "Canonical owner: "
        "nimble/packages/react/src/instrumentation/contracts.ts"
    )
    print(
        "Backup directory: "
        ".repair-backups/instrument-status-collision"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
