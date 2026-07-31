"""
Extension Registry

Genesis 13.46
"""


class ExtensionRegistry:
    def __init__(self):

        self.extensions = {}

    def register(self, extension):

        self.extensions[extension.name] = extension
