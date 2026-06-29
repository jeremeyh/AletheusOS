from abc import ABC
from abc import abstractmethod


class MarketplaceProvider(ABC):
    """
    Base class for all marketplace providers.
    """

    @abstractmethod
    def search(self, card):
        """
        Returns a normalized list of comparable sales.

        Example:

        [
            {
                "price":125,
                "source":"eBay",
                "title":"..."
            }
        ]
        """
        pass
