from game.items.item import Item


class Clay(Item):
    def __init__(self):
        super().__init__('clay', 6)


class Vine(Item):
    def __init__(self):
        super().__init__('vine', 3)
