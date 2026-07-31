from pathlib import Path

diag = Path("aletheus/runtime/diagnostics.py")
text = diag.read_text()

entry = '("tenancy_v3", "Aletheus Multi-Tenant Runtime"),'

if entry not in text:
    anchors = [
        '("security_v3", "Aletheus Security & Policy Engine"),',
        '("high_availability_v3", "Aletheus High Availability Platform"),',
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
        raise SystemExit("Unable to locate diagnostics insertion point.")

    diag.write_text(text)
    print("✔ Tenancy Runtime added to RuntimeDiagnostics.")

else:
    print("✔ RuntimeDiagnostics already patched.")
