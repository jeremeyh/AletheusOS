import re
from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

# Remove all existing compat assignment/bootstrap lines in __init__
text = re.sub(r"\n\s*# Runtime Compatibility Layer\n\s*self\.compat = compatibility_registry\n\s*self\._bootstrap_compatibility\(\)\n", "\n", text)
text = re.sub(r"\n\s*self\.compat = compatibility_registry\n", "\n", text)
text = re.sub(r"\n\s*self\._bootstrap_compatibility\(\)\n", "\n", text)

anchor = "        self.boot()\n"

if anchor not in text:
    raise SystemExit("self.boot() anchor not found.")

insert = """        # Runtime Compatibility Layer
        self.compat = compatibility_registry
        self._bootstrap_compatibility()

"""

text = text.replace(anchor, insert + anchor, 1)

path.write_text(text)

print("✔ Compatibility bootstrap moved immediately before self.boot().")
