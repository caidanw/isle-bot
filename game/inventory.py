from peewee import IntegerField
from playhouse.sqlite_ext import JSONField

from game.base_model import BaseModel


class Inventory(BaseModel):
    """ Inventory class used to manage a Player's items. """

    max_stack = IntegerField(default=50)
    items = JSONField(default={})

    def validate_stack(self, item, amount):
        """ Check whether the amount of the item can be added to the inventory,
        without going over the stack limit (also checks that the amount is a non-negative integer).

        :param item: the item to add
        :param amount: the amount to add
        :return: a boolean determining if the amount of item can be added
        """
        if not isinstance(amount, int) or amount < 0:
            return False

        if item not in self.items:
            if amount > self.max_stack:
                return False
            return True

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
            if item not in self.items:
                self.items[item] = amount
            else:
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

    def __repr__(self):
        output = '```\n---Inventory---'
        output += '\n{}: {}'.format('max stack'.ljust(10), str(self.max_stack).zfill(3))
        for item, amount in self.items.items():
            output += '\n{}: {}'.format(item.ljust(10), str(amount).zfill(3))
        output += '\n```'
        return output
