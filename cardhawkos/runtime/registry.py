class EngineRegistry:
    """
    CardHawkOS™

    Central registry of all engines and services.
    """

    _engines = {}

    @classmethod
    def register(cls, name, engine):
        """
        Register an engine.
        """
        cls._engines[name] = engine

    @classmethod
    def get(cls, name):
        """
        Retrieve an engine.
        """
        return cls._engines.get(name)

    @classmethod
    def names(cls):
        """
        Return registered engine names.
        """
        return sorted(cls._engines.keys())

    @classmethod
    def count(cls):
        """
        Number of registered engines.
        """
        return len(cls._engines)

    @classmethod
    def status(cls):
        """
        Return registry status.
        """
        return [
            {
                "engine": name,
                "loaded": True,
            }
            for name in sorted(cls._engines.keys())
        ]
