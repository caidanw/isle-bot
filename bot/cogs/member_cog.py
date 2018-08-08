from discord.abc import PrivateChannel
from discord.ext import commands

from game.game import Game
from game.inventory import Inventory
from game.island import Island
from game.player import Player
from utils.clock import format_time
from game.enums.action import Action


class MemberCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, context):
        """  """
        channel = context.message.channel
        author = context.message.author
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
                               inventory=Inventory.create())

        await channel.send(f'The machine has created {player.username} for {union.name}.')

    @commands.group(aliases=['inv'])
    async def inventory(self, context):
        """ Display every item in your inventory.

        :return: a string of the player's inventory items
        """
        if context.invoked_subcommand is None:
            player = Game.get_player(context.message.author)
            await context.message.channel.send(player.inventory.to_message())

    @inventory.command(aliases=['a'])
    async def all(self, context):
        player = Game.get_player(context.message.author)
        await context.message.channel.send(player.inventory.to_message(harvested=True, crafted=True))

    @inventory.command(aliases=['h', 'harvest'])
    async def harvested(self, context):
        player = Game.get_player(context.message.author)
        await context.message.channel.send(player.inventory.to_message(harvested=True))

    @inventory.command(aliases=['c', 'craft'])
    async def crafted(self, context):
        player = Game.get_player(context.message.author)
        await context.message.channel.send(player.inventory.to_message(crafted=True))

    @commands.command()
    async def harvest(self, context, resource_name, desired_amount=5):
        """ Harvest items from the resource.

        :param resource_name: of the resource to find on the island
        :param desired_amount: the amount of items to gather"""
        player = Game.get_player(context.message.author)
        channel = context.message.channel

        if not player.is_idle:
            return await channel.send('You can not do any more actions until you have finished '
                                                      f'{Action(player.action).name}.')

        at_union = Game.get_union(context.message.guild)
        if at_union and not at_union.get_island(player.get_location.name):
            return await channel.send('You can not harvest here, you are currently not on this island.')

        island = player.get_location
        if not isinstance(island, Island):
            return await channel.send('You must be on an island to harvest resources.')

        resource = island.get_resource(resource_name)

        if isinstance(resource, str):
            # at this point the resource is an error message we need to give to the player
            return await channel.send(resource)

        if not resource:
            return await channel.send(f'The resource "{resource_name}" is not on the current island.')
        elif resource.item_amount < desired_amount:
            return await channel.send(f'The resource has {resource.item_amount} items left to harvest.')

        player_inv = player.inventory
        if not player_inv.validate_is_room(desired_amount):
            return await channel.send('You don"t have enough room in your inventory.')

        time_to_finish = format_time(resource.average_item_harvest_time * desired_amount)
        if '#' not in resource_name:
            resource_name = f'{resource.name}#{resource.number}'
        msg = await channel.send(f'Harvesting {desired_amount} items from {resource_name}, '
                                 f'estimated time to finish {time_to_finish}')

        player.action = Action.harvesting.value
        player.save()

        harvested_items = await resource.harvest(desired_amount)
        for item_name, item_amt in harvested_items.items():
            player_inv.add_item(item=item_name, amount=item_amt)

        player.action = Action.idle.value
        player.save()

        finished_message = f'{context.message.author.mention} has finished harvesting.'
        finished_message += '\n```'
        for item_name, item_amt in harvested_items.items():
            finished_message += f'\n{item_name.ljust(8)} : {str(item_amt).zfill(3)}'
        finished_message += '\n```'
        await msg.edit(content=finished_message)

    @commands.command()
    async def travel(self, context, *destination):
        """ Travel to another island or union. """
        channel = context.message.channel

        if not destination:
            return await channel.send('You must enter a destination.')

        destination_name = " ".join(destination)

        union = Game.search_unions(destination_name)
        island = Game.search_islands(destination_name)

        if union is None and island is None:
            return await channel.send('There are no unions or islands under that name.')

        player = Game.get_player(context.message.author)

        if union:
            if player.union.id == union.id:
                return await channel.send('You are already at this union.')

            # TODO: add vehicle checking, but for now just return a generic string
            return await channel.send('You can not travel out of your union, because you do not have any vehicles.')

        if island:
            if player.get_location.id == island.id:
                return await channel.send('You are already on this island.')

            if island not in player.union.islands:
                return await channel.send('That island is not a part of this union. '
                                          'You must first travel to that union\'s location.')

            # TODO: confirm using reactions that the player wants to travel there

            player.set_location(island)
            await channel.send(f'You have traveled to the island {island.name}')


def setup(bot):
    bot.add_cog(MemberCog(bot))
