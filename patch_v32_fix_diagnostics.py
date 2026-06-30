from pathlib import Path

path = Path("aletheus/runtime/diagnostics.py")
text = path.read_text()

entry = '("persistence_v3", "Aletheus Persistence Engine"),'

if entry in text:
    print("Persistence diagnostics already present.")
    raise SystemExit(0)

anchor = '("plugins_v3", "Aletheus Plugin Manager"),'

if anchor not in text:
    raise SystemExit("Plugin Manager diagnostics entry not found.")

text = text.replace(
    anchor,
    anchor + "\n            " + entry,
    1,
)

path.write_text(text)

print("✔ Added Persistence Engine to RuntimeDiagnostics.")
