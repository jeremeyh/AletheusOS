"""
Agent Runtime

Genesis 13.27
"""


from .governance import AgentGovernance
from .memory import AgentMemory


class AgentRuntime:


    def __init__(self):

        self.memory = AgentMemory()

        self.governance = AgentGovernance()



    def execute(
        self,
        agent,
        mission
    ):


        authorization = (

            self.governance.authorize(

                agent,

                mission

            )

        )


        self.memory.store(
            authorization
        )


        return authorization

