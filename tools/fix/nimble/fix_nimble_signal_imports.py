#!/usr/bin/env python3

from pathlib import Path

ROOT = Path.cwd()

FILES = [
    ROOT / "nimble/packages/react/src/primitives/Signal.tsx",
    ROOT / "nimble/packages/react/src/primitives/Instrument.tsx",
]

for path in FILES:
    text = path.read_text(encoding="utf-8")
    original = text

    old = """import type {
  InstrumentStatus,
} from "./types";
"""

    new = """import type {
  InstrumentStatus,
} from "../instrumentation/contracts";
"""

    if old in text:
        text = text.replace(old, new)

    text = text.replace(
        "InstrumentStatus,\n",
        "",
    )

    if text != original:
        path.write_text(
            text,
            encoding="utf-8",
        )
        print(f"Patched {path}")
    else:
        print(f"No changes required: {path}")

print()
print("Import migration complete.")
