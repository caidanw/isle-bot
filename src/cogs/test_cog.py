from discord.ext import commands

from src.cogs._abstract_cog import AbstractCog
from src.game.enums.reaction import Reaction
from src.ui.menus.abstract_menu import AbstractMenu


class TestCog(AbstractCog):
    @commands.command(aliases=['hi'])
    async def hello(self, context):
        """ Replies with a nice comment. """
        await context.send(f'Hello {context.author.name}, you looking dashing today.')

    @commands.command()
    async def smile(self, context):
        """ Adds a smile reaction to your message. """
        await context.message.add_reaction('😊')

    @commands.command(aliases=['react'])
    async def reactions(self, context):
        """ Test out the reactions GUI. """
        reaction_message = AbstractMenu(self.bot, context.message.channel,
                                        ['Hello, continue?', 'Oh, sorry to hear that.', 'Thanks for understanding.'],
                                        [Reaction.DISMISS.value, Reaction.CONFIRM.value])
        await reaction_message.send()
        await reaction_message.wait_for_user_reaction(context.author)


def setup(bot):
    bot.add_cog(TestCog(bot))
