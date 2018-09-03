import datetime
import time

import settings

LOG_FILE_NAME = 'data/logs.txt'
LOG_KEEP = []
LAST_WRITE = datetime.datetime.utcnow()


def log_command(author, command, issued=True):
    dt = date_time()
    if issued:
        say_and_keep(f'{dt} {author} issued command "{command}"')
    else:
        say_and_keep(f'{dt} {author} finished command "{command}"')


def log_db(action, returned=None):
    dt = date_time()
    if returned:
        say_and_keep(f'{dt} {action} returned "{returned}"')
    else:
        say_and_keep(f'{dt} {action}')


def log(comment, force_write=False):
    say_and_keep(f'{date_time()} {comment}')
    if force_write:
        write_logs(LOG_FILE_NAME)


def date_time():
    return f'[{time.strftime("%x %X")}]'


def say_and_keep(message):
    print(message)  # output to console
    LOG_KEEP.append(message)  # keep the message for now

    # check if the log delay has been passed since last file write_logs
    if datetime.datetime.utcnow() - LAST_WRITE >= datetime.timedelta(minutes=settings.LOG_DELAY):
        write_logs(LOG_FILE_NAME)


def write_logs(filename):
    if len(LOG_KEEP) == 0:
        return

    global LAST_WRITE
    LAST_WRITE = datetime.datetime.utcnow()

    with open(filename, 'a') as f:
        print(f'{date_time()} Writing logs to {filename}\n\n')
        f.write('\n'.join(LOG_KEEP))
        LOG_KEEP.clear()
