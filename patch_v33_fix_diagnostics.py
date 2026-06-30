from pathlib import Path

path = Path("aletheus/runtime/diagnostics.py")
text = path.read_text()

entry = '("event_bus_v3", "Aletheus Event Bus"),'

if entry in text:
    print("Event Bus diagnostics already present.")
    raise SystemExit(0)

anchor = '("persistence_v3", "Aletheus Persistence Engine"),'

if anchor not in text:
    raise SystemExit("Persistence Engine diagnostics entry not found.")

text = text.replace(
    anchor,
    anchor + "\n            " + entry,
    1,
)

path.write_text(text)

print("✔ Added Event Bus to RuntimeDiagnostics.")
