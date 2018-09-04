from sqlite3 import OperationalError

from game.objects.inventory import Inventory
from game.objects.island import Island
from game.objects.player import Player
from game.objects.player_stat import PlayerStat
from game.objects.resource import Resource
from game.objects.union import Union
from utils import logger
from utils.cache import db


def connect():
    """ Connect to the database, and make sure the correct objects are setup

    :return: whether or not the connection was successful
    """
    try:
        has_connected = db.connect()
        logger.log_db('Connecting to database', has_connected)

        object_tables = [Union, Island, Resource, Player, PlayerStat, Inventory]
        db_tables = db.get_tables()

        # create the proper objects if there aren't any
        if len(db_tables) != len(object_tables):
            db.create_tables(object_tables)
            logger.log_db('Created new object tables {}'.format(
                [table.__name__ for table in object_tables if table not in db_tables]
            ))

        return has_connected
    except OperationalError as e:
        logger.log_db(e)
