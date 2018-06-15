import time


def log_command(author, command, issued=True):
    if issued:
        print('[{}] {} issued command \'{}\''.format(time.strftime('%X'), author, command))
    else:
        print('[{}] {} finished command \'{}\''.format(time.strftime('%X'), author, command))
