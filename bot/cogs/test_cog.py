from discord.ext import commands

from ui.reaction import Reaction
from ui.reaction_message import ReactionMessage


class TestCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['hi'])
    async def hello(self, context):
        """ Replies with a nice comment. """
        await self.bot.say('Hello {}, you looking dashing today.'.format(context.message.author.name))

    @commands.command(pass_context=True)
    async def smile(self, context):
        """ Adds a smile reaction to your message. """
        await self.bot.add_reaction(context.message, emoji='😊')

    @commands.command(pass_context=True, aliases=['react'])
    async def reactions(self, context):
        """ Test out the reactions GUI. """
        reaction_message = ReactionMessage(self.bot, context.message.channel,
                                           ['Hello, continue?', 'Oh, sorry to hear that.', 'Thanks for understanding.'],
                                           [Reaction.DISMISS.value, Reaction.CONFIRM.value])
        await reaction_message.send()
        await reaction_message.wait_for_user_reaction(context.message.author)


def setup(bot):
    bot.add_cog(TestCog(bot))
