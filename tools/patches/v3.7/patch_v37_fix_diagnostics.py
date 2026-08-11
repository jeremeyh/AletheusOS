from pathlib import Path

# --------------------------------------------------
# Patch RuntimeDiagnostics
# --------------------------------------------------

diag = Path("aletheus/runtime/diagnostics.py")
text = diag.read_text()

entry = '("security_v3", "Aletheus Security & Policy Engine"),'

if entry not in text:
    anchors = [
        '("high_availability_v3", "Aletheus High Availability Platform"),',
        '("telemetry_v3", "Aletheus Observability Platform"),',
        '("federation_v3", "Aletheus Federated Knowledge Fabric"),',
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
        raise SystemExit("Unable to locate insertion point in runtime/diagnostics.py")

    diag.write_text(text)
    print("✔ Added Security Engine to RuntimeDiagnostics.")

else:
    print("✔ RuntimeDiagnostics already patched.")

# --------------------------------------------------
# Verify runtime integration
# --------------------------------------------------

core = Path("aletheus/runtime/core.py")
runtime = core.read_text()

checks = [
    (
        "Import",
        "from aletheus.security_v3 import security_core",
    ),
    (
        "Initialization",
        "self.security_v3 = security_core",
    ),
    (
        "Command registration",
        'self.commands.register("security.bootstrap"',
    ),
]

print("\nVerification")

for label, token in checks:
    print(f"{label:22}", "OK" if token in runtime else "MISSING")
