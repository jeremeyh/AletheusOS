from cardhawkos.runtime.registry import EngineRegistry


class CardHawkKernel:
    """
    CardHawkOS™

    Central operating system kernel.

    Responsible for managing engines,
    services and future plugins.
    """

    VERSION = "0.9 Beta"

    @staticmethod
    def boot():
        """
        Boot CardHawkOS.
        """

        return {
            "version": CardHawkKernel.VERSION,
            "engines": EngineRegistry.count(),
            "status": "ONLINE",
        }

    @staticmethod
    def engine(name):
        """
        Retrieve a registered engine.
        """

        return EngineRegistry.get(name)

    @staticmethod
    def engines():
        """
        Return all registered engines.
        """

        return EngineRegistry.status()
