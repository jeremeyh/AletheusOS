from live_data.live_data_service import LiveDataService

class LiveDataActivationService:
    @staticmethod
    def runtime():
        return LiveDataService()

    @staticmethod
    def search(query):
        return LiveDataService().search(query)

    @staticmethod
    def comps(query):
        return LiveDataService().comps(query)

    @staticmethod
    def watch(query, max_price=0, min_score=0):
        return LiveDataService().add_watch(query, max_price, min_score)

    @staticmethod
    def scan_watchlist():
        return LiveDataService().scan_watchlist()
