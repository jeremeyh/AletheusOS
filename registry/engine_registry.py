class EngineRegistry:
    def __init__(self):
        self.engines = {}

    def register(self, name, engine):
        self.engines[name] = engine
        return engine

    def get(self, name):
        return self.engines.get(name)

    def names(self):
        return sorted(self.engines.keys())

    def register_alpha_defaults(self):
        paths = {
            "thorx": ("thorx.score", "ThorxScore"),
            "dex": ("thorx.dex_engine", "DEXEngine"),
            "def": ("thorx.def_engine", "DEFEngine"),
        }
        for name, (module_path, class_name) in paths.items():
            try:
                module = __import__(module_path, fromlist=[class_name])
                self.register(name, getattr(module, class_name))
            except Exception:
                pass
        return self
