"""
CardHawk OS™
Provider Registry
"""

from core.container import container


class ProviderRegistry:

    def __init__(self):
        self.providers={}

    def register(self,name,obj):

        self.providers[name]=obj

        container.register_provider(name,obj)

    def get(self,name):

        return self.providers.get(name)

provider_registry=ProviderRegistry()
