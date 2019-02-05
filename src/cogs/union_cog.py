from discord.abc import PrivateChannel
from discord.ext import commands

from src import settings
from src.cogs._abstract_cog import AbstractCog
from src.game.game import Game


class UnionCog(AbstractCog):
    @commands.command(description='Join the union of the current discord guild, ' +
                                  'if a name is passed then join that union instead.')
    async def join(self, context, union_name=None):
        """ Join a union. """
        channel = context.message.channel
        is_private = isinstance(channel, PrivateChannel)

        if is_private and union_name is None:
            return await channel.send('You must enter the name of the union you would like to join.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        if is_private:
            union = Game.search_unions(union_name)
        else:
            union = Game.get_union(context.message.guild)

        if union is None:
            return await channel.send('That union does not exist or is not registered.',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

        player = Game.get_player(context.author)
        if player and player.union:
            return await channel.send(f'You already belong to the union {player.union.name}',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)
        elif player is None:
            # invoke the 'create' command, instead of rewriting functionality
            return await self.bot.get_command('create').invoke(context)

        await channel.send(player.join_union(union))

    @commands.command()
    async def leave(self, context):
        """ Leave your current union. """
        player = Game.get_player(context.author)

        message = player.leave_union()
        await context.send(message)


def setup(bot):
    bot.add_cog(UnionCog(bot))
