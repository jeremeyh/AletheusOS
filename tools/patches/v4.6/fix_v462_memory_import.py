from pathlib import Path
import re

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Remove malformed/old registration imports
text = re.sub(
    r"from aletheus\.runtime\.registrations import register_runtime_commands\n",
    "",
    text,
)

text = re.sub(
    r"from aletheus\.runtime\.registrations import \(\n\s*register_runtime_commands,\n\s*\)\n",
    "",
    text,
)

text = re.sub(
    r"from aletheus\.runtime\.registrations import \(\n\s*register_runtime_commands,\n\s*register_memory_commands,\n\s*\)\n",
    "",
    text,
)

# Add correct registration import after governance/services imports
import_block = """from aletheus.runtime.registrations import (
    register_runtime_commands,
    register_memory_commands,
)
"""

if import_block not in text:
    marker = "from aletheus.runtime.services import ServiceRegistry\n"
    if marker not in text:
        raise SystemExit("Could not locate ServiceRegistry import anchor.")

    text = text.replace(marker, marker + import_block, 1)

core.write_text(text)

print("✔ Fixed v4.6.2 runtime registration imports.")
