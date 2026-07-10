"""
Application Registry

Genesis 100.5
"""


class ApplicationRegistry:


    def __init__(self):

        self.apps = []



    def register(self, application):

        self.apps.append(application)



    def list_apps(self):

        return self.apps

