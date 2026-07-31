"""
Agent Learning Memory

Genesis 13.47
"""


class AgentMemory:
    def __init__(self):

        self.experiences = []

    def learn(self, experience):

        self.experiences.append(experience)
