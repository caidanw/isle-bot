from discord import Server, User

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
        existing_guild = cls.get_guild(server)
        if existing_guild:
            return existing_guild

        # create and return a new guild
        guild = Guild.create(server_id=server.id, name=server.name)
        guild.claim_island(Island())

    @classmethod
    def get_guild(cls, server: Server):
        """ Search for an existing guild from the desired server

        :param server: to search for
        :return: a guild if found
        """
        try:
            return Guild.get(Guild.server_id == server.id)
        except Exception:
            log_db('Server #{} has not been registered as a guild.'.format(server.id))
            return None

    @classmethod
    def search_guilds(cls, name):
        """ Attempt to find a guild with 'name' in the database

        :param name: the name of the guild to search for
        :return: the guild if found, otherwise None
        """
        try:
            return Guild.get(Guild.name == name)
        except Exception:
            log_db('The name \'{}\' could not be found among the guilds.'.format(name))
            return None

    @classmethod
    def create_player(cls, user: User):
        """ Add a new Player to this game and return them.
        Unless they already exist in the database, then return that player.

        :param user: used to create a player
        """
        existing_player = cls.get_player(user)
        if existing_player:
            return existing_player

        # create and return a new player
        return Player.create(username=user.name, uuid=user.id)

    @classmethod
    def get_player(cls, user: User):
        """ Retrieve the Player from the database with the desired User.

        :param user: to search for in the database
        :return: [Player | None] object
        """
        try:
            return Player.get(Player.uuid == user.id)
        except Exception:
            log_db('User #{} has not been registered to a guild.'.format(user.id))
            return None

    @classmethod
    def create_island(cls, guild: Guild=None, resource_amount=5):
        """ Create a new Island with the desired amount of resources,
        and place it under the control of the desired guild
        (if guild is None, then it is a 'Lost Island').

        :param guild: to give control of the island
        :param resource_amount: amount of resources on the island
        """
        island = Island()
        for i in range(resource_amount):
            resource = Resource.random(island)
            island.add_resource(resource)

        if guild is not None:
            guild.claim_island(island)

        island.save()
