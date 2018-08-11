import asyncio

from discord.ext import commands

from game.enums.craftable_item import CraftableItem
from game.enums.recipe import Recipe
from game.game import Game
from game.items import items
from utils.clock import format_time


class CraftCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def craft(self, context, *item_to_craft):
        """ Craft a new item. """
        channel = context.message.channel

        if len(item_to_craft) == 0:
            return await channel.send('You must enter a recipe name. Try "?help craft"')

        author = context.message.author
        inventory = Game.get_player(author).inventory

        recipe_name = '_'.join(item_to_craft).upper()
        display_name = ' '.join(item_to_craft)

        try:
            recipe = Recipe[recipe_name].needs_items()
        except KeyError:
            return await channel.send(f'Could not find the recipe for "{recipe_name}".')

        if not inventory.enough_to_craft(recipe):
            return await channel.send(f'You do not have enough harvested items to craft this item.')

        time_to_craft = sum([items.get_by_name(item.name).harvest_time * recipe.get(item) for item in recipe])
        message = await channel.send(f'Crafting {display_name}, time to craft {format_time(time_to_craft)}')
        await asyncio.sleep(time_to_craft)

        for item, amount in recipe.items():
            inventory.remove_item(item.name, amount)

        inventory.add_craftable(CraftableItem[recipe_name])
        await message.edit(content=f'{author.mention} finished crafting {display_name}')

    @commands.group()
    async def recipe(self, context, *item_name):
        """ Get the recipe of the desired craftable item. """
        channel = context.message.channel

        for name in item_name:
            command = self.bot.get_command('recipe').get_command(name)
            if command:
                return await command.invoke(context)

        if not item_name:
            return await channel.send('A recipe name is required. Try "?help recipe"')

        recipe_name = '_'.join(item_name).upper()
        input_name = ' '.join(item_name)

        try:
            recipe = Recipe[recipe_name]
        except KeyError:
            return await channel.send(f'Could not find the recipe for "{input_name}".')

        await channel.send(recipe.to_extended_string())

    @recipe.command(aliases=['all'])
    async def list(self, context):
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

        await context.message.channel.send(output)


def setup(bot):
    bot.add_cog(CraftCog(bot))
