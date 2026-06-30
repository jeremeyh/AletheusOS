from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

service = """
        self.services.register(
            "Aletheus Cognitive Reasoning Engine",
            {
                "status": "online",
                "version": self.reasoning.version,
            },
        )
"""

if '"Aletheus Cognitive Reasoning Engine"' in text:
    print("Reasoning service already registered.")
    raise SystemExit(0)

marker = "self.services.register("

last = text.rfind(marker)

if last == -1:
    raise SystemExit("Could not locate any service registrations.")

line_end = text.find("\n", last)
insert_pos = line_end + 1

text = text[:insert_pos] + service + text[insert_pos:]

path.write_text(text)

print("✔ Added Reasoning Engine service registration.")
