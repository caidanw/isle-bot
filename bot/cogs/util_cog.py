import asyncio

from discord.ext import commands

from utils.clock import server_clock
from utils.logger import log_command


class UtilCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def sleep(self, context, amount: int = 10):
        """ Test command for asynchronous design to have bot wait while doing other things. """
        await self.bot.say(f'Sleeping {amount}s')
        await asyncio.sleep(amount)
        await self.bot.say('Finished sleeping')
        log_command(context.message.author, f'sleep {amount}', issued=False)

    @commands.command(pass_context=True)
    async def clock(self):
        """ Displays the time where the bot is located. """
        await self.bot.say(server_clock())


def setup(bot):
    bot.add_cog(UtilCog(bot))

