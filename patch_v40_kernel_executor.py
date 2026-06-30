from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "KernelExecutor" not in text:
    text = text.replace(
        "intelligence_supervisor,\n)",
        "intelligence_supervisor,\n    KernelExecutor,\n)",
        1,
    )

if "self.kernel = KernelExecutor(self)" not in text:
    anchor = "self.intelligence_supervisor = intelligence_supervisor"
    if anchor not in text:
        raise SystemExit("intelligence_supervisor initialization anchor not found.")

    text = text.replace(
        anchor,
        anchor + "\n        self.kernel = KernelExecutor(self)",
        1,
    )

core.write_text(text)

print("✔ KernelExecutor wired into runtime.")
