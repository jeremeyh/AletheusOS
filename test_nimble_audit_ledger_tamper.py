from pathlib import Path
import runpy


def main() -> None:
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


if __name__ == "__main__":
    main()
