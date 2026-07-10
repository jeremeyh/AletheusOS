"""
Entity Registry

Genesis 14.6
"""


class EntityRegistry:


    def __init__(self):

        self.entities = {}



    def add(
        self,
        entity
    ):

        self.entities[
            entity.entity_id
        ] = entity

