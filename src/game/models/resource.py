import random
import asyncio

from peewee import *
from playhouse.sqlite_ext import JSONField

from src.game import BaseModel
from src.game import Island
from src.game.items import items
from src.utils.cache import Cache


class Resource(BaseModel):
    """ Resource class used to represent a place for Player's to obtain various items. """

    name = CharField()
    number = IntegerField(default=0)
    gives_materials = JSONField(default=[])
    max_material_amount = IntegerField(default=100)
    material_amount = IntegerField(default=100)
    island = ForeignKeyField(Island, backref='resources')

    @property
    def average_harvest_time(self):
        total_time = 0
        for item_name in self.gives_materials:
            total_time += items.get_by_name(item_name).harvest_time
        return total_time // len(self.gives_materials)

    @property
    def f_name(self):
        return f'{self.name.title()}#{self.number}'

    @classmethod
    def random(cls, island, name=None, min_amt=50, max_amt=500):
        """ Create a random Resource from the resources.json file with a little help
        from the parameters.

        :param island: to to place the resource on
        :param name: optional predefined name/type
        :param min_amt: of items to give
        :param max_amt: of items to give
        :return: a new instance of the Resource class
        """
        resource = get_random_resource()  # get a random resource from our json data

        if name is None:
            name = resource['name']
        elif not cls.is_valid_type(name):
            raise ValueError('Not a valid resource type')

        resource_num = island.get_amount_of_resources(name) + 1
        materials = resource['gives_materials']
        amount = random.randint(min_amt, max_amt)

        return Resource.create(name=name,
                               number=resource_num,
                               gives_materials=materials,
                               max_material_amount=amount,
                               material_amount=amount,
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
            item_name = random.choice(self.gives_materials)

            # have the program wait until the player has finished harvesting one item
            await asyncio.sleep(items.get_by_name(item_name).harvest_time)

            if harvested_materials.get(item_name) is None:
                harvested_materials[item_name] = 1
            else:
                harvested_materials[item_name] += 1

        return harvested_materials

    @classmethod
    def is_valid_type(cls, name):
        return name.lower() in ['forest', 'quarry', 'swamp', 'field']


def get_random_resource():
    """ Get a random resource from the cached json data

    :return: a dict of the resource
    """
    resource_data = Cache.get_from_json('data/resources.json')
    return random.choice(resource_data)
