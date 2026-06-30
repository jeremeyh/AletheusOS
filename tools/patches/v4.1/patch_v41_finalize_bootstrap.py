from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

old = """        self.compat = compatibility_registry
"""

new = """        self.compat = compatibility_registry

        self._bootstrap_compatibility()
"""

text = text.replace(old, new, 1)

# Remove lazy bootstrap calls from handlers
text = text.replace(
    "        self._bootstrap_compatibility()\n\n",
    "",
)

# Reinsert one bootstrap in __init__
text = text.replace(
    "self.compat = compatibility_registry\n",
    "self.compat = compatibility_registry\n\n        self._bootstrap_compatibility()\n",
    1,
)

core.write_text(text)

print("✔ Compatibility now initializes during runtime startup.")
