from discord import User

from game.inventory import Inventory


class Player:
    def __init__(self, user: User, guild, name=None):
        self.user = user
        self.uuid = user.id
        self.name = user.name if name is None else name
        self.guild = guild
        self.on_island = guild.get_island()
        self.inventory = Inventory()
