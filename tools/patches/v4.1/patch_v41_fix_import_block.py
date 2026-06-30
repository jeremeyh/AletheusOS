from pathlib import Path
import re

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Remove every existing compatibility import
text = re.sub(
    r'\n?from aletheus\.runtime\.compat import compatibility_registry\n?',
    '\n',
    text,
)

marker = "from aletheus.runtime.context import RuntimeContext"

if marker not in text:
    raise SystemExit(
        "Couldn't locate RuntimeContext import. "
        "Run: nl -ba aletheus/runtime/core.py | sed -n '1,80p'"
    )

text = text.replace(
    marker,
    marker +
    "\nfrom aletheus.runtime.compat import compatibility_registry",
    1,
)

core.write_text(text)

print("✔ Import block repaired.")
