import re
from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Replace every ".stats()" call with a compatibility expression.
pattern = re.compile(r"self\.([A-Za-z_][A-Za-z0-9_]*)\.stats\(\)")

count = 0

def repl(match):
    global count
    count += 1
    obj = match.group(1)
    return (
        f'(self.{obj}.stats() '
        f'if hasattr(self.{obj}, "stats") '
        f'else self.{obj}.statistics())'
    )

text = pattern.sub(repl, text)

core.write_text(text)

print(f"✔ Patched {count} runtime diagnostics stats() calls.")
