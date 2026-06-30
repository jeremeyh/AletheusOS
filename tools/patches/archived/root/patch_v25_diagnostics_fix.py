from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

if "Aletheus Cognitive Reasoning Engine" in text and "diagnostics[\"services\"].append" in text:
    print("Diagnostics already patched.")
    raise SystemExit(0)

anchor = """        diagnostics = {
"""

if anchor not in text:
    raise SystemExit("Could not locate diagnostics block.")

insertion = '''
        # Ensure the Reasoning Engine is exposed through runtime diagnostics.
        try:
            if hasattr(self, "reasoning"):
                services = self.services.list_services()
                if "Aletheus Cognitive Reasoning Engine" not in services:
                    self.services.register(
                        "Aletheus Cognitive Reasoning Engine",
                        {
                            "status": "online",
                            "version": getattr(self.reasoning, "version", "2.5.0"),
                        },
                    )
        except Exception:
            pass

'''

text = text.replace(anchor, insertion + anchor, 1)

path.write_text(text)
print("✔ Runtime diagnostics patched for Cognitive Reasoning Engine.")
