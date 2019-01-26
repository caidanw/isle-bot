from discord import HTTPException, TextChannel
from discord.abc import PrivateChannel

from game.game import Game
from src.ui.confirm_menu import ConfirmMenu
from utils import logger


def find_open_channel(guild):
    channel = None

    for c in guild.channels:
        if isinstance(c, TextChannel) and not isinstance(c, PrivateChannel):
            channel = c

    return channel


async def ask_guild_to_join_game(bot, guild, channel=None):
    if channel is None:
        channel = find_open_channel(guild)

    # we don't to pollute our database with random guilds that are inactive, so ask first if they want to join
    confirm_msg = ConfirmMenu(bot, channel,
                              ['Welcome, would you like this guild to be registered within the game?',
                                  'This guild will not be registered.',  # message when dismissed
                                  'This guild is now registered.'])  # message when confirmed
    await confirm_msg.send()
    logger.log(f'Asking guild "{guild.name}" [id:{guild.id}] to join the game.')
    confirmed = await confirm_msg.wait_for_user_reaction()

    if confirmed:
        # create a new guild for the guild
        union = Game.create_union(guild)
        logger.log(f'Created a new Union under the name "{union.name}"')
    else:
        await channel.send('I am leaving this guild, as I am no longer needed. '
                           'If you change your mind and would like to register this guild, just add me back.')
        try:
            guild.leave()
        except HTTPException as exception:
            logger.log(exception)
            await channel.send('Sorry to bother you, this is kind of embarrassing. '
                               'I am having some trouble leaving, would you mind kicking me please?')
