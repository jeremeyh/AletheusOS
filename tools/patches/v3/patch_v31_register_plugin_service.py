from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

service = """
        self.services.register(
            "Aletheus Plugin Manager",
            {
                "status": "online",
                "version": self.plugins_v3.VERSION,
            },
        )
"""

if "Aletheus Plugin Manager" in text:
    print("Plugin service already present.")
    raise SystemExit(0)

anchor = 'self.services.register("Aletheus Distributed Runtime Fabric"'

idx = text.find(anchor)
if idx == -1:
    raise SystemExit("Distributed Runtime Fabric registration not found.")

end = text.find("\n\n", idx)
if end == -1:
    end = text.find("\n        self.commands.register", idx)

text = text[:end] + "\n" + service + text[end:]

path.write_text(text)

print("✔ Plugin Manager service registered.")
