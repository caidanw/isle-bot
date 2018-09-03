from discord.ext import commands
from discord.ext.commands import CommandNotFound

import settings
from game.game import Game
from game.objects.resource import Resource
from utils import logger
from utils.cache import Cache


class AdminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def logout(self, context):
        """ Command only available to developers.

        Have IsleBot logout and close all connections.
        """
        is_admin(context.author)

        logger.log('Logging out...')
        logger.write_logs(logout=True)
        await context.send('Logging out...')
        await self.bot.logout()

    @commands.group(hidden=True, aliases=['a'])
    async def add(self, context):
        """ Command only available to developers.

         Add a new object to the game without altering the database.
         """
        is_admin(context.author)

    @add.command(hidden=True, aliases=['res'])
    async def resource(self, context, name):
        """ Command only available to developers.

        Add a new resource to the island the player is currently on.
        """
        if not Resource.is_valid_type(name):
            return await context.send(f'"{name}" is not a valid resource type.')

        island = Game.get_player(context.author).get_location

        if island is None:
            return await context.send('You must be on an island to use this command.')

        res = Resource.random(island, name)
        await context.send(f'Added "{res.f_name}" to "{island.name}" of "{island.owner.name}"')


def is_admin(author):
    if author.id not in settings.DEVELOPER_IDS:
        raise CommandNotFound(f'User {author} does not have permissions to use this command.')


def setup(bot):
    bot.add_cog(AdminCog(bot))
