from discord.ext import commands

from ui.reaction import Reaction
from ui.reaction_menu import ReactionMenu


class TestCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hi'])
    async def hello(self, context):
        """ Replies with a nice comment. """
        await context.message.channel.send(f'Hello {context.message.author.name}, you looking dashing today.')

    @commands.command()
    async def smile(self, context):
        """ Adds a smile reaction to your message. """
        await context.message.add_reaction('😊')

    @commands.command(aliases=['react'])
    async def reactions(self, context):
        """ Test out the reactions GUI. """
        reaction_message = ReactionMenu(self.bot, context.message.channel,
                                        ['Hello, continue?', 'Oh, sorry to hear that.', 'Thanks for understanding.'],
                                        [Reaction.DISMISS.value, Reaction.CONFIRM.value])
        await reaction_message.send()
        await reaction_message.wait_for_user_reaction(context.message.author)


def setup(bot):
    bot.add_cog(TestCog(bot))
