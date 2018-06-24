from sqlite3 import OperationalError

from game.enums.item import Item
from utils.cache import db
from game.guild import Guild
from game.inventory import Inventory
from game.island import Island
from game.player import Player
from game.resource import Resource
from utils.logs import log_db


def connect():
    """ Connect to the database, and make sure the correct tables are setup

    :return: whether or not the connection was successful
    """
    try:
        has_connected = db.connect()
        log_db('Connecting to database', has_connected)

        object_tables = [Guild, Island, Resource, Inventory, Player, Item]

        # create the proper tables if there aren't any
        if len(db.get_tables()) != len(object_tables):
            db.create_tables(object_tables)
            log_db('Created new tables')

        return has_connected
    except OperationalError as e:
        log_db(e)
