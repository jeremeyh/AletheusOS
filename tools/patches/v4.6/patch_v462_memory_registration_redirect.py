from pathlib import Path

CORE = Path("aletheus/runtime/core.py")

if not CORE.exists():
    raise SystemExit("runtime/core.py not found.")

text = CORE.read_text()

old = """
        self.commands.register("memory.remember", self._cmd_memory_remember)
        self.commands.register("memory.recall", self._cmd_memory_recall)
        self.commands.register("memory.stats", self._cmd_memory_stats)
        self.commands.register("memory.clear_working", self._cmd_memory_clear_working)
"""

new = """
        register_memory_commands(self)
"""

if old in text:
    text = text.replace(old, new, 1)

import_line = "    register_memory_commands,\n"

if "register_memory_commands" not in text:
    marker = "from aletheus.runtime.registrations import"

    idx = text.find(marker)

    if idx != -1:
        end = text.find("\n", idx)
        text = text[: end + 1] + import_line + text[end + 1 :]

CORE.write_text(text)

print("✔ Memory registration redirected.")
