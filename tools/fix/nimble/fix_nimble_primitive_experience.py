#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REACT_PACKAGE = ROOT / "nimble/packages/react"

TSCONFIG = REACT_PACKAGE / "tsconfig.json"

TOKENS = REACT_PACKAGE / "src/primitives/tokens.ts"

REACT_INDEX = REACT_PACKAGE / "src/index.ts"

PRIMITIVES_INDEX = REACT_PACKAGE / "src/primitives/index.ts"

VALIDATOR = ROOT / "validate_nimble_primitive_experience.py"

TEST_FILE = ROOT / "tests/nimble/test_primitive_experience.py"


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
        raise SystemExit(result.returncode)


def patch_tsconfig() -> None:
    if not TSCONFIG.is_file():
        raise RuntimeError(
            "Missing React package tsconfig: " + str(TSCONFIG.relative_to(ROOT))
        )

    configuration = json.loads(TSCONFIG.read_text(encoding="utf-8"))

    compiler_options = configuration.setdefault(
        "compilerOptions",
        {},
    )

    previous = compiler_options.get("jsx")

    compiler_options["jsx"] = "react-jsx"

    TSCONFIG.write_text(
        json.dumps(
            configuration,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    if previous == "react-jsx":
        print("React JSX compiler setting already correct.")
    else:
        print('Enabled compilerOptions.jsx = "react-jsx".')


def patch_tokens() -> None:
    if not TOKENS.is_file():
        raise RuntimeError(
            "Missing primitive token helper: " + str(TOKENS.relative_to(ROOT))
        )

    text = TOKENS.read_text(encoding="utf-8")

    old = """export function token(
  name: ExperienceTokenName,
): string | number {
  return experienceTokens[name];
}"""

    replacement = """export function token(
  name: ExperienceTokenName,
): string | number {
  const value = experienceTokens[name];

  if (value === undefined) {
    throw new Error(
      `Unknown experience token: ${name}`,
    );
  }

  return value;
}"""

    if old in text:
        text = text.replace(
            old,
            replacement,
        )

        TOKENS.write_text(
            text,
            encoding="utf-8",
        )

        print("Patched strict-safe token accessor.")
        return

    if (
        "const value = experienceTokens[name];" in text
        and "Unknown experience token:" in text
    ):
        print("Token accessor already strict-safe.")
        return

    raise RuntimeError(
        "Could not safely identify the token() "
        "implementation in " + str(TOKENS.relative_to(ROOT))
    )


def patch_validator() -> None:
    if not VALIDATOR.is_file():
        raise RuntimeError(
            "Missing primitive validator: " + str(VALIDATOR.relative_to(ROOT))
        )

    text = VALIDATOR.read_text(encoding="utf-8")

    # The validator scans only the React primitive
    # package. Engine color mappings belong to
    # Experience Core, so requiring the literal
    # "instrumentation.engine" here is incorrect.
    text = text.replace(
        '        "instrumentation.engine",\n',
        "",
    )

    text = text.replace(
        '        "instrument.engine",\n',
        "",
    )

    required_markers = [
        '"instrument.aletheus-index"',
        '"instrument.thorx"',
    ]

    for marker in required_markers:
        if marker not in text:
            insertion_marker = '        "THORᵡ",\n'

            if insertion_marker not in text:
                raise RuntimeError(
                    "Could not locate the "
                    "required_concepts list in " + str(VALIDATOR.relative_to(ROOT))
                )

            text = text.replace(
                insertion_marker,
                insertion_marker + f"        {marker},\n",
                1,
            )

    VALIDATOR.write_text(
        text,
        encoding="utf-8",
    )

    print("Corrected primitive validator concepts.")


def ensure_export(
    path: Path,
    export_line: str,
) -> None:
    if not path.is_file():
        raise RuntimeError("Missing export file: " + str(path.relative_to(ROOT)))

    text = path.read_text(encoding="utf-8")

    if export_line in text:
        print(
            "Export already present:",
            export_line,
        )
        return

    path.write_text(
        text.rstrip() + "\n\n" + export_line + "\n",
        encoding="utf-8",
    )

    print(
        "Added export:",
        export_line,
    )


def validate_primitive_index() -> None:
    if not PRIMITIVES_INDEX.is_file():
        raise RuntimeError(
            "Missing primitive package index: "
            + str(PRIMITIVES_INDEX.relative_to(ROOT))
        )

    required_exports = [
        'export * from "./Badge";',
        'export * from "./Grid";',
        'export * from "./Instrument";',
        'export * from "./Meter";',
        'export * from "./Panel";',
        'export * from "./Separator";',
        'export * from "./Signal";',
        'export * from "./Stack";',
        'export * from "./Surface";',
        'export * from "./Text";',
        'export * from "./reserved";',
        'export * from "./tokens";',
        'export * from "./types";',
    ]

    text = PRIMITIVES_INDEX.read_text(encoding="utf-8")

    missing = [
        export_line for export_line in required_exports if export_line not in text
    ]

    if not missing:
        print("Primitive index exports complete.")
        return

    updated = text.rstrip()

    for export_line in missing:
        updated += "\n" + export_line

    PRIMITIVES_INDEX.write_text(
        updated + "\n",
        encoding="utf-8",
    )

    print(
        "Added missing primitive exports:",
        len(missing),
    )


def main() -> int:
    print("=" * 72)
    print("NIMBLE™ PRIMITIVE EXPERIENCE REPAIR")
    print("=" * 72)

    patch_tsconfig()
    patch_tokens()
    patch_validator()

    ensure_export(
        REACT_INDEX,
        'export * from "./primitives";',
    )

    validate_primitive_index()

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
    print("PRIMITIVE EXPERIENCE REPAIR COMPLETE")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
