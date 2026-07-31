from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Canonical runtime object
text = text.replace(
    "self.distributed_v3 = distributed_v3_core",
    "self.distributed = distributed_v3_core",
)

# Remove any remaining legacy assignment
text = text.replace("self.distributed = distributed_core", "")

# Remove legacy import
text = text.replace("from aletheus.distributed import distributed_core\n", "")

# Rename remaining references
text = text.replace("self.distributed_v3.", "self.distributed.")

core.write_text(text)

print("✔ Distributed Runtime v3 is now the canonical runtime.")
