from pathlib import Path
import re

path = Path("aletheus/event_bus_v3/event_bus_core.py")
text = path.read_text()

# Remove accidental double commas introduced by previous patch
text = text.replace(",,", ",")

# Ensure publish() accepts source and future kwargs
pattern = re.compile(
    r"""def\s+publish\s*\(
        \s*self\s*,
        (?P<args>.*?)
    \)\s*:""",
    re.S | re.X,
)

m = pattern.search(text)
if not m:
    raise SystemExit("publish() definition not found.")

args = m.group("args")

if "source=" not in args:
    args = args.rstrip()

    if args.endswith(","):
        args += " source=None, **kwargs"
    else:
        args += ", source=None, **kwargs"

    replacement = f"def publish(self,\n{args}\n):"
    text = pattern.sub(replacement, text, count=1)

path.write_text(text)

print("✔ EventBus publish() signature repaired.")
