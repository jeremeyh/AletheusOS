"""
Legacy Service Adapter
"""

from core.service_base import ServiceBase


class ServiceAdapter(ServiceBase):

    def __init__(self,module):

        self.module = module

        self.name = getattr(module,"SERVICE_NAME",module.__name__.split(".")[-1])

        self.version = getattr(module,"SERVICE_VERSION","legacy")

    def initialize(self):

        fn = getattr(self.module,"initialize",None)

        if callable(fn):
            fn()

        return True

    def shutdown(self):

        fn = getattr(self.module,"shutdown",None)

        if callable(fn):
            fn()

        return True
