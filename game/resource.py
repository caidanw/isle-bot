import random
import asyncio

from peewee import *
from playhouse.sqlite_ext import JSONField

from game.base_model import BaseModel
from game.island import Island
from game.items.item import ItemLookup
from utils.cache import Cache


class Resource(BaseModel):
    """ Resource class used to represent a place for Player's to obtain various items. """

    name = CharField()
    number = IntegerField(default=0)
    gives_items = JSONField(default=[])
    max_item_amount = IntegerField(default=100)
    item_amount = IntegerField(default=100)
    island = ForeignKeyField(Island, backref='resources')

    @classmethod
    def random(cls, island, min_amt=50, max_amt=500):
        """ Create a random Resource from the resources.json file with a little help
        from the parameters.

        :param island: to to place the resource on
        :param min_amt: of items to give
        :param max_amt: of items to give
        :return: a new instance of the Resource class
        """
        resource = get_random_resource()  # get a random resource from our json data
        name = resource['name']
        resource_num = island.get_amount_of_resources(name) + 1
        items = resource['gives_items']
        amount = random.randint(min_amt, max_amt)

        return Resource.create(name=name,
                               number=resource_num,
                               gives_items=items,
                               max_item_amount=amount,
                               item_amount=amount,
                               island=island)

    # noinspection PyTypeChecker
    @property
    def average_item_harvest_time(self):
        total_time = 0
        for item_name in self.gives_items:
            total_time += ItemLookup[item_name].harvest_time
        return total_time // len(self.gives_items)

    async def harvest(self, amount):
        """ Remove the amount of items within this resource,
        then wait until the player has 'harvested' the items.

        :param amount: of items to harvest
        :return: an ItemStack with the harvested item and amount
        """

        self.item_amount -= amount
        self.save()

        harvested_items = {}
        for i in range(amount):
            item_name = random.choice(self.gives_items)

            # have the program wait until the player has finished harvesting one item
            await asyncio.sleep(ItemLookup[item_name].harvest_time)

            if harvested_items.get(item_name) is None:
                harvested_items[item_name] = 1
            else:
                harvested_items[item_name] += 1

        return harvested_items


def get_random_resource():
    """ Get a random resource from the cached json data

    :return: a dict of the resource
    """
    resource_data = Cache.get_from_json('data/resources.json')
    return random.choice(resource_data)
