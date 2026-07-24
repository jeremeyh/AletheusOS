from pathlib import Path

path = Path("tests/nimble/test_audit_checkpoints.py")

text = path.read_text()

old = '''result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "test_nimble_audit_checkpoint_tamper.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0'''

new = '''result = subprocess.run(
        [
            "python",
            "-m",
            "pytest",
            str(
                ROOT
                / "tests"
                / "nimble"
                / "audit"
                / "test_nimble_audit_checkpoint_tamper.py"
            ),
            "-q",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, (
        f"Checkpoint tamper simulation failed.\\n\\n"
        f"STDOUT:\\n{result.stdout}\\n\\n"
        f"STDERR:\\n{result.stderr}"
    )'''

if old not in text:
    raise SystemExit("Expected code block not found.")

path.write_text(text.replace(old, new))
print(f"Updated {path}")
