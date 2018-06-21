import os

from discord.ext import commands
from discord.ext.commands import Bot

from game.game import Game
from utils.check import is_private
from utils.logs import log_command, log
from utils.cache import Cache

TOKEN = Cache.get_from_json('data/config.json')['token']
PREFIXES = ('!', '?', '.', '~')
COGS_DIR = "bot.cogs"  # this specifies what extensions to load when the bot starts up (from this directory)

bot = Bot(PREFIXES)
game = None


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
    print('Created a new Guild under the name \'{}\''.format(guild.name))
    # Todo: add an option to ask whether or not the server should be created into a guild.


@bot.event
async def on_server_update(before, after):
    # create a new guild for the server
    prev = game.get_guild(before)
    if prev is None:
        guild = game.create_guild(after)
        print('Created a new Guild under the name \'{}\''.format(guild.name))
    else:
        prev.name = after.name
        prev.save()
        print('Updated the guild \'{}\' to be \'{}\''.format(before.name, after.name))


@bot.event
async def on_message(message):
    """ Run some checks to make sure the message is valid, then continue to process the valid commands. """
    if not message.content.startswith(PREFIXES):
        return

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
async def on_command_error(exception, context):
    print(exception)
    if isinstance(exception, commands.CommandNotFound):
        return await bot.send_message(context.message.channel,
                                      'Command \'{}\' unknown.\nTry \'?help\''.format(context.invoked_with))


if __name__ == "__main__":
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

    game = Game()

    # run the bot with the token from the config file
    bot.run(TOKEN)
