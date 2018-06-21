from discord.ext import commands

from bot.isle_bot import game
from utils.clock import format_time
from utils.enums import Action


class MemberCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, context):
        """ Display info about yourself. """
        player = game.get_player(context.message.author)
        if player is None or player.guild is None or player.on_island.name is None:
            msg = 'You what mate!?'
        else:
            msg = '```\nGuild : {}\nIsland: {}\nAction: {}\n```'.format(player.guild.name,
                                                                        player.on_island.name,
                                                                        player.action)
        await self.bot.say(msg)

    @commands.command(pass_context=True, aliases=['inv'])
    async def inventory(self, context):
        """ Display every item in your inventory. """
        player = game.get_player(context.message.author)
        await self.bot.say(player.inventory)

    @commands.command(pass_context=True)
    async def harvest(self, context, resource_name, desired_amount=5):
        """ Harvest items from the resource. """
        player = game.get_player(context.message.author)

        if not player.is_idle:
            return await self.bot.say('You can not do any more actions until you have finished {}.'.format(player.action))

        resource = player.on_island.get_resource(resource_name)
        if not resource:
            return await self.bot.say('The resource \'{}\' is not on the current island.'.format(resource_name))
        elif resource.amount < desired_amount:
            return await self.bot.say('The resource only has {} items left to harvest.'.format(resource.amount))

        player_inv = player.inventory
        if not player_inv.validate_stack(resource.gives_item, desired_amount):
            await self.bot.say('You don\'t have enough room in your inventory.')
            return

        time_to_finish = format_time(resource.seconds_to_one_item * desired_amount)
        msg = await self.bot.say('Harvesting from {}, time to finish {}'.format(resource_name, time_to_finish))
        player.action = Action.harvesting

        item_stack = await resource.harvest(desired_amount)
        player_inv.add_item(item_stack.item, item_stack.amount)

        player.action = Action.idle
        await self.bot.edit_message(msg, '{} harvested {} {}'.format(player.user.mention,
                                                                     item_stack.amount,
                                                                     item_stack.item))

        game.save()


def setup(bot):
    bot.add_cog(MemberCog(bot))
