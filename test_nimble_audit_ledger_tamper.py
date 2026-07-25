import runpy
from pathlib import Path

runpy.run_path(
    str(
        Path(__file__).resolve().parent
        / "tests"
        / "nimble"
        / "audit"
        / "test_nimble_audit_ledger_tamper.py"
    ),
    run_name="__main__",
)
