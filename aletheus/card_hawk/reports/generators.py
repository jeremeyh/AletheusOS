"""
Card Hawk Report Generators

Genesis 13.18
"""


from .models import IntelligenceReport



class ReportGenerator:


    def create(
        self,
        report_type,
        title,
        data
    ):

        return IntelligenceReport(

            report_type=
                report_type,

            title=
                title,

            summary=
                "Generated intelligence report",

            data=
                data

        )

