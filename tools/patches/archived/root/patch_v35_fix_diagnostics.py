from pathlib import Path

diag = Path("aletheus/runtime/diagnostics.py")
text = diag.read_text()

entry = '("telemetry_v3", "Aletheus Observability Platform"),'

if entry in text:
    print("Telemetry diagnostics already installed.")
    raise SystemExit(0)

# Prefer inserting after federation, otherwise after event bus.
anchors = [
    '("federation_v3", "Aletheus Federated Knowledge Fabric"),',
    '("event_bus_v3", "Aletheus Event Bus"),',
]

anchor = None
for a in anchors:
    if a in text:
        anchor = a
        break

if anchor is None:
    raise SystemExit("Unable to locate diagnostics insertion point.")

text = text.replace(
    anchor,
    anchor + "\n            " + entry,
    1,
)

diag.write_text(text)

print("✔ Added Aletheus Observability Platform to RuntimeDiagnostics.")
