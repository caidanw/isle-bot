from datetime import datetime

from peewee import *

from src.game import BaseModel


class Union(BaseModel):
    """ Union class used to represent a Discord Guild. """

    guild_id = IntegerField()
    name = CharField(max_length=100)
    max_islands = IntegerField(default=1)
    claimed_islands = IntegerField(default=0)
    created_at = DateTimeField(default=datetime.now())

    @property
    def member_count(self):
        """ Return the (int) amount of members currently in this union. """
        return len(self.members)

    def set_name(self, name):
        self.name = name
        self.save()

    def has_member(self, player):
        """ Search through the list of members that belong to this union,
        find the desired player.

        :param player: to search for among the union members
        :return: a boolean (True if the player is a member)
        """
        return player in self.members

    def get_member(self, user):
        """ Search for the discord user among the members and compare based on (UU)ID.

        :param user: to compare the user.id
        :return: [Player or None] object
        """
        for player in self.members:
            if player.uuid == user.id:
                return player
        return None

    def claim_island(self, island):
        """ Claim an island for the union, also check if union can sustain another island.
        If the union can take on another island then set the islands attributes appropriately.

        :param island: to claim for this union
        :return: a boolean (True if island claimed)
        """
        if self.claimed_islands < self.max_islands:
            self.claimed_islands += 1

            island.union = self
            island.union_number = self.claimed_islands
            island.name = f'Island #{island.union_number}'
            island.claimed = True

            island.save()
            self.save()
            return True
        return False

    def get_island(self, name=None):
        """ Find an island of the given name, otherwise get the only island the union owns.

        :param name: of the island
        :return: [Island or None] object
        """
        # query the db to islands associated with this union id
        if not name:
            # return the first island if no name is given
            return self.islands[0]

        for island in self.islands:
            if island.name == name:
                return island
        return None
