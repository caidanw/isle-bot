from datetime import datetime
import random

from peewee import *

from game.base_model import BaseModel
from game.guild import Guild


class Island(BaseModel):
    """
    Island class used to represent an area a Guild can own,
    and a place for Players to harvest Resources.
    """

    guild = ForeignKeyField(Guild, backref='islands')
    name = CharField(default='Lost Island')
    claimed = BooleanField(default=False)
    size = IntegerField(default=random.randint(300, 800))
    claimed_at = DateTimeField(default=datetime.now())

    def get_resource(self, name):
        """ Get a Resource by name that is located on the this Island

        :param name: of the resource
        :return: a resource if found by the name
        """
        for resource in self.resources:
            if resource.name == name:
                return resource
        return None

    def add_resource(self, resource):
        """ Add a Resource to this current Island

        :param resource: to add
        """
        resource.on_island = self
        resource.save()
