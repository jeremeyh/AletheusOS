from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

replacements = {
    "self.planning.version": "self.planning_v2.VERSION",
    "self.planning.VERSION": "self.planning_v2.VERSION",
    "self.planning = planning_core": "self.planning_v2 = planning_core",
}

for old, new in replacements.items():
    text = text.replace(old, new)

core.write_text(text)

print("✔ Fixed v2.9 Planning Engine version references.")
