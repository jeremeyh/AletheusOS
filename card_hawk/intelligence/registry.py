"""
Card Hawk Intelligence Registry

Genesis 14.14
"""


class IntelligenceRegistry:


    def __init__(self):

        self.domains = {}



    def register(
        self,
        name,
        domain
    ):

        self.domains[name] = domain



    def get(
        self,
        name
    ):

        return self.domains.get(name)

