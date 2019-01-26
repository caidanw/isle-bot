import time


def server_clock():
    return f'Date: {time.strftime("%x")} | Time: {time.strftime("%X")}'


def format_time(seconds):
    if seconds >= 60:
        minutes = seconds // 60
        seconds %= 60
        return f'{str(minutes).zfill(2)}:{str(seconds).zfill(2)}s'
    else:
        return f'{str(seconds).zfill(2)}s'
