"""
Module Discovery Engine

Post-Genesis 80.5
"""

import os


class ModuleDiscoveryEngine:
    def discover(self, root="aletheus"):

        modules = []

        for item in os.listdir(root):
            path = os.path.join(root, item)

            if os.path.isdir(path):
                modules.append(item)

        return {"modules": modules, "count": len(modules)}
