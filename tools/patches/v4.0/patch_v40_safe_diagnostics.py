import re
from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Replace direct .stats() calls with a compatibility expression.
pattern = re.compile(r"self\.([A-Za-z_][A-Za-z0-9_]*)\.stats\(\)")

def repl(match):
    obj = match.group(1)
    return (
        f"(self.{obj}.stats() "
        f"if hasattr(self.{obj}, 'stats') "
        f"else self.{obj}.statistics() "
        f"if hasattr(self.{obj}, 'statistics') "
        f"else {{'status': getattr(self.{obj}, 'status', 'unknown')}})"
    )

new_text, count = pattern.subn(repl, text)

if count == 0:
    print("No .stats() calls found to patch.")
else:
    core.write_text(new_text)
    print(f"✔ Patched {count} .stats() calls in runtime diagnostics.")
