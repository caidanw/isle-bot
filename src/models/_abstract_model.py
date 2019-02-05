from peewee import Model

from src.utils.cache import db


class AbstractModel(Model):
    class Meta:
        database = db
