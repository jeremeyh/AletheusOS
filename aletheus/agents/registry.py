"""
Agent Registry

Genesis 13.27
"""


class AgentRegistry:
    def __init__(self):

        self.agents = {}

    def register(self, agent):

        self.agents[agent.agent_id] = agent

    def list(self):

        return list(self.agents.keys())
