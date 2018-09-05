import asyncio
import random
import re

from discord.abc import PrivateChannel
from discord.ext import commands

import settings
from game.game import Game
from game.items import items
from game.objects.inventory import Inventory
from game.objects.island import Island
from game.objects.player import Player
from game.objects.player_stat import PlayerStat
from ui.reaction import Reaction
from utils.clock import format_time
from game.enums.action import Action


class MemberCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, context):
        """ Be born under a new union.

         The union you choose to be born at will stay with you and be visible to all players until death.
         """
        channel = context.message.channel
        author = context.author
        union = context.message.guild

        if Game.get_player(author) is not None:
            return await channel.send('You can not be recreated, please die first.')

        if isinstance(channel, PrivateChannel):
            return await author.create_dm('You can not be created on thin air. Only out of thin air. '
                                          'Please ask one of the islands machines. (enter command in guild chat)')
        else:
            union = Game.get_union(union)

        player = Player.create(username=author.name,
                               uuid=author.id,
                               union=union,
                               on_island=union.get_island(),
                               inventory=Inventory.create(),
                               stats=PlayerStat.create())

        await channel.send(f'The machine has created {player.username} for {union.name}.')

        dm_channel = await author.create_dm()

        welcome_msg_part_one = f"""Welcome {player.username}, here is the rundown of the game.
        
        The bot responds to a few discriminators for commands, all discriminators are (`?` `!` `.` `~`) you can use these like so, eg. `?help` `!help` `.help` `~help` and they will all mean the same to the bot.
        This was done with making it easier for you to use in mind, depending on which platform you keyboard has, you can choose your most comfortable fit of discriminator.
        If you are struggling with a command, try using `?help command_name` and it will give you a message with command usage and what it does.

        Each discord server is created into a union, every union is in the same game world. You can travel between unions and trade with other players (not currently supported).
        Each union starts with one floating island, that island has resources (you can find an islands resources by using `?info resource` or `?info res`).
        You can harvest materials from resources with ?harvest resource amount eg. `?harvest forest 20.` You can not choose the exact material you harvest, as they are given out randomly.
        You can craft new items using ?craft item name. To find a list of recipes do `?recipe all` or to find a specific recipe do `?recipe item name`.
        You can also eat materials that you harvest, although most materials can not be eaten, try finding out what you can eat as you may be surprised. Use `?eat material`.
        """

        welcome_msg_part_two = """Another note on the `?info` command, if you do `?help info` you can see what information is available.
        Using `?info me` will show you all of your stats. You can level up stats by eating certain materials.
        Higher level stats allow you to do more damage, block more damage, or have more starting health.
        
        You can fight other players using ?fight player name (player name is case sensitive). For example, `?fight mildmelon` is not the same as `?fight MildMelon`.
        When in combat, you are presented with a menu of actions, start from left to right are the actions you can choose.
        Attack: :crossed_swords: | Defend: :shield: | Use Item: :package: | Pass Turn: :no_entry_sign: | Surrender: :flag_white:
        Currently, using an item during combat is not implemented, and remember... Don't pass your turn, unless you want to die.

        You may also do a private message with IsleBot if you don't want to clog up the general chat or you want to do an action privately.
        Good luck, have fun, and message `mildmelon#5380` or anyone on the `Arcane Blood` server if you have any questions.
        """

        await dm_channel.send(welcome_msg_part_one)
        await dm_channel.send(welcome_msg_part_two)

    @commands.command(aliases=['e', 'consume'])
    async def eat(self, context, *item_name):
        """ Eat an item or material.

         This can be used to restore health, or increase a stat level.
         """
        channel = context.message.channel
        author = context.author

        if len(item_name) == 0:
            return await channel.send('An item name is required. Try "?help eat"')

        player = Game.get_player(context.author)

        if not player.is_idle:
            return await channel.send(f'You can not do anymore actions until you have finished {player.f_action}')

        input_name = ' '.join(item_name)
        item_name = '_'.join(item_name).upper()
        item = items.get_by_name(item_name)

        if item is None:
            return await channel.send(f'The item "{input_name}" does not exist.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        if not player.inventory.has_material(item_name):
            return await channel.send(f'You do not have the item "{input_name}".',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        if not item.can_consume:
            return await channel.send(f'You can not consume "{item.name.lower()}".',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)
        else:
            player.set_action(Action.EATING)
            succeeded = await item.consume(self.bot, author)
            if succeeded:
                player.inventory.remove_material(item.name)
            player.set_action(Action.IDLE)

    @commands.group(aliases=['inv'])
    async def inventory(self, context):
        """ Display every item in your inventory.

        :return: a string of the player's inventory
        """
        if context.invoked_subcommand is None:
            player = Game.get_player(context.author)
            await context.send(player.inventory.to_message(harvested=True, crafted=True))

    @inventory.command(aliases=['m'])
    async def max(self, context):
        player = Game.get_player(context.author)
        await context.send(player.inventory.to_message())

    @inventory.command(aliases=['h', 'harvest'])
    async def harvested(self, context):
        player = Game.get_player(context.author)
        await context.send(player.inventory.to_message(harvested=True))

    @inventory.command(aliases=['c', 'craft'])
    async def crafted(self, context):
        player = Game.get_player(context.author)
        await context.send(player.inventory.to_message(crafted=True))

    @commands.command(aliases=['h', 'harv'])
    async def harvest(self, context, resource_name, desired_amount=5):
        """ Harvest materials from a resource.

        :param resource_name: of the resource to find on the island
        :param desired_amount: the amount of materials to harvest
        """
        player = Game.get_player(context.author)
        channel = context.message.channel

        if not player.is_idle:
            return await channel.send(f'You can not do any more actions until you have finished {player.f_action}')

        if not isinstance(player.get_location, Island):
            return await channel.send('You can not harvest here, you are currently not on an island.')

        island = player.get_location
        if not isinstance(island, Island):
            return await channel.send('You must be on an island to harvest resources.')

        resource = island.get_resource(resource_name)

        if isinstance(resource, str):
            # at this point the resource is an error message we need to give to the player
            return await channel.send(resource)

        if not resource:
            return await channel.send(f'The resource "{resource_name}" is not on the current island.')
        elif resource.material_amount < desired_amount:
            return await channel.send(f'The resource has {resource.material_amount} materials left to harvest.')

        player_inv = player.inventory
        if not player_inv.validate_is_room(desired_amount):
            return await channel.send('You don\'t have enough room in your inventory.')

        time_to_finish = format_time(resource.average_harvest_time * desired_amount)
        if '#' not in resource_name:
            resource_name = f'{resource.name}#{resource.number}'
        msg = await channel.send(f'Harvesting {desired_amount} materials from {resource_name}, '
                                 f'estimated time to finish {time_to_finish}')

        player.set_action(Action.HARVESTING)

        harvested_materials = await resource.harvest(desired_amount)
        for name, amt in harvested_materials.items():
            player_inv.add_material(material=name, amount=amt)

        player.set_action(Action.IDLE)

        finished_message = f'{context.author.mention} has finished harvesting materials.'
        finished_message += '\n```'
        for name, amt in harvested_materials.items():
            finished_message += f'\n{name.ljust(8)} : {str(amt).zfill(3)}'
        finished_message += '\n```'

        await msg.edit(content=finished_message)

    @commands.command(aliases=['t', 'trav'])
    async def travel(self, context, *destination):
        """ Travel to another island or union. """
        channel = context.message.channel
        guild = context.message.guild
        author = context.author

        if not destination:
            return await channel.send('You must enter a destination.')

        destination_name = " ".join(destination)
        island_number = re.search('island#(\d+)', destination_name).group(1)
        island_number = int(island_number)

        union = Game.search_unions(destination_name)

        local_union = None
        if union is None:
            local_union = Game.search_unions_by_guild_id(guild.id)
            island = Game.search_islands_by_number(local_union, island_number)
        else:
            island = Game.search_islands_by_number(union, island_number)

        if union is None and island is None:
            return await channel.send('There are no unions or islands under that name.')

        player = Game.get_player(author)

        if union:
            if player.union.id == union.id:
                return await channel.send('You are already at this union.')

            # TODO: add vehicle checking, but for now just return a generic string
            return await channel.send('You can not travel out of your union, because you do not have any vehicles.')

        if island:
            if player.get_location.id == island.id:
                return await channel.send('You are already on this island.')

            if island not in local_union.islands:
                return await channel.send('That island is not a part of this union. '
                                          'You must first travel to that union\'s location.')

            # TODO: confirm using reactions that the player wants to travel there

            # TODO: estimate the eta, based on distance
            message = await channel.send(f'You start heading towards {island.name}. ETA: 02s')

            player.set_action(Action.TRAVELING)
            await asyncio.sleep(random.randint(1, 3))
            player.set_action(Action.IDLE)

            player.set_location(island)
            await message.edit(content=f'{author.mention} has arrived at {island.name}')


def setup(bot):
    bot.add_cog(MemberCog(bot))
