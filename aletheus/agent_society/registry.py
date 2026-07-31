"""
Agent Registry

Genesis 13.51
"""


class AgentRegistry:
    def __init__(self):

        self.agents = {}

    def register(self, agent):

        self.agents[agent.agent_id] = agent
