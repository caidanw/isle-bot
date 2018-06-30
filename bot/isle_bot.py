import os
import sys
import traceback
import logging

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from game.game import Game
from utils.check import is_private
from utils.logs import log_command, log
from utils.cache import Cache

DEBUGGING = True
TOKEN = Cache.get_from_json('data/config.json')['token']
PREFIXES = ('!', '?', '.', '~')
COGS_DIR = "bot.cogs"  # this specifies what extensions to load when the bot starts up (from this directory)

bot = Bot(PREFIXES)


@bot.event
async def on_ready():
    print('Logged in as')
    print('[name]:', bot.user.name)
    print('[  id]:', bot.user.id)
    print('------')


@bot.event
async def on_server_join(server):
    # create a new guild for the server
    guild = game.create_guild(server)
    print('Created a new Guild under the name "{}"'.format(guild.name))
    # Todo: add an option to ask whether or not the server should be created into a guild.


@bot.event
async def on_server_update(before, after):
    # check to see if there is a guild within the database already
    if game.check_guild_exists(before):
        prev = game.get_guild(before)
        prev.name = after.name
        prev.save()
        log('Updated the guild "{}" to be "{}"'.format(before.name, after.name))
    else:
        guild = game.create_guild(after)
        log('Created a new Guild under the name "{}"'.format(guild.name))


@bot.event
async def on_message(message):
    """ Run some checks to make sure the message is valid, then continue to process the valid commands. """
    if not message.content.startswith(PREFIXES):
        return

    message.content = message.content.lower()

    log_command(message.author, message.content.strip())

    player = game.get_player(message.author)
    if player is None and 'join' not in message.content:
        return await bot.send_message(message.channel, 'You are not registered as a part of this game.')

    if not is_private(message):
        guild = game.get_guild(message.server)
        if guild is None:
            return await bot.send_message(message.channel, 'This discord server is not registered as a guild.')

    await bot.process_commands(message)


@bot.event
async def on_member_remove(member):
    """ Remove the banned player from the guild,
    do nothing if the member wasn't currently in the guild. """
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
    log(exception)
    if DEBUGGING:
        traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    cmd = context.invoked_with

    if isinstance(exception, commands.CommandNotFound):
        return await bot.send_message(context.message.channel, f'Command "{cmd}" unknown. Try "?help"')

    elif isinstance(exception, discord.InvalidArgument) or isinstance(exception, commands.CommandInvokeError):
        return await bot.send_message(context.message.channel,
                                      f'Invalid argument "{exception.original}" for command "{cmd}". \nTry ?help')


if __name__ == "__main__":
    global game
    game = Game()

    # load all the extensions from the cogs directory
    for extension in os.listdir(COGS_DIR.replace('.', '/')):
        try:
            if extension.endswith('.py'):
                extension_path = COGS_DIR + "." + extension.replace('.py', '')
                bot.load_extension(extension_path)
                log('Loaded extension {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}:\n\t{}'.format(extension, exc))

    # run the bot with the token from the config file
    bot.run(TOKEN)
