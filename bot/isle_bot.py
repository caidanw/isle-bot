import os
import sys
import traceback

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from game.game import Game
from utils import manage, logger, check
from utils.cache import Cache

DEBUGGING = True
TOKEN = Cache.get_from_json('data/config.json')['token']
PREFIXES = ('!', '?', '.', '~')
COGS_DIR = "bot.cogs."  # this specifies the directory of extensions to load when the bot starts up ('.' replaces '/')

bot = Bot(PREFIXES)


@bot.event
async def on_ready():
    """ Runs after the bot logs in and before any commands are taken. """
    print('Logged in as')
    print('[name]:', bot.user.name)
    print('[  id]:', bot.user.id)
    print('------')


@bot.event
async def on_server_join(server):
    """ When the bot is added to a server, ask them to join the game. If they refuse, then leave the server. """
    if not game.check_guild_exists(server):
        await manage.ask_server_to_join_game(game, bot, server, server.default_channel)
    else:
        bot.send_message(server, 'Ah, I glad to see you rejoined the game. Welcome back, we are happy to have you.')


@bot.event
async def on_server_update(before, after):
    """ When a server updates, we want to update it's corresponding guild. """
    # check to see if there is a guild within the database already
    if game.check_guild_exists(before):
        prev = game.get_guild(before)
        prev.name = after.name
        prev.save()
        logger.log(f'Updated the guild "{before.name}" to be "{after.name}"')
    else:
        # theoretically there can't be a case where a guild is updated before it's created... except in testing
        await manage.ask_server_to_join_game(game, bot, after, after.default_channel)


@bot.event
async def on_message(message):
    """ Run some checks to make sure the message is valid, then continue to process the valid commands. """
    if not message.content.startswith(PREFIXES):
        return

    message.content = message.content.lower()

    logger.log_command(message.author, message.content.strip())

    player = game.get_player(message.author)
    if player is None and 'join' not in message.content:
        return await bot.send_message(message.channel, 'You are not registered as a part of this game.')

    if not check.is_private(message):
        guild = game.get_guild(message.server)
        if guild is None:
            await bot.send_message(message.channel, 'This discord server is not registered as a guild.')
            return await manage.ask_server_to_join_game(game, bot, message.server, message.channel)

    await bot.process_commands(message)


@bot.event
async def on_member_remove(member):
    """ Remove the banned player from the guild, do nothing if the player wasn't a member of the guild. """
    player = Game.get_player(member)
    guild = Game.get_guild(member.server)

    if player is None or guild is None:
        return

    if player in guild.members:
        message = player.leave_guild()
        return await bot.send_message(member.server, message)


@bot.event
async def on_command_error(exception, context):
    """ Handle errors that are given from the bot. """
    if DEBUGGING:
        logger.log(exception)
        traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    cmd = context.invoked_with

    if isinstance(exception, commands.CommandNotFound):
        return await bot.send_message(context.message.channel, f'Command "{cmd}" unknown. Try "?help"')

    elif isinstance(exception, discord.InvalidArgument):
        return await bot.send_message(context.message.channel,
                                      f'Invalid argument for command "{cmd}". Try "?help {cmd}"')

    elif isinstance(exception, commands.MissingRequiredArgument):
        return await bot.send_message(context.message.channel,
                                      f'Missing argument for command "{cmd}". Try "?help {cmd}"')

    elif isinstance(exception, commands.CommandInvokeError):
        return await bot.send_message(context.message.channel,
                                      'Oops, looks like something on the back end broke. '
                                      'Please contact the admin or developer.')


if __name__ == "__main__":
    global game
    game = Game()

    # load all the extensions from the cogs directory
    for extension in os.listdir(COGS_DIR.replace('.', '/')):
        try:
            if extension.endswith('.py'):
                extension_path = COGS_DIR + extension.replace('.py', '')
                bot.load_extension(extension_path)
                logger.log(f'Loaded extension {extension}')
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}:\n\t{exc}')

    # run the bot with the token from the config file
    bot.run(TOKEN)
