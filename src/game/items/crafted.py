from game.items.items import Crafted


class StoneAxe(Crafted):
    def __init__(self):
        super().__init__('stone axe', 10)
