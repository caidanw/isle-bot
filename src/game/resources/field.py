from src.game.items import material, living
from src.game.resources.abstract_resource import AbstractResource


class Field(AbstractResource):
    def __init__(self):
        super().__init__(
            name='FIELD',
            materials=[
                material.Grass,
                material.Wheat,
                living.Fairy
            ]
        )
