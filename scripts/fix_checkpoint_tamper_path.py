from pathlib import Path

path = Path("tests/nimble/test_audit_checkpoints.py")
text = path.read_text(encoding="utf-8")

old = '''ROOT
                / "test_nimble_audit_checkpoint_tamper.py"'''

new = '''ROOT
                / "tests"
                / "nimble"
                / "audit"
                / "test_nimble_audit_checkpoint_tamper.py"'''

if old not in text:
    raise SystemExit("Expected path not found. The file may already be modified.")

path.write_text(text.replace(old, new), encoding="utf-8")
print(f"Updated {path}")
