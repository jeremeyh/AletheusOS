"""
Card Hawk Dashboard Widgets

Genesis 13.14
"""


class DashboardWidgetFactory:
    def portfolio_summary(self, portfolio):

        return {"type": "portfolio_summary", "data": portfolio}

    def intelligence_feed(self, signals):

        return {"type": "intelligence_feed", "data": signals}

    def opportunity_feed(self, opportunities):

        return {"type": "opportunity_feed", "data": opportunities}
