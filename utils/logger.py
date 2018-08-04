import time


def log_command(author, command, issued=True):
    if issued:
        print(f'[{time.strftime("%X")}] {author} issued command "{command}"')
    else:
        print(f'[{time.strftime("%X")}] {author} finished command "{command}"')


def log_db(action, returned=None):
    if returned:
        print(f'[{time.strftime("%X")}] {action} returned "{returned}"')
    else:
        print(f'[{time.strftime("%X")}] {action}')


def log(comment):
    print(f'[{time.strftime("%X")}] {comment}')
