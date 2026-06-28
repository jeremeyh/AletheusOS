from engines.qdef_engine import QDEFEngine
from engines.ddef_engine import DDEFEngine


class DEXEngine:
    """
    Decision Execution Engine™

    Final intelligence layer.
    """

    @staticmethod
    def evaluate(asset):

        qdef=QDEFEngine.evaluate(asset)

        ddef=DDEFEngine.evaluate(asset,qdef)

        return {

            "qdef":qdef,

            "ddef":ddef,

            "action":ddef.recommendation,

            "confidence":ddef.confidence

        }