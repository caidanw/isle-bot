from src.utils.cache import Cache


CONFIG_DIR = 'src/data/config.json'


""" Configuration data """

DEBUGGING = Cache.get_from_json(CONFIG_DIR)['debugging']


def get_token():
    if DEBUGGING:
        token = Cache.get_from_json(CONFIG_DIR)['dev_token']
    else:
        token = Cache.get_from_json(CONFIG_DIR)['token']

    if token is None:
        token_key = 'dev_token' if DEBUGGING else 'token'
        raise ValueError(f'IsleBot "{token_key}" not found in {CONFIG_DIR}')

    return token


""" Message settings """

# how long to wait until delete message (for reducing spam)
DEFAULT_DELETE_DELAY = 60  # in seconds

# how long to wait until a client stops waiting for a reaction or message
DEFAULT_TIMEOUT = 30  # in seconds

LOG_DELAY = 10


""" Security settings """

DEVELOPER_IDS = [
    178948814256734208  # mildmelon#5380 lead developer
]

