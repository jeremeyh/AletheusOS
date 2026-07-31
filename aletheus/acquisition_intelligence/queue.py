"""
Acquisition Queue
"""


class AcquisitionQueue:
    def rank(self, assets):

        return sorted(assets, key=lambda x: x.get("confidence", 0), reverse=True)
