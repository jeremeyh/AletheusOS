"""
Card Hawk Intelligence Reports

Genesis 13.11
"""


class IntelligenceReportBuilder:
    def build(self, context):

        return {
            "asset_id": context.asset_id,
            "signals": context.signals,
            "analysis": context.analysis,
            "decisions": context.decisions,
        }
