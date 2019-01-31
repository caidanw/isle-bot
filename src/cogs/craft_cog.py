import asyncio

from discord.ext import commands

from src import settings
from src.cogs.__abstract_cog import AbstractCog
from src.game.enums.recipe import Recipe
from src.game.game import Game
from src.game.items import items
from src.utils.clock import format_time


class CraftCog(AbstractCog):
    @commands.command()
    async def craft(self, context, *item_to_craft):
        """ Craft a new item from harvested materials. """
        if len(item_to_craft) == 0:
            return await context.send('You must enter a recipe name. Try "?help craft"')

        author = context.author
        inventory = Game.get_player(author).inventory

        recipe_name = '_'.join(item_to_craft).upper()
        display_name = ' '.join(item_to_craft)

        try:
            recipe = Recipe[recipe_name].needs_materials()
        except KeyError:
            await context.send(f'Could not find the recipe for "{display_name}".',
                               delete_after=settings.DEFAULT_DELETE_DELAY)
            await asyncio.sleep(settings.DEFAULT_DELETE_DELAY)
            return await context.message.delete()

        if not inventory.enough_to_craft(recipe):
            return await context.send(f'You do not have enough materials to craft this item.')

        time_to_craft = sum([items.get_by_name(item.name).harvest_time * recipe.get(item) for item in recipe])
        message = await context.send(f'Crafting {display_name}, time to finish {format_time(time_to_craft)}')
        await asyncio.sleep(time_to_craft)

        for item, amount in recipe.items():
            inventory.remove_material(item.name, amount)

        inventory.add_item(items.get_by_name(recipe_name))
        await message.edit(content=f'{author.mention} finished crafting {display_name}')

    @commands.command(aliases=['recipes'])
    async def recipe(self, context, *item_name):
        """ Get the recipe of the desired craftable item. """
        if len(item_name) == 0:
            message = self.list_recipes()  # return all recipes when in the even of an empty item_name
        else:
            input_name = ' '.join(item_name)

            try:
                recipe_name = '_'.join(item_name).upper()
                recipe = Recipe[recipe_name]

                message = recipe.to_extended_string()
            except KeyError:
                await context.send(f'Could not find the recipe for "{input_name}".',
                                   delete_after=settings.DEFAULT_DELETE_DELAY)
                await asyncio.sleep(settings.DEFAULT_DELETE_DELAY)
                return await context.message.delete()

        await context.send(message)

    @staticmethod
    def list_recipes():
        """ Get all of the recipes of the craftable items. """
        output = '```\n'
        output += 'RECIPE LIST'

        for item in Recipe:
            try:
                recipe = item.to_short_string()
            except Exception:
                recipe = f'Unavailable'
            output += f'\n\t{item.name.replace("_", " ")} : {recipe}'  # format item name and recipe string

        output += '\n```'
        return output


def setup(bot):
    bot.add_cog(CraftCog(bot))
