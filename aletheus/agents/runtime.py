"""
Agent Runtime

Genesis 13.27
"""


from .memory import AgentMemory
from .governance import AgentGovernance



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

