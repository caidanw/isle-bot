import configparser

CONFIG_PATH = 'src/data/config.ini'

config = configparser.ConfigParser()
config.read(CONFIG_PATH)


# ==================
# Configuration data
# ==================

DEBUGGING = bool(int(config.get('bot', 'debugging')))
TOKEN = config.get('bot', 'token')
DEV_TOKEN = config.get('bot', 'dev_token')


def get_token():
    token = DEV_TOKEN if DEBUGGING else TOKEN

    if token is None:
        token_key = 'dev_token' if DEBUGGING else 'token'
        raise ValueError(f'IsleBot "{token_key}" not found in {CONFIG_PATH}')

    return token


# ================
# Message settings
# ================

# how long to wait until delete message (for reducing spam)
DEFAULT_DELETE_DELAY = int(config.get('message', 'default_delete_delay'))  # in seconds

# how long to wait until a client stops waiting for a reaction or message
DEFAULT_TIMEOUT = int(config.get('message', 'default_timeout'))  # in seconds

LOG_DELAY = int(config.get('message', 'log_delay'))  # in seconds


# =================
# Security settings
# =================

DEVELOPER_IDS = [int(dev[1]) for dev in config.items('developers')]

