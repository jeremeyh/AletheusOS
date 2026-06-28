from live_data.providers.provider_contract import ProviderContract, LiveListing

class DemoLiveProvider(ProviderContract):
    name = "Demo Live Provider"

    def search(self, query: str, limit: int = 25):
        return [
            LiveListing(
                title=f"{query} Gold /10 Candidate",
                price=275.00,
                source=self.name,
                seller="demo_seller",
            ),
            LiveListing(
                title=f"{query} Rookie Auto PSA 10",
                price=165.00,
                source=self.name,
                seller="demo_seller_2",
            ),
        ][:limit]
