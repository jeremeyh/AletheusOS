#!/usr/bin/env python3

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent

runpy.run_path(
    str(ROOT / "tools" / "append" / "append_nimble_audit_event.py"),
    run_name="__main__",
)
