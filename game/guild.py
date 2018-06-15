from datetime import datetime

from discord import Server

from game.island import Island
from game.player import Player


class Guild:
    def __init__(self, server: Server, name=None):
        self.server = server
        self.name = server.name if name is None else name
        self.members = []
        self.max_islands = 1
        self.islands = []
        self.created_at = datetime.now().isoformat()
        self.days_since_founded = 0
        self.claim_island(Island(self))

    @property
    def member_count(self):
        return len(self.members)

    def get_member(self, user):
        for player in self.members:
            if player.uuid == user.id:
                return player
        return None

    def add_member(self, player: Player):
        member = self.get_member(player.user)
        if member:
            return '{} is already a member of {}'.format(player.name, self.name)
        else:
            self.members.append(player)
            return '{} has joined {}'.format(player.name, self.name)

    def claim_island(self, island):
        if len(self.islands) >= self.max_islands:
            return 'already at max islands'
        else:
            self.islands.append(island)
            island.claimed = True
            return 'new island claimed'

    def get_island(self, name=None):
        """ Find an island of the given name, otherwise get the only island the guild has

        :param name: of the island
        :return: an island
        """
        if not name:
            return self.islands[0]

        for island in self.islands:
            if island.name == name:
                return island
        return None
