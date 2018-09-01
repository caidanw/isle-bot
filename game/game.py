from discord import Guild, User
from peewee import fn

from game.objects.player import Player
from game.objects.resource import Resource
from utils import database
from game.objects.union import Union
from game.objects.island import Island
from utils.logger import log_db


class Game:
    """Main game class."""

    def __init__(self):
        """" Initialize main game system. """
        # connect to the database
        database.connect()

    @classmethod
    def create_union(cls, guild: Guild):
        """ Return an existing union if there is one linked to the discord guild,
        other wise create a new union using the discord guild.

        :param guild: the discord guild that the bot currently resides
        :return: a union
        """
        if cls.check_union_exists(guild):
            return cls.get_union(guild)

        # create and return a new union
        union = Union.create(guild_id=guild.id, name=guild.name)
        island = Game.create_island(union)
        union.claim_island(island)
        union.save()
        return union

    @classmethod
    def check_union_exists(cls, guild: Guild):
        """ Check to see if a union exists within the database

        :param guild: to check for
        :return: a boolean
        """
        if Union.get_or_none(Union.guild_id == guild.id) is None:
            return False
        return True

    @classmethod
    def get_union(cls, guild: Guild):
        """ Search for an existing union from the desired guild

        :param guild: to search for
        :return: a union if found
        """
        try:
            return Union.get(Union.guild_id == guild.id)
        except Exception:
            log_db(f'Guild "{guild.name}" [id:{guild.id}] is not registered as a union.')
            return None

    @classmethod
    def search_unions(cls, name: str):
        """ Attempt to find a union with 'name' in the database

        :param name: the name of the union to search for
        :return: the union if found, otherwise None
        """
        return Union.get_or_none(fn.Lower(Union.name) == name)

    @classmethod
    def search_unions_by_guild_id(cls, guild_id: int):
        """ Attempt to find a union with 'name' in the database

        :param guild_id: the unique id of the guild to search for
        :return: the union if found, otherwise None
        """
        return Union.get_or_none(Union.guild_id == guild_id)

    @classmethod
    def get_player(cls, user: User):
        """ Retrieve the Player from the database with the desired User.

        :param user: to search for in the database by id
        :return: [Player | None] object
        """
        return Player.get_or_none(Player.uuid == user.id)

    @classmethod
    def get_player_by_name(cls, name: str):
        """ Retrieve the Player from the database with the desired name.

        :param name: to search for in the database
        :return: [Player | None] object
        """
        return Player.get_or_none(Player.username == name)

    @classmethod
    def create_island(cls, union: Union=None, resource_amount: int=5):
        """ Create a new Island with the desired amount of resources,
        and place it under the control of the desired union
        (if union is None, then it is a 'Lost Island').

        :param union: to give control of the island
        :param resource_amount: amount of resources on the island
        """
        if union is None:
            return None

        island = Island.create()
        union.claim_island(island)

        for i in range(resource_amount):
            Resource.random(island)  # create new resources for the island

        island.save()
        return island

    @classmethod
    def check_island_exists(cls, island: Island):
        """ Check to see if an island exists within the database

        :param island: to check for
        :return: a boolean
        """
        return Island.get_or_none(Island.id == island.id) is not None

    @classmethod
    def search_islands(cls, name: str):
        """ Attempt to find a union with 'name' in the database

        :param name: the name of the union to search for
        :return: the union if found, otherwise None
        """
        return Island.get_or_none(fn.Lower(Island.name) == name)

    @classmethod
    def search_islands_by_number(cls, union: Union, number: int):
        for island in union.islands:
            if island.union_number == number:
                return island
        return None
