import pickle
from pathlib import Path

root_dir = 'data/'
extension = '.p'


def validate(filename):
    return Path(root_dir + filename + extension).is_file()


def save(obj, filename):
    with open(root_dir + filename + extension, 'wb') as filehandler:
        pickle.dump(obj, filehandler)


def load(filename):
    with open(root_dir + filename + extension, 'rb') as filehandler:
        return pickle.load(filehandler)
