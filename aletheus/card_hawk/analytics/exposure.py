"""
Collection Exposure Analytics

Genesis 13.17
"""


class ExposureAnalyticsEngine:


    def analyze(
        self,
        assets
    ):

        players = {}


        for asset in assets:

            player = (
                asset.player
            )


            players[player] = (

                players.get(
                    player,
                    0
                )

                +

                asset.estimated_value

            )


        return players

