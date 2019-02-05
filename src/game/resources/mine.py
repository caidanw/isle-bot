from src.game.items import material
from src.game.resources.abstract_resource import AbstractResource


class Mine(AbstractResource):
    def __init__(self):
        super().__init__(
            name='MINE',
            materials=[
                material.Stone,
                material.Iron
            ]
        )
