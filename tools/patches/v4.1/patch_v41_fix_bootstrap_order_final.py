import re
from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Remove every existing direct self._bootstrap_compatibility() call.
text = re.sub(
    r"\n\s*self\._bootstrap_compatibility\(\)\n",
    "\n",
    text,
)

# Ensure self.compat exists before any late bootstrap.
if "self.compat = compatibility_registry" not in text:
    anchor = "self.tenancy_v3 = tenancy_core"
    if anchor not in text:
        raise SystemExit("Could not find tenancy initialization anchor.")
    text = text.replace(
        anchor,
        anchor + "\n        self.compat = compatibility_registry",
        1,
    )

# Put compat assignment late if it currently appears too early.
# Remove the first compat assignment and reinsert it near kernel init.
text = re.sub(
    r"\n\s*# Runtime Compatibility Layer\n\s*self\.compat = compatibility_registry\n+",
    "\n",
    text,
    count=1,
)

anchor = "        self.kernel = KernelExecutor(self)"
if anchor not in text:
    raise SystemExit("KernelExecutor initialization anchor not found.")

replacement = """        self.kernel = KernelExecutor(self)

        # Runtime Compatibility Layer
        self.compat = compatibility_registry
        self._bootstrap_compatibility()"""

text = text.replace(anchor, replacement, 1)

# Make runtime version v4.1.0.
text = text.replace('self.version = "4.0.0"', 'self.version = "4.1.0"')

core.write_text(text)
print("✔ Fixed v4.1 compatibility bootstrap order.")
