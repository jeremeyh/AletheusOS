from abc import ABC, abstractmethod


class MarketplaceProvider(ABC):
    """
    Base class for every CardHawk marketplace provider.

    Every provider must implement the same interface.
    """

    @property
    @abstractmethod
    def name(self):
        """
        Marketplace name.
        """
        pass

    @abstractmethod
    def search(self, query):
        """
        Search marketplace.
        """
        pass

    @abstractmethod
    def get_comps(self, card):
        """
        Return sold comparable sales.
        """
        pass

    @abstractmethod
    def get_listings(self, card):
        """
        Return active listings.
        """
        pass

    @abstractmethod
    def get_sales(self, card):
        """
        Return historical sales.
        """
        pass

    @abstractmethod
    def health_check(self):
        """
        Verify provider availability.
        """
        pass
