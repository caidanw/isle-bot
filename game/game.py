from discord import Server, User
from peewee import fn

from game.player import Player
from game.resource import Resource
from utils import database
from game.guild import Guild
from game.island import Island
from utils.logs import log_db


class Game:
    """Main game class."""

    def __init__(self):
        """"Initialize main game system."""
        # connect to the database
        database.connect()

    @classmethod
    def create_guild(cls, server: Server):
        """ Return an existing guild if there is one linked to the discord server,
        other wise create a new guild using the discord server.

        :param server: the discord server that the bot currently resides
        :return: a guild
        """
        if cls.check_guild_exists(server):
            return cls.get_guild(server)

        # create and return a new guild
        guild = Guild.create(server_id=server.id, name=server.name)
        island = Game.create_island(guild)
        guild.claim_island(island)
        guild.save()
        return guild

    @classmethod
    def check_guild_exists(cls, server: Server):
        """ Check to see if a guild exists within the database

        :param server: to check for
        :return: a boolean
        """
        if Guild.get_or_none(Guild.server_id == server.id) is None:
            return False
        return True

    @classmethod
    def get_guild(cls, server: Server):
        """ Search for an existing guild from the desired server

        :param server: to search for
        :return: a guild if found
        """
        try:
            return Guild.get(Guild.server_id == server.id)
        except Exception:
            log_db('Server "{}" [id:{}] has not been registered as a guild.'.format(server.name, server.id))
            return None

    @classmethod
    def search_guilds(cls, name):
        """ Attempt to find a guild with 'name' in the database

        :param name: the name of the guild to search for
        :return: the guild if found, otherwise None
        """
        return Guild.get_or_none(fn.Lower(Guild.name) == name)

    @classmethod
    def get_player(cls, user: User):
        """ Retrieve the Player from the database with the desired User.

        :param user: to search for in the database by id
        :return: [Player | None] object
        """
        return Player.get_or_none(Player.uuid == user.id)

    @classmethod
    def create_island(cls, guild: Guild=None, resource_amount=5):
        """ Create a new Island with the desired amount of resources,
        and place it under the control of the desired guild
        (if guild is None, then it is a 'Lost Island').

        :param guild: to give control of the island
        :param resource_amount: amount of resources on the island
        """
        island = Island()

        if guild is not None:
            guild.claim_island(island)

        for i in range(resource_amount):
            Resource.random(island)

        island.save()
        return island

    @classmethod
    def check_island_exists(cls, island: Island):
        """ Check to see if an island exists within the database

        :param island: to check for
        :return: a boolean
        """
        if Island.get_or_none(Island.id == island.id) is None:
            return False
        return True

    @classmethod
    def search_islands(cls, name):
        """ Attempt to find a guild with 'name' in the database

        :param name: the name of the guild to search for
        :return: the guild if found, otherwise None
        """
        return Island.get_or_none(fn.Lower(Island.name) == name)
