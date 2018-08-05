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
        if len(item_to_craft) == 0:
            return await self.bot.say('You must enter a recipe name. Try "?help craft"')

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
        subcommands = self.bot.commands.get('recipe').commands.keys()
        for name in item_name:
            # ignore everything in this function if there was a subcommand passed
            if name in subcommands:
                subcommand = self.bot.commands.get('recipe').commands.get(name)
                return await subcommand.invoke(context)

        if not item_name:
            return await self.bot.say('A recipe name is required. Try "?help recipe"')

        recipe_name = '_'.join(item_name).upper()
        input_name = ' '.join(item_name)

        try:
            recipe = Recipe[recipe_name]
        except Exception:
            return await self.bot.say(f'Could not find the recipe for "{input_name}".')

        await self.bot.say(recipe.to_extended_string())

    @recipe.command(aliases=['all'])
    async def list(self):
        """ Get all of the recipes of the craftable items. """
        output = 'Recipe List:'
        output += '```\n'
        for item in Recipe:
            name = item.name.replace('_', ' ')

            try:
                recipe = item.to_short_string()
            except Exception:
                recipe = 'Unavailable'

            output += f'\n{name} : {recipe}'
        output += '\n```'

        await self.bot.say(output)


def setup(bot):
    bot.add_cog(CraftCog(bot))
