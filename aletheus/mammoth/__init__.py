"""Mammoth™ bounded persistence substrate — Genesis 113.2."""
from .contracts.objects import MammothIdentityStrategy, MammothObjectMetadata, MammothRetentionClass
from .identity.object_ids import MammothObjectIdFactory
from .identity.version_lineage import MammothVersionLineage
from .fabric import MammothProviderRegistry, MammothProviderRequirements
from .providers import LocalDiskPersistenceProvider
__all__=["MammothIdentityStrategy","MammothObjectMetadata","MammothRetentionClass","MammothObjectIdFactory","MammothVersionLineage","MammothProviderRegistry","MammothProviderRequirements","LocalDiskPersistenceProvider"]
__version__="113.2.0"
