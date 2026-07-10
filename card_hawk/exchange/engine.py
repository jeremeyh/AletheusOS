"""
Card Hawk Marketplace Exchange Engine

Genesis 14.10
"""


from .listings import ListingEngine
from .offers import OfferEngine
from .negotiations import NegotiationEngine
from .trades import TradeEngine
from .transactions import TransactionEngine



class ExchangeEngine:


    def __init__(self):

        self.listings = ListingEngine()

        self.offers = OfferEngine()

        self.negotiations = NegotiationEngine()

        self.trades = TradeEngine()

        self.transactions = TransactionEngine()



    def execute(
        self,
        action
    ):


        return {

            "status":

                "processed"

        }

