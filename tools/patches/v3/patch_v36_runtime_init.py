from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "self.high_availability_v3 = high_availability_core" in text:
    print("✔ Runtime already initializes high_availability_v3.")
    raise SystemExit(0)

anchor = "self.telemetry_v3 = telemetry_core"

if anchor not in text:
    raise SystemExit("Telemetry initialization anchor not found.")

text = text.replace(
    anchor,
    anchor + "\n        self.high_availability_v3 = high_availability_core",
    1,
)

core.write_text(text)

print("✔ Added self.high_availability_v3 initialization.")
