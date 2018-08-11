import time


def log_command(author, command, issued=True):
    dt = date_time()
    if issued:
        print(f'[{dt}] {author} issued command "{command}"')
    else:
        print(f'[{dt}] {author} finished command "{command}"')


def log_db(action, returned=None):
    dt = date_time()
    if returned:
        print(f'[{dt}] {action} returned "{returned}"')
    else:
        print(f'[{dt}] {action}')


def log(comment):
    print(f'[{date_time()}] {comment}')


def date_time():
    return time.strftime('%x %X')
