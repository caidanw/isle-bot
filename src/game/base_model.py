from peewee import Model

from utils.cache import db


class BaseModel(Model):
    class Meta:
        database = db
