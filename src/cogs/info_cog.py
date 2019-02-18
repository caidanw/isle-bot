import asyncio
from operator import attrgetter

import discord
from discord.abc import PrivateChannel
from discord.ext import commands
from discord.ext.commands.bot import _default_help_command

from src import settings
from src.cogs._abstract_cog import AbstractCog
from src.game.enums.reaction import Reaction
from src.game.game import Game
from src.utils import logger


class InfoCog(AbstractCog):
    @commands.command(name='help')
    async def _help(self, context, *extra_commands):
        """ Get this message from the bot, and add a mailbox emoji to your help command. """
        author = context.author
        channel = context.message.channel
        dm_channel = author.dm_channel
        message = context.message

        if dm_channel is None:
            dm_channel = await author.create_dm()

        # hacky way to force the help message into a dm instead of guild channel
        context.message.channel = dm_channel
        if len(extra_commands) != 0:
            await _default_help_command(context, *extra_commands)
        else:
            await _default_help_command(context)
        # undo the hacks
        context.message.channel = channel

        if context.guild:
            try:
                # try to add a :mailbox: reaction
                await message.add_reaction(Reaction.MAILBOX.value)
            except (discord.HTTPException, discord.Forbidden, discord.NotFound, discord.InvalidArgument) as e:
                # if the reaction failed, then send a basic message
                logger.log(f'Could not add :mailbox: reaction, {e}')
                await channel.send(f"Sent you a list of the commands, {author.name}")

    @commands.group()
    async def info(self, context):
        """ Display info about yourself. """
        if context.invoked_subcommand is None:
            player = Game.get_player(context.author)

            msg = '```'
            if player.union:
                msg += f'\nUNION  : {player.union.name}'
            else:
                msg += f'\nUNION  : NONE'

            if player.on_island:
                msg += f'\nISLAND : {player.on_island.name}'
            else:
                msg += f'\nISLAND : NONE'

            msg += f'\nACTION : {str(player.get_action)}'
            msg += '```'

            if not isinstance(context.channel, PrivateChannel):
                await context.send(msg, delete_after=settings.DEFAULT_DELETE_DELAY)
                # we can't delete the other user's direct message, so we save the sleep call
                await asyncio.sleep(60)
                # # delete the bot and user after a minute so chat doesn't get clogged
                await context.message.delete()
            else:
                await context.send(msg)

    @info.command(aliases=['self'])
    async def me(self, context):
        """ Display information about your current stats. """
        player = Game.get_player(context.author)
        stats = player.stats

        msg = '```'
        msg += f'\n{player.username}'
        msg += f'\n---------------'
        msg += f'\nVIGOR     : {str(stats.vigor).zfill(3)}'
        msg += f'\nSTRENGTH  : {str(stats.strength).zfill(3)}'
        msg += f'\nDEXTERITY : {str(stats.dexterity).zfill(3)}'
        msg += f'\nFORTITUDE : {str(stats.fortitude).zfill(3)}'
        msg += '```'

        await context.send(msg, delete_after=settings.DEFAULT_DELETE_DELAY)

    @info.command(aliases=['guild'])
    async def union(self, context):
        """ Display information about your union. """
        player = Game.get_player(context.author)
        union = player.union

        msg = '```'
        msg += '\nUNION'
        msg += '\n--------'
        if union:
            msg += f'\nID              : {union.guild_id}'
        if union.name:
            msg += f'\nNAME            : {union.name}'
        if union.created_at:
            msg += f'\nCREATED ON      : {union.created_at}'
        if union.max_islands:
            msg += f'\nMAX ISLANDS     : {union.max_islands}'
        if union.claimed_islands:
            msg += f'\nCLAIMED ISLANDS : {union.claimed_islands}'
        msg += '```'

        await context.send(msg, delete_after=settings.DEFAULT_DELETE_DELAY)

    @info.command(aliases=['loc', 'island', 'isle'])
    async def location(self, context):
        """ Display information about your location. """
        player = Game.get_player(context.author)
        location = player.get_location

        msg = '```'
        msg += '\nLOCATION'
        msg += '\n--------'
        if location:
            msg += f'\nTYPE  : {type(location).__name__}'
        if location.name:
            msg += f'\nNAME  : {location.name}'
        if location.owner:
            msg += f'\nOWNER : {location.owner.name}'
        if location.size:
            msg += f'\nSIZE  : {location.size}'
        msg += '```'

        await context.send(msg, delete_after=settings.DEFAULT_DELETE_DELAY)

    @info.command(aliases=['res', 'resource'])
    async def resources(self, context):
        """ Display information about the resources on the current island. """
        channel = context.message.channel
        island = Game.get_player(context.author).get_location

        if not isinstance(island, Island):
            return await channel.send('You are currently not on an island.')

        if not island.resources:
            return await channel.send('This island does not have any resources.')

        msg = '```'
        msg += f'ISLAND {island.union_number}'
        if island.resources:
            header = f'{"RESOURCE".ljust(10)} : AMT : MAX'
            msg += '\n' + header
            msg += '\n' + '-' * len(header)
            for resource in sorted(island.resources, key=attrgetter('name', 'number')):
                full_name = resource.name.title() + '#' + str(resource.number)
                material_amount = str(resource.material_amount).zfill(3)
                max_material_amount = str(resource.max_material_amount).zfill(3)

                msg += f'\n{full_name.ljust(10)} : {material_amount} : {max_material_amount}'
        msg += '\n```'

        await channel.send(msg, delete_after=settings.DEFAULT_DELETE_DELAY)


def setup(bot):
    bot.add_cog(InfoCog(bot))
