"""
Marketplace Connector Contract

Genesis 13.24
"""


from abc import ABC, abstractmethod


class MarketplaceConnector(ABC):


    def __init__(
        self,
        name
    ):

        self.name = name

        self.status = "created"



    @abstractmethod
    def search(
        self,
        query
    ):

        pass



    def health(
        self
    ):

        return {

            "name":
                self.name,

            "status":
                self.status

        }

