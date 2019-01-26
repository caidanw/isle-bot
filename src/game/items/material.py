from src.game.items.items import Material

""" Forest """


class Wood(Material):
    def __init__(self):
        super().__init__('wood', 5)


class Mushroom(Material):
    def __init__(self):
        super().__init__('mushroom', 4, consumable=True)


class Leaf(Material):
    def __init__(self):
        super().__init__('leaf', 2)


""" Quarry """


class Stone(Material):
    def __init__(self):
        super().__init__('stone', 6)


class Iron(Material):
    def __init__(self):
        super().__init__('iron', 12)


""" Swamp"""


class Clay(Material):
    def __init__(self):
        super().__init__('clay', 6)


class Vine(Material):
    def __init__(self):
        super().__init__('vine', 3)


""" Field """


class Grass(Material):
    def __init__(self):
        super().__init__('grass', 2)


class Wheat(Material):
    def __init__(self):
        super().__init__('wheat', 6, consumable=True)
