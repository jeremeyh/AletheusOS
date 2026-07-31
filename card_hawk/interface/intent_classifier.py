"""
Card Hawk Intent Intelligence Classifier

Genesis 60.7.1
"""


class IntentClassifier:
    def classify(self, request):

        text = request.lower()

        #
        # Acquisition
        #
        if any(
            word in text
            for word in [
                "should i buy",
                "buy this",
                "purchase",
                "acquire",
                "offer",
                "negotiate",
            ]
        ):
            return "acquisition_evaluation"

        #
        # Market Discovery
        #
        if any(
            word in text
            for word in [
                "find",
                "search",
                "discover",
                "undervalued",
                "opportunities",
                "targets",
            ]
        ):
            return "market_discovery"

        #
        # Portfolio
        #
        if any(
            word in text
            for word in [
                "collection",
                "portfolio",
                "holdings",
                "allocation",
                "roi",
                "performance",
            ]
        ):
            return "portfolio_analysis"

        #
        # Comparison / Reasoning
        #
        if any(word in text for word in ["compare", "versus", "vs", "better"]):
            return "cross_asset_reasoning"

        #
        # Community
        #
        if any(word in text for word in ["trade", "collector", "community"]):
            return "community_intelligence"

        return "general_assistant"
