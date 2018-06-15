from discord import Server

from utils import data_handler
from game.guild import Guild
from game.island import Island


class Game:
    """Main game class."""

    def __init__(self):
        """"Initialize main game system."""
        self.actions = []

        # load from file if we have it
        if data_handler.validate('guilds'):
            self.guilds = data_handler.load('guilds')
        else:
            self.guilds = []

    def create_guild(self, server: Server):
        """ Return an existing guild if there is one linked to the discord server,
        other wise create a new guild using the discord server.

        :param server: the discord server that the bot currently resides
        :return: a guild
        """
        existing_guild = self.get_guild(server)
        if existing_guild:
            return existing_guild

        # create and add a new guild
        guild = Guild(server)
        self.guilds.append(guild)
        self.save()

        return guild

    def get_guild(self, server: Server):
        """ Search for an existing guild from the desired server

        :param server: to search for
        :return: a guild
        """
        for guild in self.guilds:
            if guild.server.id == server.id:
                return guild
        return None

    @classmethod
    def create_island(cls, guild: Guild):
        island = Island(guild)
        guild.claim_island(island)

    def save(self):
        # save our guilds to ensure our data persists
        data_handler.save(self.guilds, 'guilds')
