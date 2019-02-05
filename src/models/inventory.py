from peewee import IntegerField
from playhouse.sqlite_ext import JSONField

from src.models.abstract_model import AbstractModel


class Inventory(AbstractModel):
    """ Inventory class used to manage a Player's items. """

    max_materials = IntegerField(default=200)
    materials = JSONField(default={})
    items = JSONField(default=[])

    def validate_is_room(self, amount):
        """ Check whether the amount of the harvested material can be added to harvested_items,
        also checks that the amount is a non-negative integer.

        :param amount: to check if there is room
        :return: a boolean determining if the amount of item can be added
        """
        if not isinstance(amount, int) or amount < 0:
            return False

        return (sum(self.materials.values()) + amount) <= self.max_materials

    def add_material(self, material, amount=1):
        """ Add the specified amount of the item to the inventory

        :param material: to add
        :param amount: of the item to add
        :return: a boolean showing whether or not the item was added
        """
        if self.validate_is_room(amount):
            if material not in self.materials:
                self.materials[material] = amount
            else:
                self.materials[material] += amount
            self.save()
            return True
        else:
            return False

    def remove_material(self, item, amount=1):
        """ Remove a material of the specified amount from the inventory

        :param item: to remove
        :param amount: of the material to remove
        :return: a boolean showing whether or not the item was removed
        """
        if self.materials[item] >= amount:
            self.materials[item] -= amount

        if self.materials[item] <= 0:
            del self.materials[item]

        self.save()

    def add_item(self, item, amount=1):
        if amount > 0:
            for i in range(amount):
                self.items.append({'name': item.name, 'durability': item.durability})
            self.save()
            return True
        return False

    def has_material(self, name):
        if name in self.materials:
            return True
        return False

    def enough_to_craft(self, recipe):
        for item, amount in recipe.items():
            if not self.has_material(item.name):
                return False
            elif self.materials[item.name] < amount:
                return False
        return True

    def to_message(self, harvested=False, crafted=False):
        output = 'Inventory'
        output += '\n```'

        if harvested:
            output += '\nMATERIALS'
            if len(self.materials) > 0:
                output += '\nITEM       : AMT'
                for item, amount in self.materials.items():
                    output += f'\n{item.ljust(10)} : {str(amount).zfill(3)}'
            else:
                output += '\nYou do not have any harvested materials.'

        # add a divider so the text isn't smashed together
        if harvested and crafted:
            output += '\n'

        if crafted:
            output += '\nCRAFTED ITEMS'
            if len(self.items) > 0:
                output += '\nITEM       : DURABILITY'
                for item in self.items:
                    item_name = item['name'].replace('_', ' ')
                    item_durability = item['durability']
                    output += f'\n{item_name.ljust(10)} : {str(item_durability).zfill(3)}'
            else:
                output += '\nYou do not have any crafted items.'

        if not harvested and not crafted:
            output += f'\nMATERIALS' \
                      f'\n\tCUR AMT : {str(sum(self.materials.values())).zfill(3)}' \
                      f'\n\tMAX AMT : {str(self.max_materials).zfill(3)}' \
                      f'\n' \
                      f'\nITEMS' \
                      f'\n\tCUR AMT : {str(sum(self.items)).zfill(3)}' \
                      f'\n\tMAX AMT : NO LIMIT'

        output += '\n```'
        return output
