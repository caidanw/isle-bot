from discord.ext import commands

from game.game import Game
from game.inventory import Inventory
from game.player import Player
from utils.check import is_private


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

        if private_channel:
            guild = Game.search_guilds(guild_name)
        else:
            guild = Game.get_guild(context.message.server)

        if guild is None:
            return await self.bot.say('That guild does not exist or is not registered.')

        player = Game.get_player(context.message.author)
        if player and player.guild:
            return await self.bot.say('You already belong to the guild {}'.format(player.guild.name))
        elif player is None:
            author = context.message.author

            player = Player.create(username=author.name,
                                   uuid=author.id,
                                   guild=guild,
                                   on_island=guild.get_island(),
                                   inventory=Inventory.create())

        if player.guild is guild:
            message = '{} was born and has joined {}'.format(player.username, guild.name)
        else:
            message = player.join_guild(guild)

        await self.bot.say(message)

    @commands.command(pass_context=True)
    async def leave(self, context):
        """ Leave your current guild. """
        player = Game.get_player(context.message.author)

        message = player.leave_guild()
        await self.bot.say(message)


def setup(bot):
    bot.add_cog(GuildCog(bot))
