import time


def log_command(author, command, issued=True):
    if issued:
        print('[{}] {} issued command \'{}\''.format(time.strftime('%X'), author, command))
    else:
        print('[{}] {} finished command \'{}\''.format(time.strftime('%X'), author, command))


def log_db(action, returned=None):
    if returned:
        print('[{}] {} returned \'{}\''.format(time.strftime('%X'), action, returned))
    else:
        print('[{}] {}'.format(time.strftime('%X'), action))


def log(comment):
    print('[{}] {}'.format(time.strftime('%X'), comment))
