import asyncio

from discord.ext import commands

from game.enums.craftable_item import CraftableItem
from game.enums.recipe import Recipe
from game.game import Game
from utils.clock import format_time


class CraftCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def craft(self, context, *item_to_craft):
        author = context.message.author
        inventory = Game.get_player(author).inventory

        recipe_name = '_'.join(item_to_craft)
        display_name = ' '.join(item_to_craft)

        if recipe_name not in Recipe:
            return await self.bot.say(f'Could not find the recipe for "{recipe_name}".')

        recipe = Recipe[recipe_name].needs_items()

        if not inventory.enough_to_craft(recipe):
            return await self.bot.say(f'You do not have enough harvested items to craft this item.')

        time_to_craft = sum([item.value * recipe.get(item) for item in recipe])
        message = await self.bot.say(f'Crafting {display_name}, time to craft {format_time(time_to_craft)}')
        await asyncio.sleep(time_to_craft)

        for item, amount in recipe.items():
            inventory.remove_item(item.name, amount)

        inventory.add_craftable(CraftableItem[recipe_name])
        await self.bot.edit_message(message, f'{author.mention} finished crafting {display_name}')


def setup(bot):
    bot.add_cog(CraftCog(bot))
