from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# Fix incorrect runtime attribute names
text = text.replace("self.agents.version", "self.agents_v2.VERSION")
text = text.replace("self.agents.VERSION", "self.agents_v2.VERSION")

# If the service registration accidentally references self.agents,
# correct it to the runtime instance we created.
text = text.replace(
    '"version": self.agents.version',
    '"version": self.agents_v2.VERSION',
)

text = text.replace(
    '"version": self.agents.VERSION',
    '"version": self.agents_v2.VERSION',
)

core.write_text(text)

print("✔ Fixed v2.7 agent runtime version reference.")
