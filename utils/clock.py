import time


def server_clock():
    return 'Date: {} | Time: {}'.format(time.strftime('%x'), time.strftime('%X'))


def format_time(seconds):
    if seconds >= 60:
        minutes = seconds // 60
        seconds %= 60
        return '{}:{}s'.format(str(minutes).zfill(2), str(seconds).zfill(2))
    else:
        return '{}s'.format(str(seconds).zfill(2))
