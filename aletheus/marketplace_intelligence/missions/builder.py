"""
Discovery Mission Builder

Genesis 13.25
"""


class DiscoveryMissionBuilder:


    def create(
        self,
        mission_id,
        name,
        category,
        query
    ):

        from .models import DiscoveryMission


        return DiscoveryMission(

            mission_id,

            name,

            category,

            query

        )

