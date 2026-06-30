from pathlib import Path

path = Path("aletheus/agents_v2/agent_core.py")
text = path.read_text()

if "def stats(self)" in text:
    print("✔ Agent stats() compatibility already exists.")
    raise SystemExit(0)

anchor = "    def statistics(self):"

if anchor not in text:
    raise SystemExit("statistics() anchor not found in agents_v2/agent_core.py")

insert = '''
    def stats(self):
        return self.statistics()

'''

text = text.replace(anchor, insert + anchor, 1)

path.write_text(text)

print("✔ Added agents_v2 stats() compatibility method.")
