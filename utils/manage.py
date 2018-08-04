from discord import HTTPException

from ui.confirm_message import ConfirmMessage
from utils import logger


async def ask_server_to_join_game(game, bot, server, channel):
    # we don't to pollute our database with random servers that are inactive, so ask first if they want to join
    confirm_msg = ConfirmMessage(bot, channel,
                                 ['Welcome, would you like this guild to be registered within the game?',
                                  'This guild will not be registered.',  # message when dismissed
                                  'This guild is now registered.'])  # message when confirmed
    await confirm_msg.send()
    logger.log(f'Asking server "{server.name}" [id:{server.id}] to join the game.')
    confirmed = await confirm_msg.wait_for_user_reaction()

    if confirmed:
        # create a new guild for the server
        guild = game.create_guild(server)
        logger.log(f'Created a new Guild under the name "{guild.name}"')
    else:
        bot.send_message(channel, 'I am leaving this server, as I am no longer needed. '
                                  'If you change your mind and would like to register this guild, just add me back.')
        try:
            bot.leave_server(server)
        except HTTPException as exception:
            logger.log(exception)
            bot.send_message(channel, 'Sorry to bother you, this is kind of embarrassing. '
                                      'I am having some trouble leaving, would you mind kicking me please?')
