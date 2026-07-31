"""
Market Saturation Index

Genesis 13.9

Measures supply pressure versus opportunity.
"""


class MarketSaturationIndex:
    def calculate(self, supply, demand):

        if demand == 0:
            return 100

        index = supply / demand

        return min(int(index * 100), 100)
