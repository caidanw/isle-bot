from src.game.items.items import Crafted


class StoneAxe(Crafted):
    def __init__(self):
        super().__init__('stone axe', 10)


class StoneSword(Crafted):
    def __init__(self):
        super().__init__('stone sword', 15)
