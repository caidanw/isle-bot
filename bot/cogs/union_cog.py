from discord.abc import PrivateChannel
from discord.ext import commands

from game.game import Game
from game.inventory import Inventory
from game.player import Player


class UnionCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,
                      description='Join the union of the current discord guild, ' +
                                  'if a name is passed then join that union instead.')
    async def join(self, context, union_name=None):
        """ Join a union. """
        channel = context.message.channel
        is_private = isinstance(channel, PrivateChannel)

        if is_private and union_name is None:
            return await context.message.channel.send('You must enter the name of the union you would like to join.')

        if is_private:
            union = Game.search_unions(union_name)
        else:
            union = Game.get_union(context.message.guild)

        if union is None:
            return await context.message.channel.send('That union does not exist or is not registered.')

        player = Game.get_player(context.message.author)
        if player and player.union:
            return await context.message.channel.send(f'You already belong to the union {player.union.name}')
        elif player is None:
            # invoke the 'create' command, instead of rewriting functionality
            return await self.bot.commands.get('create').invoke(context)

        await context.message.channel.send(player.join_union(union))

    @commands.command(pass_context=True)
    async def leave(self, context):
        """ Leave your current union. """
        player = Game.get_player(context.message.author)

        message = player.leave_union()
        await context.message.channel.send(message)


def setup(bot):
    bot.add_cog(UnionCog(bot))
