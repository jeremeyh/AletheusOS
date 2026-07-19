from aletheus.agents_v2 import agent_core

print(type(agent_core))
print(agent_core)

print("Has VERSION:", hasattr(agent_core, "VERSION"))
print("Has bootstrap:", hasattr(agent_core, "bootstrap"))
