import os
import sys
import traceback

import discord
from discord.abc import PrivateChannel
from discord.ext import commands
from discord.ext.commands import Bot

from game.game import Game
from utils import manage, logger
from utils.cache import Cache
from utils.manage import find_open_channel

DEBUGGING = Cache.get_from_json('data/config.json')['debugging']
TOKEN = Cache.get_from_json('data/config.json')['token']
PREFIXES = ('!', '?', '.', '~')
COGS_DIR = "cogs."  # this specifies the directory of extensions to load when the bot starts up ('.' replaces '/')

bot = Bot(PREFIXES)
bot.remove_command('help')  # I have my own custom help command, I don't use any of the pre-made filth


@bot.event
async def on_ready():
    """ Runs after the bot logs in and before any commands are taken. """
    print('Logged in as')
    print('[name]:', bot.user.name)
    print('[  id]:', bot.user.id)
    print('-------')


@bot.event
async def on_guild_join(guild):
    """ When the bot is added to a guild, ask them to join the game. If they refuse, then leave the guild. """
    if not game.check_union_exists(guild):
        await manage.ask_guild_to_join_game(game, bot, guild)
    else:
        channel = find_open_channel(guild)
        await channel.send('Ah, I am glad to see you have rejoined the game. Welcome back, we are happy to have you.')


@bot.event
async def on_guild_update(before, after):
    """ When a guild updates, we want to update it's corresponding union. """
    # check to see if there is a union within the database already
    if game.check_union_exists(before):
        game.get_union(before).set_name(after.name)
        logger.log(f'Updated the union named "{before.name}" to "{after.name}"')
    else:
        # theoretically there can't be a case where a union is updated before it's created... except in testing
        await manage.ask_guild_to_join_game(game, bot, after)


@bot.event
async def on_message(message):
    """ Run some checks to make sure the message is valid, then continue to process the valid commands. """
    if not message.content.startswith(PREFIXES):
        return

    content = message.content.lower()
    channel = message.channel

    logger.log_command(message.author, message.content.strip())

    player = game.get_player(message.author)
    if player is None:
        if 'create' not in content and 'join' not in content:
            return await channel.send('You are not registered as a part of this game. Try "?create"')

    if not isinstance(channel, PrivateChannel):
        union = game.get_union(message.guild)
        if union is None:
            await channel.send('This discord guild is now registered as a union.')
            return await manage.ask_guild_to_join_game(bot, message.guild, channel)

    await bot.process_commands(message)


@bot.event
async def on_member_remove(member):
    """ Remove the banned player from the union, do nothing if the player wasn't a member of the union. """
    player = Game.get_player(member)
    union = Game.get_union(member.guild)

    if player is None or union is None:
        return

    if player in union.members:
        message = player.leave_union()
        return await bot.send_message(member.guild, message)


@bot.event
async def on_command_error(context, exception):
    """ Handle errors that are given from the bot. """
    if DEBUGGING:
        logger.log(exception)
        traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    cmd = context.invoked_with
    channel = context.message.channel

    if isinstance(exception, commands.CommandNotFound):
        return await channel.send(f'Command "{cmd}" unknown. Try "?help"')

    elif isinstance(exception, discord.InvalidArgument):
        return await channel.send(f'Invalid argument for command "{cmd}". Try "?help {cmd}"')

    elif isinstance(exception, commands.MissingRequiredArgument):
        return await channel.send(f'Missing argument for command "{cmd}". Try "?help {cmd}"')

    elif isinstance(exception, commands.CommandInvokeError):
        return await channel.send('Oops, looks like something on the back end broke. '
                                  'Please contact @mildmelon#5380.')


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
            if DEBUGGING:
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}:\n\t{exc}')

    # run the bot with the token from the config file
    bot.run(TOKEN)
