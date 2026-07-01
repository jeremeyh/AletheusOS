"""
Aletheus Runtime Lifecycle Manager

Version 5.0.1
"""


class LifecycleManager:

    def __init__(self, runtime):
        self.runtime = runtime

    def initialize(self):

        self.runtime.events.publish("runtime.initializing")

    def boot(self):

        self.runtime.events.publish("runtime.boot")

    def ready(self):

        self.runtime.status = "READY"

        self.runtime.events.publish("runtime.ready")

    def shutdown(self):

        self.runtime.status = "STOPPING"

        self.runtime.events.publish("runtime.shutdown")
