import re
from pathlib import Path

path = Path("aletheus/event_bus_v3/event_bus_core.py")
text = path.read_text()

pattern = re.compile(
    r"def publish\(\s*self,\s*event,\s*payload\s*\):"
)

replacement = (
    "def publish("
    "self, "
    "event, "
    "payload, "
    "source=None, "
    "**kwargs"
    "):"
)

text, count = pattern.subn(replacement, text, count=1)

if count != 1:
    raise SystemExit(
        "publish() signature not found. Inspect event_bus_core.py manually."
    )

path.write_text(text)

print("✔ EventBus publish() now accepts source and future keyword arguments.")
