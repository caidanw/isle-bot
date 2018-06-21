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
    has_connected = db.connect()
    log_db('Connecting to database', has_connected)
    # create the proper tables if there aren't any
    if len(db.get_tables()) == 0:
        db.create_tables([Guild, Island, Resource, Inventory, Player])
        log_db('Created tables [Guild, Island, Resource, Inventory, Player]')
    return has_connected
