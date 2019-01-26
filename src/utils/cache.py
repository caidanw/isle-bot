import json

from peewee import SqliteDatabase

db = SqliteDatabase('data/universe.db', pragmas={
    'cache_size': -1024 * 32,  # Set cache size to 32MB for *current connection*
    'journal_mode': 'wal',
    'foreign_keys': 'on'
})


class Cache:
    json_cache = {}

    @classmethod
    def get_from_json(cls, filename):
        """ Store the json data in a cache so we don't make as many I/O file operations. """
        if filename not in cls.json_cache:
            with open(filename) as file:
                json_data = json.load(file)
                cls.json_cache[filename] = json_data
        return cls.json_cache.get(filename)

    @classmethod
    def clear_json_cache(cls):
        """ This may want to be called based on how often the json files change. """
        cls.json_cache = {}
