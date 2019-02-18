import asyncio
import random

from peewee import *
from playhouse.sqlite_ext import JSONField

from src.game import resources
from src.game.items import abstract_item
from src.models.abstract_model import AbstractModel
from src.models.island import Island


class Resource(AbstractModel):
    """ Resource class used to represent a place for Player's to obtain various items. """

    name = CharField()
    number = IntegerField(default=0)
    materials = JSONField(default=[])
    material_amount = IntegerField(default=100)
    max_material_amount = IntegerField(default=100)
    island = ForeignKeyField(Island, backref='resources')

    @property
    def average_harvest_time(self):
        total_time = 0
        for item_name in self.materials:
            total_time += abstract_item.get_by_name(item_name).harvest_time
        return total_time // len(list(self.materials))

    @property
    def f_name(self):
        return f'{str(self.name).title()}#{self.number}'

    @classmethod
    def random(cls, island, name=None, min_amt=50, max_amt=500):
        """ Create a random Resource with a little help from the parameters.

        :param island: to place the resource on
        :param name: optional predefined name/type
        :param min_amt: of items to give
        :param max_amt: of items to give
        :return: a new instance of the this class
        """
        resource = random.choice(resources.all_resources())
        resource_num = island.get_amount_of_resources(name) + 1
        amount = random.randint(min_amt, max_amt)

        return Resource.create(name=resource.name,
                               number=resource_num,
                               materials=resource.materials,
                               material_amount=amount,
                               max_material_amount=amount,
                               island=island)

    async def harvest(self, amount):
        """ Remove the amount of materials within this resource,
        then wait until the player has 'harvested' the materials.

        :param amount: of materials to harvest
        :return: an ItemStack with the harvested material and amount
        """

        self.material_amount -= amount
        self.save()

        harvested_materials = {}
        for i in range(amount):
            item_name = random.choice(self.materials)

            # have the program wait until the player has finished harvesting one item
            await asyncio.sleep(abstract_item.get_by_name(item_name).harvest_time)

            if harvested_materials.get(item_name) is None:
                harvested_materials[item_name] = 1
            else:
                harvested_materials[item_name] += 1

        return harvested_materials

    @classmethod
    def is_valid_type(cls, name):
        return name.upper() in ['FOREST', 'FIELD', 'MINE', 'SWAMP']
