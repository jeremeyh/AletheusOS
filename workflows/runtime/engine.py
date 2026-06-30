from cardhawkos.runtime.orchestrator import RuntimeOrchestrator
from decision_engine.runtime.engine import DecisionEngine
from jobs.system.def_jobs import DEFJobs
from portfolio.digital_twin.engine import PortfolioDigitalTwin


class WorkflowEngine:
    """
    CardHawkOS Workflow Engine™

    Defines repeatable operating workflows.
    """

    @staticmethod
    def portfolio_refresh():
        return RuntimeOrchestrator.run_workflow(
            "Portfolio Refresh",
            [
                (
                    "Load Portfolio Digital Twin",
                    lambda: PortfolioDigitalTwin.snapshot(),
                ),
                (
                    "Run DEF Portfolio Summary",
                    lambda: DecisionEngine.portfolio_summary(),
                ),
            ],
        )

    @staticmethod
    def def_rescore():
        return RuntimeOrchestrator.run_workflow(
            "DEF Rescore",
            [
                (
                    "Rescore All Assets",
                    lambda: DEFJobs.rescore_all(),
                ),
            ],
        )

    @staticmethod
    def nightly_intelligence_refresh():
        return RuntimeOrchestrator.run_workflow(
            "Nightly Intelligence Refresh",
            [
                (
                    "Refresh Portfolio",
                    lambda: PortfolioDigitalTwin.snapshot(),
                ),
                (
                    "Rescore DEF",
                    lambda: DEFJobs.rescore_all(),
                ),
                (
                    "Build DEF Summary",
                    lambda: DecisionEngine.portfolio_summary(),
                ),
            ],
        )
