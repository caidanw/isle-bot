import asyncio

from discord import Client

from src.game.enums.action import Action
from src.game.models import Resource, Player
from src.utils import logger

MINUTE = 60
HOUR = MINUTE * 60
DAY = HOUR * 24


def register_tasks(client: Client):
    background_tasks = [replenish_resources, set_players_action_idle]

    for task in background_tasks:
        client.loop.create_task(task(client))
        logger.log_world_task(task, 'registered')


async def replenish_resources(client: Client):
    await client.wait_until_ready()  # wait until the client is ready to go
    logger.log_world_task(replenish_resources, 'Starting...')

    while not client.is_closed():
        # replenish the items for all resources that aren't currently full
        query = Resource.update(material_amount=Resource.max_material_amount) \
                        .where(Resource.material_amount < Resource.max_material_amount)
        query.execute()

        logger.log_world_task(replenish_resources, 'Replenished all resources')

        # wait for the appropriate amount of time between replenishment
        await asyncio.sleep(HOUR)


async def set_players_action_idle(client: Client):
    await client.wait_until_ready()  # wait until the client is ready to go
    logger.log_world_task(set_players_action_idle, 'Starting...')

    query = Player.update(action=Action.IDLE.value).where(Player.action != Action.IDLE.value)
    query.execute()

    logger.log_world_task(set_players_action_idle, 'Set all player actions to IDLE')
