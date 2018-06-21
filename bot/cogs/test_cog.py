from discord.ext import commands


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


def setup(bot):
    bot.add_cog(TestCog(bot))
