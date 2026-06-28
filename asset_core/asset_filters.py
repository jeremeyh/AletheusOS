class AssetFilters:
    """
    Asset Filters™

    Reusable filtering helpers for Asset Vault™, Command Center™, and Portfolio Engine™.
    """
    @staticmethod
    def by_sport(assets, sport):
        if not sport or sport == "All":
            return assets
        return [a for a in assets if getattr(a, "sport", "") == sport]

    @staticmethod
    def by_team(assets, team):
        if not team or team == "All":
            return assets
        return [a for a in assets if getattr(a, "team", "") == team]

    @staticmethod
    def by_min_thorx(assets, minimum=0):
        return [
            a for a in assets
            if float(getattr(a, "thorx_score", 0) or 0) >= float(minimum)
        ]

    @staticmethod
    def strike_zone(assets):
        return [a for a in assets if bool(getattr(a, "strike_zone", False))]
