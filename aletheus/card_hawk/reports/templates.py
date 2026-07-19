"""
Card Hawk Report Templates

Genesis 13.18
"""


class ReportTemplates:


    def daily_brief(
        self,
        data
    ):

        return {

            "title":
                "Card Hawk Daily Intelligence",

            "sections":
                data

        }



    def opportunity(
        self,
        data
    ):

        return {

            "title":
                "Acquisition Opportunity",

            "sections":
                data

        }



    def portfolio(
        self,
        data
    ):

        return {

            "title":
                "Portfolio Intelligence Report",

            "sections":
                data

        }

