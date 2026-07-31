"""
SPA Runtime Health Registry

Genesis 152
"""


class HealthRegistry:
    def __init__(self):

        self.services = {}

    def register(self, service, status):

        self.services[service] = status

    def report(self):

        return self.services
