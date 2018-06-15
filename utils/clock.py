import time


def server_clock():
    return 'Date: {} | Time: {}'.format(time.strftime('%x'), time.strftime('%X'))
