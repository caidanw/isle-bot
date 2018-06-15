import random
import asyncio

from game.item import ItemStack
from utils.cache import Cache


class Resource:
    def __init__(self, name, gives_item, seconds_to_one_item, max_item_amount):
        self.name = name
        self.gives_item = gives_item
        self.seconds_to_one_item = seconds_to_one_item
        self.max_item_amount = max_item_amount
        self.amount = max_item_amount

    @classmethod
    def random(cls, min_amt, max_amt):
        # get a random resource from our json data
        resource = get_random_resource()
        return Resource(name=resource['name'],
                        gives_item=resource['item'],
                        seconds_to_one_item=resource['time'],
                        max_item_amount=random.randint(min_amt, max_amt))

    async def harvest(self, amount):
        await asyncio.sleep(amount * self.seconds_to_one_item)
        return ItemStack(item=self.gives_item, amount=amount)


def get_random_resource():
    """ Get a random resource from the cached json data

    :return: a dict of the resource
    """
    resource_data = Cache.get_from_json('data/resources.json')
    return resource_data[random.randint(0, len(resource_data)-1)]
