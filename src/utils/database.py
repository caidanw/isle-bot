from sqlite3 import OperationalError

from src import models
from src.utils import logger
from src.utils.cache import db


def connect():
    """ Connect to the database, and make sure the correct objects are setup

    :return: whether or not the connection was successful
    """
    successful_connection = False

    try:
        successful_connection = db.connect()
        logger.log_db('Connecting to database', successful_connection)

        db_tables = db.get_tables()

        # create the proper objects if there aren't any
        if len(db_tables) < len(models.all_models()):
            db.create_tables(models.all_models())
            logger.log_db('Created new object tables {}'.format(
                [table.__name__ for table in models.all_models() if table not in db_tables]
            ))
    except OperationalError as e:
        logger.log_db(e)

    return successful_connection
