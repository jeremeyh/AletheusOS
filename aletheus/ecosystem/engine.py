"""
Aletheus Ecosystem Core

Post-Genesis 1051-1075
"""


class EcosystemEngine:


    def __init__(self):

        self.members = []


    def initialize(self):

        return {

            "system":
            "aletheus_ecosystem",

            "range":
            "1051-1075",

            "status":
            "operational"

        }


    def register_creator(self, creator):

        member = {

            "creator":
            creator,

            "status":
            "registered"

        }


        self.members.append(member)


        return member



    def list_creators(self):

        return self.members

