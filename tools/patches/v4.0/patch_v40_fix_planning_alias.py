from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Add legacy compatibility alias if missing.
anchor = "self.planning_v2 = planning_core"

if anchor not in text:
    raise SystemExit("planning_v2 initialization not found.")

alias = anchor + "\n        self.planning = self.planning_v2"

if "self.planning = self.planning_v2" not in text:
    text = text.replace(anchor, alias, 1)
    core.write_text(text)
    print("✔ Added legacy planning alias.")
else:
    print("✔ Planning alias already exists.")
