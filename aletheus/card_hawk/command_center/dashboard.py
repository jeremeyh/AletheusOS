"""
Card Hawk Dashboard Engine

Genesis 13.14
"""

from .widgets import DashboardWidgetFactory


class CardHawkDashboard:
    def __init__(self):

        self.widgets = DashboardWidgetFactory()

    def render(self, context):

        return [
            self.widgets.portfolio_summary(context.get("portfolio", {})),
            self.widgets.intelligence_feed(context.get("intelligence", {})),
            self.widgets.opportunity_feed(context.get("opportunities", [])),
        ]
