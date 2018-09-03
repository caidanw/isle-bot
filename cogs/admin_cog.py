from discord.ext import commands
from discord.ext.commands import CommandNotFound

import settings
from utils import logger


class AdminCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def logout(self, context):
        is_admin(context.author)

        logger.log('Logging out...')
        logger.write_logs(logout=True)
        await context.send('Logging out...')
        await self.bot.logout()


def is_admin(author):
    if author.id not in settings.DEVELOPER_IDS:
        raise CommandNotFound(f'User {author} does not have permissions to use this command.')


def setup(bot):
    bot.add_cog(AdminCog(bot))
