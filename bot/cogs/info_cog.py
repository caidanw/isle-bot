import asyncio
from operator import attrgetter

import discord
from discord.abc import PrivateChannel
from discord.ext import commands
from discord.ext.commands.bot import _default_help_command

from game.game import Game
from game.enums.action import Action
from game.island import Island
from game.items import items
from ui.reaction import Reaction
from utils import logger
from utils.clock import format_time


class InfoCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def _help(self, context, *extra_commands):
        author = context.message.author
        channel = context.message.channel
        dm_channel = author.dm_channel
        message = context.message

        if not dm_channel:
            dm_channel = await author.create_dm()

        # hacky way to force the standard help into a dm
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
            channel = context.message.channel
            player = Game.get_player(context.message.author)

            msg = '```'

            if player.union:
                msg += f'\nUNION  : {player.union.name}'
            else:
                msg += f'\nUNION  : NONE'

            if player.on_island:
                msg += f'\nISLAND : {player.on_island.name}'
            else:
                msg += f'\nISLAND : NONE'

            msg += f'\nACTION : {Action(player.action).name}'
            msg += '```'

            to_delete = await channel.send(msg)

            if not isinstance(channel, PrivateChannel):
                # we can't delete the other user's direct message, so we save the sleep call
                await asyncio.sleep(60)
                # # delete the bot and user after a minute so chat doesn't get clogged
                await context.message.delete()
                await to_delete.delete()

    @info.command(aliases=['loc', 'island', 'isle'])
    async def location(self, context):
        player = Game.get_player(context.message.author)
        location = player.get_location

        msg = '```'
        msg += '\nLOCATION'
        msg += '\n--------'

        if location:
            msg += f'\nTYPE  : {type(location).__name__}'
        if location.name:
            msg += f'\nName  : {location.name}'
        if location.owner:
            msg += f'\nOWNER : {location.owner}'
        if location.size:
            msg += f'\nSIZE  : {location.size}'

        msg += '```'
        await context.message.channel.send(msg)  # should use 'delete_after=60' param eventually

    @info.command(aliases=['res'])
    async def resources(self, context, name=None):
        channel = context.message.channel
        island = Game.get_player(context.message.author).get_location

        if not isinstance(island, Island):
            return await channel.send('You are currently not on an island.')

        if not island.resources:
            return await channel.send('This island does not have any resources.')

        msg = '```'

        if name is None:
            if island.resources:
                header = f'{"RESOURCE".ljust(10)} : ITEMS'
                msg += '\n' + header
                msg += '\n' + '-' * len(header)
                for resource in sorted(island.resources, key=attrgetter('name', 'number')):
                    full_name = resource.name.title() + '#' + str(resource.number)
                    item_amount = str(resource.item_amount).zfill(3)
                    msg += f'\n{full_name.ljust(10)} : {item_amount}'
        else:
            for res in island.resources:
                if '#' in name:
                    split_name = name.split('#')
                    name = split_name[0]
                    number = split_name[1]
                    if res.number != number:
                        continue

                if res.name == name:
                    msg += f'\n{res.name.title()}#{res.number} has {str(res.item_amount).zfill(3)} items left'
                    msg += '\n\tITEM NAME : HARVEST TIME'
                    msg += '\n\t------------------------'
                    for item_name in res.gives_items:
                        item = items.get_by_name(item_name)
                        msg += f'\n\t{item.name.ljust(10)}: {format_time(item.harvest_time())}'
                    msg += '\n'

        if msg == '```':
            # there were no resources found
            msg = f'No resources found for "{name}"'
        else:
            msg += '\n```'

        await channel.send(msg)


def setup(bot):
    bot.add_cog(InfoCog(bot))
