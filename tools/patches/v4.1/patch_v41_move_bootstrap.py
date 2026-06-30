from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

old = """
        # Runtime Compatibility Layer
        self.compat = compatibility_registry

        self._bootstrap_compatibility()


        self.copilot = copilot_core
"""

new = """
        # Runtime Compatibility Layer
        self.compat = compatibility_registry


        self.copilot = copilot_core
"""

if old not in text:
    raise SystemExit(
        "Original compatibility bootstrap block not found."
    )

text = text.replace(old, new, 1)

anchor = "        self.kernel = KernelExecutor(self)\n"

if anchor not in text:
    raise SystemExit(
        "Kernel initialization anchor not found."
    )

text = text.replace(
    anchor,
    anchor + "\n        self._bootstrap_compatibility()\n",
    1,
)

core.write_text(text)

print("✔ Compatibility bootstrap moved to end of runtime initialization.")
