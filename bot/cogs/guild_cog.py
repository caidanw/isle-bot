from discord.ext import commands

from utils.check import is_private

from game.player import Player
from bot.isle_bot import game


class GuildCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,
                      description='Join the guild of the current discord server, '
                                  + 'if a name is passed then join that guild instead.')
    async def join(self, context, guild_name=None):
        """ Join a guild. """
        private_channel = is_private(context.message)
        if private_channel and guild_name is None:
            return await self.bot.say('You must enter the name of the guild you would like to join.')

        if private_channel or guild_name is not None:
            guild = game.search_guilds(guild_name)
        else:
            guild = game.get_guild(context.message.server)

        if guild is None:
            return await self.bot.say('That guild does not exist or is not registered.')

        player = game.get_player(context.message.author)
        if player and player.guild is not None:
            return await self.bot.say('You already belong to the guild {}'.format(player.guild.name))
        elif player is None:
            player = Player(game, context.message.author, guild)

        game.create_player(player)
        message = player.join_guild(guild)
        await self.bot.say(message)

        game.save()

    @commands.command(pass_context=True)
    async def leave(self, context):
        """ Leave your current guild. """
        player = game.get_player(context.message.author)

        message = player.leave_guild()
        await self.bot.say(message)

        game.save()


def setup(bot):
    bot.add_cog(GuildCog(bot))
