from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

bad_imports = [
    "import aletheus.agents.agent_core as agent_core\n",
    "from aletheus.agents import agent_core as agent_core_module\n",
    "from aletheus.agents import agent_core_module\n",
]

for bad in bad_imports:
    text = text.replace(bad, "")

if "from aletheus.agents import agent_core\n" not in text:
    anchor = "from aletheus.executive import executive_core\n"
    if anchor in text:
        text = text.replace(anchor, anchor + "from aletheus.agents import agent_core\n")
    else:
        raise SystemExit("Could not find executive_core import anchor.")

text = text.replace("self.agents = agent_core.agent_core", "self.agents = agent_core")
text = text.replace("self.agents = agents.agent_core", "self.agents = agent_core")
text = text.replace("self.agents = aletheus.agents.agent_core", "self.agents = agent_core")

if "self.agents = agent_core" not in text:
    anchor = "self.executive = executive_core\n"
    if anchor in text:
        text = text.replace(anchor, anchor + "        self.agents = agent_core\n")
    else:
        raise SystemExit("Could not find executive assignment anchor.")

path.write_text(text)
print("Runtime agent import/assignment repaired.")
