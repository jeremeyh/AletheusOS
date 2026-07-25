import re
from pathlib import Path

# Locate the event bus implementation
candidates = [
    Path("aletheus/event_bus_v3/event_bus_core.py"),
    Path("aletheus/event_bus_v3/event_bus.py"),
    Path("aletheus/event_bus_v3/core.py"),
]

path = None
for candidate in candidates:
    if candidate.exists():
        path = candidate
        break

if path is None:
    raise SystemExit("Could not locate the Event Bus implementation.")

text = path.read_text()

# Match any publish() signature that starts with def publish(self,...
pattern = re.compile(
    r"def\s+publish\s*\(\s*self\s*,(?P<args>.*?)\)\s*:",
    re.DOTALL,
)

match = pattern.search(text)

if not match:
    raise SystemExit("Could not locate publish() definition.")

args = match.group("args")

# Already patched?
if "source" in args:
    print("✔ publish() already accepts source.")
    raise SystemExit(0)

new_args = args.rstrip()

if new_args.strip():
    new_args = new_args + ", source=None, **kwargs"
else:
    new_args = "source=None, **kwargs"

replacement = f"def publish(self,{new_args}):"

text = pattern.sub(replacement, text, count=1)

path.write_text(text)

print(f"✔ Patched {path}")
