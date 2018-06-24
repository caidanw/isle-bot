from discord.ext import commands

from game.game import Game
from game.island import Island
from utils.clock import format_time
from game.enums.action import Action


class MemberCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['inv'])
    async def inventory(self, context):
        """ Display every item in your inventory.

        :return: a string of the player's inventory items
        """
        player = Game.get_player(context.message.author)
        await self.bot.say(player.inventory.to_message())

    @commands.command(pass_context=True)
    async def harvest(self, context, resource_name, desired_amount=5):
        """ Harvest items from the resource.

        :param resource_name: of the resource to find on the island
        :param desired_amount: the amount of items to gather"""
        player = Game.get_player(context.message.author)

        if not player.is_idle:
            return await self.bot.say(f'You can not do any more actions until you have finished {Action(player.action)}.')

        at_guild = Game.get_guild(context.message.server)
        if at_guild and not at_guild.get_island(player.get_location.name):
            return await self.bot.say('You can not harvest here, you are currently not on this island.')

        island = player.get_location
        if not isinstance(island, Island):
            return await self.bot.say('You must be on an island to harvest resources.')

        resource = island.get_resource(resource_name)
        if not resource:
            return await self.bot.say('The resource \'{}\' is not on the current island.'.format(resource_name))
        elif resource.item_amount < desired_amount:
            return await self.bot.say('The resource only has {} items left to harvest.'.format(resource.item_amount))

        player_inv = player.inventory
        if not player_inv.validate_is_room(desired_amount):
            return await self.bot.say('You don\'t have enough room in your inventory.')

        time_to_finish = format_time(resource.average_item_harvest_time * desired_amount)
        msg = await self.bot.say('Harvesting {} items from {}, estimated time to finish {}'.format(desired_amount,
                                                                                                   resource_name,
                                                                                                   time_to_finish))
        player.action = Action.harvesting.value
        player.save()

        harvested_items = await resource.harvest(desired_amount)
        for item_name, item_amt in harvested_items.items():
            player_inv.add_item(item=item_name, amount=item_amt)

        player.action = Action.idle.value
        player.save()

        finished_message = '{} has finished harvesting.'.format(context.message.author.mention)
        finished_message += '\n```'
        for item_name, item_amt in harvested_items.items():
            finished_message += '\n{} : {}'.format(item_name.ljust(8), str(item_amt).zfill(3))
        finished_message += '\n```'
        await self.bot.edit_message(msg, finished_message)


def setup(bot):
    bot.add_cog(MemberCog(bot))
