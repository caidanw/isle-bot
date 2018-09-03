import asyncio

from discord import Client

from game.enums.action import Action
from game.objects.player import Player
from game.objects.resource import Resource
from utils import logger

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24


def register_tasks(client: Client):
    background_tasks = [replenish_resources, set_players_action_idle]

    for task in background_tasks:
        logger.log(f'Registering world task {task.__name__}')
        client.loop.create_task(task(client))


async def replenish_resources(client: Client):
    await client.wait_until_ready()  # wait until the client is ready to go
    logger.log(f'Running world task {replenish_resources.__name__}')

    while not client.is_closed():
        # replenish the items for all resources that aren't currently full
        query = Resource.update(material_amount=Resource.max_material_amount) \
                        .where(Resource.material_amount < Resource.max_material_amount)
        query.execute()

        logger.log('\tReplenished all resources')

        # wait for the appropriate amount of time between replenishment
        await asyncio.sleep(HOUR)


async def set_players_action_idle(client: Client):
    await client.wait_until_ready()  # wait until the client is ready to go
    logger.log(f'Running world task {set_players_action_idle.__name__}')

    query = Player.update(action=Action.IDLE.value).where(Player.action != Action.IDLE.value)
    query.execute()

    logger.log('\tSet all player actions to IDLE')
