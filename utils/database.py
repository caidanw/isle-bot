from sqlite3 import OperationalError

from game.tables.inventory import Inventory
from game.tables.island import Island
from game.tables.player import Player
from game.tables.player_stat import PlayerStat
from game.tables.resource import Resource
from game.tables.union import Union
from utils import logger
from utils.cache import db


def connect():
    """ Connect to the database, and make sure the correct tables are setup

    :return: whether or not the connection was successful
    """
    try:
        has_connected = db.connect()
        logger.log_db('Connecting to database', has_connected)

        object_tables = [Union, Island, Resource, Player, PlayerStat, Inventory]
        db_tables = db.get_tables()

        # create the proper tables if there aren't any
        if len(db_tables) != len(object_tables):
            db.create_tables(object_tables)
            logger.log_db('Created new tables {}'.format(
                [table.__name__ for table in object_tables if table not in db_tables]
            ))

        return has_connected
    except OperationalError as e:
        logger.log_db(e)
