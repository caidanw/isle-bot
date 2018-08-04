from peewee import *

from game.base_model import BaseModel
from game.guild import Guild
from game.inventory import Inventory
from game.island import Island
from game.enums.action import Action


class Player(BaseModel):
    """ Player class used to represent a Discord User within the game world. """

    username = CharField()
    uuid = IntegerField()
    action = IntegerField(default=Action.idle.value)  # every action maps to an integer value
    guild = ForeignKeyField(Guild, backref='members', null=True)
    on_island = ForeignKeyField(Island, backref='residents', null=True)
    inventory = ForeignKeyField(Inventory)

    @property
    def is_idle(self):
        return self.action is Action.idle.value

    @property
    def get_location(self):
        if self.on_island is not None:
            return Island.get_or_none(Island.id == self.on_island)
        return None

    def set_location(self, island: Island):
        self.on_island = island
        self.save()

    def join_guild(self, guild):
        """ Join the desired Guild, first check that the Player does not belong
        to the desired Guild.

        :param guild: to join
        :return: a string declaring whether or not the player joined
        """
        if not guild.has_member(self):
            self.guild = guild
            if self.on_island is None:
                self.on_island = guild.get_island()
            self.save()
            return f'{self.username} has joined {guild.name}'
        else:
            return f'{self.username} is already a member of {guild.name}'

    def leave_guild(self):
        """ Leave the current Guild, check if the Player does not have a guild.
        Otherwise remove them from their current Guild.

        :return: a string declaring whether or not the player was removed
        """
        if self.guild is None:
            return f'{self.username} is not a member of any guild'

        if self.guild.has_member(self):
            guild_name = self.guild.name
            self.guild = None
            self.save()
            return f'{self.username} has been removed from {guild_name}'
