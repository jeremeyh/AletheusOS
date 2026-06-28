from collections import defaultdict


class AllocationEngine:
    """
    Portfolio allocation analytics.
    """

    @staticmethod
    def by_player(assets):

        d=defaultdict(float)

        for asset in assets:

            d[asset.player]+=asset.current_value

        return dict(d)


    @staticmethod
    def by_team(assets):

        d=defaultdict(float)

        for asset in assets:

            d[asset.team]+=asset.current_value

        return dict(d)


    @staticmethod
    def by_sport(assets):

        d=defaultdict(float)

        for asset in assets:

            d[asset.sport]+=asset.current_value

        return dict(d)