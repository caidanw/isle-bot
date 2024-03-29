import asyncio
import os
import sys
import traceback

import discord
from discord.abc import PrivateChannel
from discord.ext import commands
from discord.ext.commands import Bot

from src import settings
from src.game import world_tasks
from src.game.game import Game
from src.utils import logger, manage
from src.utils.manage import find_open_channel

PREFIXES = ('!', '?', '.', '~')
COGS_DIR = "src.cogs."  # this specifies the directory of extensions to load when the bot starts up ('.' replaces '/')

bot = Bot(PREFIXES)
bot.remove_command('help')  # I have my own custom help command, I won't use any of that pre-made filth


@bot.event
async def on_ready():
    """ Runs after the bot logs in and before any commands are taken. """
    logger.log('Logged in as')
    logger.log(f'[name]: {bot.user.name}')
    logger.log(f'[  id]: {bot.user.id}')
    logger.log('-------')


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

    if not game.check_player_exists(message.author):
        if 'create' not in content and 'join' not in content:
            return await channel.send('You are not registered as a part of this game. Try "?create"',
                                      delete_after=settings.DEFAULT_DELETE_DELAY)

    if not isinstance(channel, PrivateChannel):
        union = game.get_union(message.guild)
        if union is None:
            await channel.send('This discord guild is not registered as a union.')
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
        # TODO: get this working with sending to the proper channel
        # await bot.send_message(member.guild, message)


@bot.event
async def on_command_error(context, exception):
    """ Handle errors that are given from the bot. """
    if settings.DEBUGGING:
        logger.log(exception)
        traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    cmd = context.invoked_with
    channel = context.message.channel

    if isinstance(exception, commands.CommandNotFound):
        await channel.send(f'Command "{cmd}" unknown. Try "?help"', delete_after=settings.DEFAULT_DELETE_DELAY)

    elif isinstance(exception, discord.InvalidArgument):
        await channel.send(f'Invalid argument for command "{cmd}". Try "?help {cmd}"',
                           delete_after=settings.DEFAULT_DELETE_DELAY)

    elif isinstance(exception, commands.MissingRequiredArgument):
        await channel.send(f'Missing argument for command "{cmd}". Try "?help {cmd}"',
                           delete_after=settings.DEFAULT_DELETE_DELAY)

    elif isinstance(exception, commands.CommandInvokeError):
        await channel.send('Oops, looks like something on the back end broke. Please contact @mildmelon#5380.',
                           delete_after=settings.DEFAULT_DELETE_DELAY)

    await asyncio.sleep(settings.DEFAULT_DELETE_DELAY)
    await context.message.delete()


if __name__ == "__main__":
    global game
    game = Game()

    # load all the extensions from the cogs directory
    for extension in os.listdir(COGS_DIR.replace('.', '/')):
        try:
            if extension.endswith('.py') and not extension.startswith('__'):
                extension_path = COGS_DIR + extension.replace('.py', '')
                bot.load_extension(extension_path)
                logger.log(f'Loaded extension {extension}')
        except Exception as e:
            if settings.DEBUGGING:
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}:\n\t{exc}')

    # run tasks for the game before starting the bot, this includes starting infinite looping tasks
    world_tasks.register_tasks(bot)

    # login and start the bot
    bot.run(settings.get_token())
