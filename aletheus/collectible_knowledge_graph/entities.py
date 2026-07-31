"""
Entity Registry

Genesis 13.37
"""


class EntityRegistry:
    def __init__(self):

        self.entities = {}

    def add(self, entity):

        self.entities[entity.entity_id] = entity

    def get(self, entity_id):

        return self.entities.get(entity_id)
