"""
Discovery Mission Executor

Genesis 13.25
"""


class DiscoveryMissionExecutor:


    def __init__(
        self,
        connector_runtime=None
    ):

        self.connector_runtime = (
            connector_runtime
        )



    def execute(
        self,
        mission
    ):


        mission.status = (
            "running"
        )


        return {

            "mission":
                mission.name,

            "status":
                mission.status,

            "sources":
                mission.sources

        }

