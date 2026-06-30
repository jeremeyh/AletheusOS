from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Remove any remaining distributed_v3 references
text = text.replace("self.distributed_v3", "self.distributed")

# Remove duplicate assignment if both exist
lines = text.splitlines()
seen = False
new_lines = []

for line in lines:
    if "self.distributed = distributed_v3_core" in line:
        if seen:
            continue
        seen = True
    new_lines.append(line)

text = "\n".join(new_lines)

core.write_text(text)

print("✔ Runtime unified to canonical distributed runtime.")
