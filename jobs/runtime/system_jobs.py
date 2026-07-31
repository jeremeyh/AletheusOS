from jobs.runtime.scheduler import JobScheduler


class SystemJobs:
    @staticmethod
    def register():

        JobScheduler.register(
            "Marketplace Refresh", lambda: print("Refreshing marketplace...")
        )

        JobScheduler.register(
            "Portfolio Rescore", lambda: print("Rescoring portfolio...")
        )

        JobScheduler.register("Timeline Cleanup", lambda: print("Cleaning timeline..."))

        JobScheduler.register(
            "Deal Finder Scan", lambda: print("Scanning marketplace deals...")
        )

        JobScheduler.register("Watchlist Scan", lambda: print("Scanning watchlists..."))

        JobScheduler.register(
            "Genome Snapshot", lambda: print("Creating genome snapshot...")
        )

        JobScheduler.register(
            "Founder Brief Refresh", lambda: print("Refreshing Founder AI briefs...")
        )

        JobScheduler.register(
            "Marketplace Intelligence",
            lambda: print("Collecting marketplace intelligence..."),
        )
