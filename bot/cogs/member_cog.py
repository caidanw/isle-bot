from discord.ext import commands

from game.game import Game
from game.island import Island
from utils.clock import format_time
from game.enums.action import Action


class MemberCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=['inv'])
    async def inventory(self, context):
        """ Display every item in your inventory.

        :return: a string of the player's inventory items
        """
        if context.invoked_subcommand is None:
            player = Game.get_player(context.message.author)
            await self.bot.say(player.inventory.to_message())

    @inventory.command(pass_context=True, aliases=['a'])
    async def all(self, context):
        player = Game.get_player(context.message.author)
        await self.bot.say(player.inventory.to_message(harvested=True, crafted=True))

    @inventory.command(pass_context=True, aliases=['h', 'harvest'])
    async def harvested(self, context):
        player = Game.get_player(context.message.author)
        await self.bot.say(player.inventory.to_message(harvested=True))

    @inventory.command(pass_context=True, aliases=['c', 'craft'])
    async def crafted(self, context):
        player = Game.get_player(context.message.author)
        await self.bot.say(player.inventory.to_message(crafted=True))

    @commands.command(pass_context=True)
    async def harvest(self, context, resource_name, desired_amount=5):
        """ Harvest items from the resource.

        :param resource_name: of the resource to find on the island
        :param desired_amount: the amount of items to gather"""
        player = Game.get_player(context.message.author)

        if not player.is_idle:
            return await self.bot.say('You can not do any more actions until you have finished '
                                      f'{Action(player.action)}.')

        at_guild = Game.get_guild(context.message.server)
        if at_guild and not at_guild.get_island(player.get_location.name):
            return await self.bot.say('You can not harvest here, you are currently not on this island.')

        island = player.get_location
        if not isinstance(island, Island):
            return await self.bot.say('You must be on an island to harvest resources.')

        resource = island.get_resource(resource_name)

        if isinstance(resource, str):
            # at this point the resource is an error message we need to give to the player
            return await self.bot.say(resource)

        if not resource:
            return await self.bot.say(f'The resource "{resource_name}" is not on the current island.')
        elif resource.item_amount < desired_amount:
            return await self.bot.say(f'The resource has {resource.item_amount} items left to harvest.')

        player_inv = player.inventory
        if not player_inv.validate_is_room(desired_amount):
            return await self.bot.say('You don"t have enough room in your inventory.')

        time_to_finish = format_time(resource.average_item_harvest_time * desired_amount)
        if '#' not in resource_name:
            resource_name = f'{resource.name}#{resource.number}'
        msg = await self.bot.say(f'Harvesting {desired_amount} items from {resource_name}, '
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
        await self.bot.edit_message(msg, finished_message)

    @commands.command(pass_context=True)
    async def travel(self, context, *destination):
        """ Travel to another island or guild. """
        if not destination:
            return await self.bot.say('You must enter a destination.')

        destination_name = " ".join(destination)

        guild = Game.search_guilds(destination_name)
        island = Game.search_islands(destination_name)

        if guild is None and island is None:
            return await self.bot.say('There are no guilds or islands under that name.')

        player = Game.get_player(context.message.author)

        if guild:
            if player.guild.id == guild.id:
                return await self.bot.say('You are already at this guild.')

            # TODO: add vehicle checking, but for now just return a generic string
            return await self.bot.say('You can not travel out of your guild, because you do not have any vehicles.')

        if island:
            if player.get_location.id == island.id:
                return await self.bot.say('You are already on this island.')

            if island not in player.guild.islands:
                return await self.bot.say('That island is not a part of this guild. '
                                          'You must first travel to that guild\'s location.')

            # TODO: confirm using reactions that the player wants to travel there

            player.set_location(island)
            await self.bot.say(f'You have traveled to the island {island.name}')


def setup(bot):
    bot.add_cog(MemberCog(bot))
