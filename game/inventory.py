class Inventory:
    def __init__(self, max_stack=50):
        self.max_stack = max_stack
        self.items = {}

    def validate_stack(self, item, amount):
        if item not in self.items:
            self.items[item] = 0

        if self.items[item] + amount > self.max_stack:
            return False
        return True

    def add_item(self, item, amount=1):
        """ Add the specified amount of the item to the inventory

        :param item: to add
        :param amount: of the item to add
        :return: a boolean showing whether or not the item was added
        """
        if self.validate_stack(item, amount):
            self.items[item] += amount
            return True
        else:
            return False

    def remove_item(self, item, amount):
        """ Remove an item of the specified amount from the inventory

        :param item: to remove
        :param amount: of the item to remove
        :return: a boolean showing whether or not the item was removed
        """

        if self.items[item] >= amount:
            self.items[item] -= amount
            return True
        return False
