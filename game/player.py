from peewee import *

from game.base_model import BaseModel
from game.guild import Guild
from game.inventory import Inventory
from game.island import Island
from utils.enums import Action


class Player(BaseModel):
    """ Player class used to represent a Discord User within the game world. """

    username = CharField()
    uuid = UUIDField()
    action = IntegerField(default=Action.idle.value)  # every action maps to an integer value
    guild = ForeignKeyField(Guild, backref='members', default=None)
    on_island = ForeignKeyField(Island, backref='residents', default=None)
    inventory = ForeignKeyField(Inventory, default=Inventory())

    @property
    def is_idle(self):
        return self.action is Action.idle.value

    def join_guild(self, guild):
        """ Join the desired Guild, first check that the Player does not belong
        to the desired Guild.

        :param guild: to join
        :return: a string declaring whether or not the player joined
        """
        if not guild.has_member(self):
            self.guild = self
            if self.on_island is None:
                self.on_island = guild.get_island()
            self.save()
            return '{} has joined {}'.format(self.username, guild.name)
        else:
            return '{} is already a member of {}'.format(self.username, guild.name)

    def leave_guild(self):
        """ Leave the current Guild, check if the Player does not have a guild.
        Otherwise remove them from their current Guild.

        :return: a string declaring whether or not the player was removed
        """
        if self.guild is None:
            return '{} is not a member of any guild'.format(self.username)

        if self.guild.has_member(self):
            guild_name = self.guild.name
            self.guild = None
            self.save()
            return '{} has been removed from {}'.format(self.username, guild_name)