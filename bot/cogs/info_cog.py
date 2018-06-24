import asyncio

from discord.ext import commands

from game.enums.item import Item
from game.game import Game
from game.enums.action import Action
from game.island import Island
from utils.clock import format_time


class InfoCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def info(self, context):
        """ Display info about yourself. """
        if context.invoked_subcommand is None:
            player = Game.get_player(context.message.author)
            msg = '```'

            if player.guild:
                msg += f'\nGuild  : {player.guild.name}'
            else:
                msg += f'\nGuild  : None'

            if player.on_island:
                msg += f'\nIsland : {player.on_island.name}'
            else:
                msg += f'\nIsland : None'

            msg += f'\nAction : {Action(player.action)}'
            msg += '```'

            await self.bot.say(msg, delete_after=10)
            await asyncio.sleep(10)
            await self.bot.delete_message(context.message)

    @info.command(pass_context=True, aliases=['loc', 'island', 'isle'])
    async def location(self, context):
        player = Game.get_player(context.message.author)
        location = player.get_location

        msg = '```'

        if location:
            msg += f'\nArea     : {type(location).__name__}'
        if location.name:
            msg += f'\nLocation : {location.name}'
        if location.owner:
            msg += f'\nOwner    : {location.owner}'
        if location.size:
            msg += f'\nSize     : {location.size}'
        if location.resources:
            msg += '\nResources:'
            for resource in location.resources:
                msg += f'\n\t{resource.name} : {resource.item_amount}'

        msg += '```'
        await self.bot.say(msg, delete_after=60)

    @info.command(pass_context=True, aliases=['res'])
    async def resource(self, context):
        island = Game.get_player(context.message.author).get_location

        if not isinstance(island, Island):
            return await self.bot.say('You are currently not on an island.')

        if not island.resources:
            return await self.bot.say('This island does not have any resources.')

        msg = '```'

        for res in island.resources:
            msg += f'\n{res.name} has {str(res.item_amount).zfill(3)} items left'
            msg += '\n\titem name : harvest time'
            msg += '\n\t------------------------'
            for item_name in res.gives_items:
                item = Item[item_name]
                msg += '\n\t{}: {}'.format(item.name.ljust(10), format_time(item.harvest_time()))

        msg += '\n```'
        await self.bot.say(msg)


def setup(bot):
    bot.add_cog(InfoCog(bot))
