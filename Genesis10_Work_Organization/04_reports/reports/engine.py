"""
Card Hawk Intelligence Reports Engine

Genesis 13.18
"""


from .templates import ReportTemplates
from .generators import ReportGenerator



class CardHawkReportsEngine:


    def __init__(
        self
    ):

        self.templates = (
            ReportTemplates()
        )

        self.generator = (
            ReportGenerator()
        )



    def daily(
        self,
        data
    ):

        return self.generator.create(

            "daily",

            "Card Hawk Daily Intelligence",

            self.templates.daily_brief(
                data
            )

        )



    def opportunity(
        self,
        data
    ):

        return self.generator.create(

            "opportunity",

            "Acquisition Opportunity",

            self.templates.opportunity(
                data
            )

        )



    def portfolio(
        self,
        data
    ):

        return self.generator.create(

            "portfolio",

            "Portfolio Intelligence",

            self.templates.portfolio(
                data
            )

        )

