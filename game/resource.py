import random
import asyncio

from peewee import *

from game.base_model import BaseModel
from game.island import Island
from game.item import ItemStack
from utils.cache import Cache


class Resource(BaseModel):
    """ Resource class used to represent a place for Player's to obtain various items. """

    name = CharField()
    gives_item = CharField()
    seconds_to_one_item = IntegerField()
    max_item_amount = IntegerField(default=100)
    item_amount = IntegerField(default=100)
    on_island = ForeignKeyField(Island, backref='resources')

    @classmethod
    def random(cls, island, min_amt=50, max_amt=500):
        """ Create a random Resource from the resources.json file with a little help
        from the parameters.

        :param island: to to place the resource on
        :param min_amt: of items to give
        :param max_amt: of items to give
        :return: a new instance of the Resource class
        """
        # get a random resource from our json data
        resource = get_random_resource()
        amount = random.randint(min_amt, max_amt)
        return Resource(name=resource['name'],
                        gives_item=resource['item'],
                        seconds_to_one_item=resource['time'],
                        max_item_amount=amount,
                        item_amount=amount,
                        on_island=island)

    async def harvest(self, amount):
        """ Remove the amount of items within this resource,
        then wait until the player has 'harvested' the items.

        :param amount: of items to harvest
        :return: an ItemStack with the harvested item and amount
        """
        self.item_amount -= amount
        await asyncio.sleep(amount * self.seconds_to_one_item)
        return ItemStack(item=self.gives_item, amount=amount)


def get_random_resource():
    """ Get a random resource from the cached json data

    :return: a dict of the resource
    """
    resource_data = Cache.get_from_json('data/resources.json')
    return random.choice(resource_data)