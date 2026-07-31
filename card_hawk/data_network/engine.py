"""
Global Data Network Engine

Genesis 14.22
"""

from .ingestion import IngestionPipeline
from .normalization import NormalizationEngine


class DataNetworkEngine:
    def __init__(self):

        self.ingestion = IngestionPipeline()

        self.normalization = NormalizationEngine()

    def process(self, data):

        return {"status": "processed"}
