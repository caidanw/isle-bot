import asyncio

from discord.ext.commands import Bot

from game.game import Game
from game.player import Player
from utils.clock import server_clock
from utils.logs import log_command

TOKEN = 'NDU2MDk5MzExMzM2NDIzNDM1.DgF-jA.ymkelNjBMc5sJHtXdB9jppgAI0U'
PREFIXES = ('!', '?', '.', '-', '~')

bot = Bot(PREFIXES)
game = Game()


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


@bot.event
async def on_server_update(before, after):
    # create a new guild for the server
    guild = game.create_guild(after)
    print('Created a new Guild under the name \'{}\''.format(guild.name))


@bot.event
async def on_message(message):
    if message.content.startswith(PREFIXES):
        log_command(message.author, message.content[1:])
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def join(context):
    guild = game.get_guild(context.message.server)
    player = Player(user=context.message.author, guild=guild)

    message = guild.add_member(player)
    await bot.say(message)

    game.save()


@bot.command(pass_context=True)
async def harvest(context, desired_amount=5, resource_name=None):
    guild = game.get_guild(context.message.server)
    if not guild:
        await bot.say('The discord server is not registered as a guild.')
        return

    player = guild.get_member(context.message.author)
    if not player:
        await bot.say('You are not registered as a member of this guild.'
                      '\n\nType \'.join_guild\' to join this discord server\'s guild')
        return

    island = player.on_island
    resource = island.get_resource(resource_name)
    if not resource:
        await bot.say('The resource \'{}\' is not on the current island.'.format(resource_name))
        return
    elif resource.amount < desired_amount:
        await bot.say('The resource only has {} items left to harvest.'.format(resource.amount))
        return

    player_inv = player.inventory
    if not player_inv.validate_stack(resource.gives_item, desired_amount):
        await bot.say('You don\'t have enough room in your inventory.')
        return

    await bot.say('Harvesting from {}, time to finish {}s'.format(desired_amount,
                                                                  resource.seconds_to_one_item * desired_amount))
    item_stack = await resource.harvest(desired_amount)
    player_inv.add_item(item_stack.item, item_stack.amount)
    await bot.say('{} harvested {} {}'.format(player.user.mention, item_stack.amount, item_stack.item))


@bot.command(pass_context=True)
async def hello(context):
    await bot.say('Hello {}, you looking dashing today.'.format(context.message.author.mention))


@bot.command(pass_context=True)
async def smile(context):
    await bot.add_reaction(context.message, emoji='😊')


@bot.command(pass_context=True)
async def sleep(context, amount: int=10):
    await bot.say('Sleeping {}s'.format(amount))
    await asyncio.sleep(amount)
    await bot.say('Finished sleeping')
    log_command(context.message.author, 'sleep {}'.format(amount), issued=False)


@bot.command(pass_context=True)
async def clock():
    await bot.say(server_clock())


if __name__ == '__main__':
    bot.run(TOKEN)
