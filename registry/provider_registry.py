class ProviderRegistry:
    def __init__(self):
        self.providers = {}

    def register(self, name, provider):
        self.providers[name] = provider
        return provider

    def get(self, name):
        return self.providers.get(name)

    def all(self):
        return self.providers

    def names(self):
        return sorted(self.providers.keys())

    def register_alpha_defaults(self):
        paths = {
            "ebay": ("providers.ebay_live", "EbayLive"),
            "mercari": ("providers.mercari_live", "MercariLive"),
            "comc": ("providers.comc_live", "ComcLive"),
            "goldin": ("providers.goldin_live", "GoldinLive"),
            "pwcc": ("providers.pwcc_live", "PwccLive"),
            "fanatics": ("providers.fanatics_live", "FanaticsLive"),
        }
        for name, (module_path, class_name) in paths.items():
            try:
                module = __import__(module_path, fromlist=[class_name])
                self.register(name, getattr(module, class_name)())
            except Exception:
                pass
        return self
