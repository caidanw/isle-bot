import asyncio
from operator import attrgetter

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

            await self.bot.say(msg, delete_after=60)
            await asyncio.sleep(60)
            await self.bot.delete_message(context.message)

    @info.command(pass_context=True, aliases=['loc', 'island', 'isle'])
    async def location(self, context):
        player = Game.get_player(context.message.author)
        location = player.get_location

        msg = '```'
        msg += '\nLocation'
        msg += '\n--------'

        if location:
            msg += f'\nType  : {type(location).__name__}'
        if location.name:
            msg += f'\nName  : {location.name}'
        if location.owner:
            msg += f'\nOwner : {location.owner}'
        if location.size:
            msg += f'\nSize  : {location.size}'

        msg += '```'
        await self.bot.say(msg)  # should use 'delete_after=60' param eventually

    @info.command(pass_context=True, aliases=['res'])
    async def resource(self, context, name=None):
        island = Game.get_player(context.message.author).get_location

        if not isinstance(island, Island):
            return await self.bot.say('You are currently not on an island.')

        if not island.resources:
            return await self.bot.say('This island does not have any resources.')

        msg = '```'

        if name is None:
            if island.resources:
                header = '{} : Items'.format('Resource'.ljust(10))
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
                    msg += '\n\titem name : harvest time'
                    msg += '\n\t------------------------'
                    for item_name in res.gives_items:
                        item = Item[item_name]
                        msg += '\n\t{}: {}'.format(item.name.ljust(10), format_time(item.harvest_time()))
                    msg += '\n'

        if msg == '```':
            # there were no resources found
            msg = f'No resources found for "{name}"'
        else:
            msg += '\n```'

        await self.bot.say(msg)


def setup(bot):
    bot.add_cog(InfoCog(bot))
