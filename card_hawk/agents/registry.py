"""
Agent Registry

Genesis 14.23
"""


class AgentRegistry:


    def __init__(self):

        self.agents = {}



    def register(
        self,
        name,
        agent
    ):

        self.agents[name] = agent

