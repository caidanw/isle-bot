from game.items.items import Item


""" Forest """


class Wood(Item):
    def __init__(self):
        super().__init__('wood', 5)


class Mushroom(Item):
    def __init__(self):
        super().__init__('mushroom', 4)


class Leaf(Item):
    def __init__(self):
        super().__init__('leaf', 2)


""" Quarry """


class Stone(Item):
    def __init__(self):
        super().__init__('stone', 6)


class Iron(Item):
    def __init__(self):
        super().__init__('iron', 12)


""" Swamp"""


class Clay(Item):
    def __init__(self):
        super().__init__('clay', 6)


class Vine(Item):
    def __init__(self):
        super().__init__('vine', 3)


""" Field """


class Grass(Item):
    def __init__(self):
        super().__init__('grass', 2)


class Wheat(Item):
    def __init__(self):
        super().__init__('wheat', 6)
