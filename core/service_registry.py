"""
CardHawk OS™
Service Registry
"""

from core.container import container

class ServiceRegistry:

    def __init__(self):
        self.services = {}

    def register(self,name,obj):

        self.services[name]=obj

        container.register_service(name,obj)

    def get(self,name):

        return self.services.get(name)

service_registry=ServiceRegistry()
