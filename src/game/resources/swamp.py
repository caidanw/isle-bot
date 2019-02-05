from src.game.items import material
from src.game.resources.abstract_resource import AbstractResource


class Swamp(AbstractResource):
    def __init__(self):
        super().__init__(
            name='SWAMP',
            materials=[
                material.Clay,
                material.Vine
            ]
        )
