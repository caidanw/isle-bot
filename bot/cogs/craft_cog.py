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
        """ Craft a new item. """
        author = context.message.author
        inventory = Game.get_player(author).inventory

        recipe_name = '_'.join(item_to_craft)
        display_name = ' '.join(item_to_craft)

        if not Recipe[recipe_name]:
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

    @commands.group(pass_context=True)
    async def recipe(self, context, *item_name):
        """ Get the recipe of the desired craftable item. """
        if context.invoked_subcommand:
            # ignore everything in this function if there was a subcommand passed
            return

        if not item_name:
            return await self.bot.say('A recipe name is required.')

        recipe_name = '_'.join(item_name)
        display_name = ' '.join(item_name)

        if not Recipe[recipe_name]:
            return await self.bot.say(f'Could not find the recipe for "{display_name}".')

        recipe = Recipe[recipe_name]

        return await self.bot.say(recipe.to_string())

    @recipe.command()
    async def all(self):
        """ Get all of the recipes of the craftable items. """
        output = '```\n'
        for item in Recipe:
            name = item.name.replace('_', ' ')
            name = name.title()
            print(name)


def setup(bot):
    bot.add_cog(CraftCog(bot))
