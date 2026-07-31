from pathlib import Path

diag = Path("aletheus/runtime/diagnostics.py")
text = diag.read_text()

entry = '("high_availability_v3", "Aletheus High Availability Platform"),'

if entry not in text:
    anchors = [
        '("telemetry_v3", "Aletheus Observability Platform"),',
        '("federation_v3", "Aletheus Federated Knowledge Fabric"),',
        '("event_bus_v3", "Aletheus Event Bus"),',
    ]

    inserted = False

    for anchor in anchors:
        if anchor in text:
            text = text.replace(
                anchor,
                anchor + "\n            " + entry,
                1,
            )
            inserted = True
            break

    if not inserted:
        raise SystemExit("Could not locate a diagnostics insertion point.")

    diag.write_text(text)
    print("✔ Added High Availability to RuntimeDiagnostics.")

else:
    print("✔ Diagnostics already patched.")

core = Path("aletheus/runtime/core.py")
runtime = core.read_text()

if "self.high_availability_v3 = high_availability_core" not in runtime:
    print("WARNING: Runtime never initializes high_availability_v3")

if "from aletheus.high_availability_v3 import high_availability_core" not in runtime:
    print("WARNING: Runtime never imports high_availability_v3")

if "ha.bootstrap" not in runtime:
    print("WARNING: HA commands not registered")
