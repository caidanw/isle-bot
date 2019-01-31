from discord.ext import commands
from discord.ext.commands import CommandNotFound

from src import settings
from src.cogs.__abstract_cog import AbstractCog
from src.game.enums.action import Action
from src.game.game import Game
from src.game.models import Resource, Island
from src.utils import logger


class AdminCog(AbstractCog):
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
            return await context.send(f'"{name}" is not a valid resource type.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        island = Game.get_player(context.author).get_location

        if island is None:
            return await context.send('You must be on an island to use this command.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        res = Resource.random(island, name)
        await context.send(f'Added "{res.f_name}" to "{island.name}" of "{island.owner.name}".',
                           delete_after=settings.DEFAULT_DELETE_DELAY)

    @add.command(hidden=True, aliases=['isl'])
    async def island(self, context, *guild_name):
        """ Command only available to developers.

        Add a new island to the current guild_name.
        """
        if not guild_name:
            union = Game.get_union(context.guild)
        else:
            guild_name = ' '.join(guild_name)
            union = Game.search_unions(guild_name)
            if union is None:
                return await context.send(f'Could not find any union under the name "{guild_name}"',
                                          delete_after=settings.DEFAULT_DELETE_DELAY)

        island = Island.create()

        union.max_islands += 1
        if union.claim_island(island):
            return await context.send(f'"{union.name}" claimed {island.name}',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)
        await context.send(f'Failed to claim {island.name} for "{union.name}"',
                           delete_after=settings.DEFAULT_DELETE_DELAY)

    @commands.group(hidden=True, aliases=['p'])
    async def player(self, context):
        """ Command only available to developers.

        Alter player attributes.
        """
        is_admin(context.author)

    @player.command(hiddent=True, aliases=['inv'])
    async def inventory(self, context, name, amount):
        """ Command only available to developers.

        Set the player's max inventory amount.
        """
        try:
            amount = int(amount)
        except ValueError:
            return await context.send(f'Inventory amount must be an integer, you entered "{amount}".',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        if amount < 1:
            return await context.send('Inventory amount can not be less than 1.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        player = Game.get_player_by_name(name)
        if player is None:
            return await context.send(f'Player "{name}" does not exist.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        inventory = player.inventory
        inventory.max_materials = amount
        inventory.save()

        await context.send(f'Set max materials for "{player.username}" to {inventory.max_materials}.',
                           delete_after=settings.DEFAULT_DELETE_DELAY)

    @player.command(hiddent=True, aliases=['act'])
    async def action(self, context, name, action):
        """ Command only available to developers.

        Set the player's current action.
        """
        try:
            action = Action[action.upper()]
        except KeyError:
            return await context.send(f'Action "{action}" does not exist.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        player = Game.get_player_by_name(name)
        if player is None:
            return await context.send(f'Player "{name}" does not exist.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        player.set_action(action)
        await context.send(f'Set action for "{player.username}" to {player.f_action}.',
                           delete_after=settings.DEFAULT_DELETE_DELAY)

    @player.command(hiddent=True)
    async def stat(self, context, name, stat, amount):
        """ Command only available to developers.

        Add amount to the player's stat.
        """
        stat = stat.lower()
        if stat not in ['vigor', 'strength', 'dexterity', 'fortitude']:
            return await context.send(f'Stat "{stat}" does not exist.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        player = Game.get_player_by_name(name)
        if player is None:
            return await context.send(f'Player "{name}" does not exist.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)
        try:
            amount = int(amount)
        except ValueError:
            return await context.send(f'Increase amount must be an integer, you entered "{amount}".',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        if amount < 1:
            return await context.send('Increase amount can not be less than 1.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        stats = player.stats
        if stat == 'vigor':
            stats.increase_vigor(amount)
        elif stat == 'strength':
            stats.increase_strength(amount)
        elif stat == 'dexterity':
            stats.increase_dexterity(amount)
        elif stat == 'fortitude':
            stats.increase_fortitude(amount)

        await context.send(f'Increased {stat} for "{player.username}" by {amount}.',
                           delete_after=settings.DEFAULT_DELETE_DELAY)


def is_admin(author):
    if author.id not in settings.DEVELOPER_IDS:
        raise CommandNotFound(f'User {author} does not have permissions to use this command.')


def setup(bot):
    bot.add_cog(AdminCog(bot))
