from peewee import Model

from src.utils.cache import db


class BaseModel(Model):
    class Meta:
        database = db
