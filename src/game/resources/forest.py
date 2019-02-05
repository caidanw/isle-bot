from src.game.items import material, living
from src.game.resources.abstract_resource import AbstractResource


class Forest(AbstractResource):
    def __init__(self):
        super().__init__(
            name='FOREST',
            materials=[
                material.Wood,
                material.Mushroom,
                material.Leaf,
                living.Fairy
            ]
        )
