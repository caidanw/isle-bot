import asyncio

from discord.ext import commands

from src.utils.clock import server_clock
from src.utils.logger import log_command


class UtilCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sleep(self, context, amount: int = 10):
        """ Test command for asynchronous design to have bot wait while doing other things. """
        await context.send(f'Sleeping {amount}s')
        await asyncio.sleep(amount)
        await context.send('Finished sleeping')
        log_command(context.author, f'sleep {amount}', issued=False)

    @commands.command()
    async def clock(self, context):
        """ Displays the time where the bot is located. """
        await context.send(server_clock())


def setup(bot):
    bot.add_cog(UtilCog(bot))

