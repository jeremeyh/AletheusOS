from pathlib import Path

path = Path("aletheus/runtime/diagnostics.py")
text = path.read_text()

entry = '("federation_v3", "Aletheus Federated Knowledge Fabric"),'

if entry in text:
    print("Federation diagnostics already present.")
    raise SystemExit(0)

anchor = '("event_bus_v3", "Aletheus Event Bus"),'

if anchor not in text:
    raise SystemExit("Event Bus diagnostics entry not found.")

text = text.replace(
    anchor,
    anchor + "\n            " + entry,
    1,
)

path.write_text(text)

print("✔ Added Federated Knowledge Fabric to RuntimeDiagnostics.")
