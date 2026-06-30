from pathlib import Path

path = Path("aletheus/agents_v2/agent_core.py")
text = path.read_text()

if "def register_default_agents" in text:
    print("register_default_agents already exists.")
    raise SystemExit(0)

anchor = "    def bootstrap(self):"

if anchor not in text:
    raise SystemExit("Could not locate bootstrap().")

insert = '''
    def register_default_agents(self):
        """
        Backwards-compatible alias expected by the runtime.
        """
        return self.bootstrap()

'''

text = text.replace(anchor, insert + anchor, 1)

path.write_text(text)

print("✔ Added register_default_agents compatibility method.")
