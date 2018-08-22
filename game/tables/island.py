from datetime import datetime
import random

from peewee import *

from game.base_model import BaseModel
from game.union import Union


class Island(BaseModel):
    """
    Island class used to represent an area a Union can own,
    and a place for Players to harvest Resources.
    """

    union = ForeignKeyField(Union, backref='islands', null=True)
    union_number = IntegerField(default=0)  # islands with a 0 are claimable
    name = CharField(default='Lost Island')
    size = IntegerField(default=random.randint(300, 800))
    claimed = BooleanField(default=False)
    claimed_at = DateTimeField(default=datetime.now())

    @property
    def owner(self):
        return self.union

    def get_amount_of_resources(self, name):
        from game.resource import Resource
        return self.resources.select(fn.COUNT(Resource.name)).where(Resource.name == name).scalar()

    def get_resource(self, name, number=1):
        """ Get a Resource by name that is located on the this Island

        :param name: of the resource
        :param number: the specific resource to find
        :return: a resource if found by the name
        """
        if '#' in name:
            split_name = name.split('#')
            name = split_name[0]
            try:
                num = int(split_name[1])
                if num < 1:
                    raise ValueError
                number = num
            except ValueError:
                return f'"{split_name[1]}" is not a valid number.'

        for resource in self.resources:
            if resource.name == name and resource.number == number:
                return resource
        return None

    def add_resource(self, resource):
        """ Add a Resource to this current Island

        :param resource: to add
        """
        resource.island = self
        resource.save()
