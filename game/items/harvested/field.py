from game.items.item import Item


class Grass(Item):
    def __init__(self):
        super().__init__('grass', 2)


class Wheat(Item):
    def __init__(self):
        super().__init__('wheat', 6)
