import re
from pathlib import Path

path = Path("aletheus/runtime/compat/registry.py")
text = path.read_text()

pattern = re.compile(
    r"def statistics\(self\):.*?return\s*\{.*?\}",
    re.DOTALL,
)

replacement = '''def statistics(self):

        return {
            "version": self.VERSION,
            "registered": len(self.services),
            "services": len(self.services),
            "aliases": sorted(self.services.keys()),
            "health": "healthy",
        }'''

text, count = pattern.subn(replacement, text, count=1)

if count != 1:
    raise SystemExit(
        "Could not patch statistics(). Inspect registry.py manually."
    )

path.write_text(text)

print("✔ CompatibilityRegistry.statistics() updated.")
