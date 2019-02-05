from src.game.items.abstract_item import AbstractItem


class Crafted(AbstractItem):
    def __init__(self, name, durability):
        super().__init__(name)
        self.durability = durability


class WoodAxe(Crafted):
    def __init__(self):
        super().__init__('wood axe', 5)


class WoodSword(Crafted):
    def __init__(self):
        super().__init__('wood sword', 10)


class WoodShield(Crafted):
    def __init__(self):
        super().__init__('wood shield', 20)


class StoneAxe(Crafted):
    def __init__(self):
        super().__init__('stone axe', 10)


class StoneSword(Crafted):
    def __init__(self):
        super().__init__('stone sword', 15)


class StoneShield(Crafted):
    def __init__(self):
        super().__init__('stone shield', 30)
