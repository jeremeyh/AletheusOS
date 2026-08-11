from pathlib import Path

path = Path("aletheus/agents_v2/agent_core.py")
text = path.read_text()

if "def status(" not in text:
    insert = """

    def status(self):
        return {
            "agents": [a.to_dict() for a in self.agents.values()]
        }

    def list_agents(self):
        return [a.to_dict() for a in self.agents.values()]

"""
    anchor = "    def statistics(self):"
    if anchor not in text:
        raise SystemExit("statistics() not found")
    text = text.replace(anchor, insert + "\n" + anchor, 1)

path.write_text(text)
print("✔ Agent runtime compatibility API added.")
