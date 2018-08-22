from peewee import *

from game.base_model import BaseModel
from game.tables.player_stat import PlayerStat
from game.tables.union import Union
from game.tables.inventory import Inventory
from game.tables.island import Island
from game.enums.action import Action


class Player(BaseModel):
    """ Player class used to represent a Discord User within the game world. """

    username = CharField()
    uuid = IntegerField()
    action = IntegerField(default=Action.IDLE.value)  # every action maps to an integer value
    union = ForeignKeyField(Union, backref='members', null=True)
    on_island = ForeignKeyField(Island, backref='residents', null=True)
    inventory = ForeignKeyField(Inventory)
    stats = ForeignKeyField(PlayerStat)

    @property
    def is_idle(self):
        return self.action is Action.IDLE.value

    @property
    def get_location(self):
        if self.on_island is not None:
            return Island.get_or_none(Island.id == self.on_island)
        return None

    def set_location(self, island: Island):
        self.on_island = island
        self.save()

    def set_action(self, action: Action):
        self.action = action.value
        self.save()

    def join_union(self, union):
        """ Join the desired Union, first check that the Player does not belong
        to the desired Union.

        :param union: to join
        :return: a string declaring whether or not the player joined
        """
        if not union.has_member(self):
            self.union = union
            if self.on_island is None:
                self.on_island = union.get_island()
            self.save()
            return f'{self.username} has joined {union.name}'
        else:
            return f'{self.username} is already a member of {union.name}'

    def leave_union(self):
        """ Leave the current Union, check if the Player does not have a Union.
        Otherwise remove them from their current Union.

        :return: a string declaring whether or not the player was removed
        """
        if self.union is None:
            return f'{self.username} is not a member of any guild'

        if self.union.has_member(self):
            union_name = self.union.name
            self.union = None
            self.save()
            return f'{self.username} has been removed from {union_name}'
