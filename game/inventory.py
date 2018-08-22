from peewee import IntegerField
from playhouse.sqlite_ext import JSONField

from game.base_model import BaseModel


class Inventory(BaseModel):
    """ Inventory class used to manage a Player's items. """

    max_harvested_items = IntegerField(default=200)
    harvested_items = JSONField(default={})
    crafted_items = JSONField(default=[])

    def validate_is_room(self, amount):
        """ Check whether the amount of the harvested item can be added to harvested_items,
        also checks that the amount is a non-negative integer.

        :param amount: to check if there is room
        :return: a boolean determining if the amount of item can be added
        """
        if not isinstance(amount, int) or amount < 0:
            return False

        return (sum(self.harvested_items.values()) + amount) <= self.max_harvested_items

    def add_item(self, item, amount=1):
        """ Add the specified amount of the item to the inventory

        :param item: to add
        :param amount: of the item to add
        :return: a boolean showing whether or not the item was added
        """
        if self.validate_is_room(amount):
            if item not in self.harvested_items:
                self.harvested_items[item] = amount
            else:
                self.harvested_items[item] += amount
            self.save()
            return True
        else:
            return False

    def remove_item(self, item, amount=1):
        """ Remove an item of the specified amount from the inventory

        :param item: to remove
        :param amount: of the item to remove
        :return: a boolean showing whether or not the item was removed
        """
        if self.harvested_items[item] >= amount:
            self.harvested_items[item] -= amount
            return True
        return False

    def add_craftable(self, item, amount=1):
        if amount > 0:
            for i in range(amount):
                self.crafted_items.append({'name': item.name, 'durability': item.durability()})
            self.save()
            return True
        return False

    def enough_to_craft(self, recipe):
        for item, amount in recipe.items():
            if item.name not in self.harvested_items:
                return False
            elif self.harvested_items[item.name] < amount:
                return False
        return True

    def to_message(self, harvested=False, crafted=False):
        output = 'Inventory'
        output += '\n```'

        if harvested:
            output += '\nHarvested'
            if len(self.harvested_items) > 0:
                output += '\n[item]     : [amount]'
                for item, amount in self.harvested_items.items():
                    output += f'\n{item.ljust(10)} : {str(amount).zfill(3)}'
            else:
                output += '\nYou do not have any harvested items.'

        # add a divider so the text isn't smashed together
        if harvested and crafted:
            output += '\n'

        if crafted:
            output += '\nCrafted'
            if len(self.crafted_items) > 0:
                output += '\n[item]     : [durability]'
                for item in self.crafted_items:
                    item_name = item['name'].replace('_', ' ')
                    item_durability = item['durability']
                    output += f'\n{item_name.ljust(10)} : {str(item_durability).zfill(3)}'
            else:
                output += '\nYou do not have any crafted items.'

        if not harvested and not crafted:
            output += f'\nharvested max amount : {str(self.max_harvested_items).zfill(3)}'
            output += f'\ncrafted max amount   : no limit'

        output += '\n```'
        return output
