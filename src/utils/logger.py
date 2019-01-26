import datetime
import time

from src import settings

LOG_FILE_NAME = 'src/data/logs.txt'
LOG_KEEP = []
LAST_WRITE = datetime.datetime.utcnow()


def log(comment):
    say_and_keep(f'{date_time()} {comment}')


def log_command(author, command, issued=True):
    if issued:
        log(f'{author} issued command "{command}"')
    else:
        log(f'{author} finished command "{command}"')


def log_db(action, returned=None):
    if returned:
        log(f'{action} returned "{returned}"')
    else:
        log(f'{action}')


def log_world_task(task, action):
    log(f'[World Task: {task.__name__}] {action}')


def date_time():
    return f'[{time.strftime("%x %X")}]'


def say_and_keep(message):
    print(message)  # output to console
    LOG_KEEP.append(message)  # keep the message for now

    # check if the log delay has been passed since last file write_logs
    if datetime.datetime.utcnow() - LAST_WRITE >= datetime.timedelta(minutes=settings.LOG_DELAY):
        write_logs()


def write_logs(filename=LOG_FILE_NAME, logout=False):
    if len(LOG_KEEP) == 0 and not logout:
        return

    # copy the logs, then clear the old ones
    old_logs = LOG_KEEP.copy()
    LOG_KEEP.clear()
    # append an empty string so we get a newline at the end, or we get chunky logs, no one wants chunky logs
    old_logs.append('')

    global LAST_WRITE
    LAST_WRITE = datetime.datetime.utcnow()

    with open(filename, 'a') as f:
        if logout:
            print(f'{date_time()} Finished logging, appending new lines')
            LOG_KEEP.append('\n\n')
        else:
            print(f'{date_time()} Writing logs to "{filename}"')

        f.write('\n'.join(old_logs))
    print(f'{date_time()} Finished writing logs to "{filename}"')
