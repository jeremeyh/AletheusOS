from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

old = "self.distributed = distributed_core"
new = (
    "self.distributed = distributed_v3_core\n"
    "        self.distributed_v3 = distributed_v3_core"
)

if old in text:
    text = text.replace(old, new, 1)
    path.write_text(text)
    print("✔ Runtime now aliases distributed -> distributed_v3.")
else:
    print("Could not find legacy distributed assignment.")
