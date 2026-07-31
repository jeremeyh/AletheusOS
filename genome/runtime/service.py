from asset_core.asset_genome import AssetGenome


class GenomeService:
    """
    Runtime manager for Asset Genome™.
    """

    _genomes = {}

    @classmethod
    def get(cls, asset_uuid):

        if asset_uuid not in cls._genomes:
            cls._genomes[asset_uuid] = AssetGenome(asset_uuid)

        return cls._genomes[asset_uuid]
