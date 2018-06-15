from datetime import datetime
import random

from game.resource import Resource


class Island:
    def __init__(self, guild, name=None):
        self.guild = guild
        if guild:
            self.name = name if not None else '{} island'.format(guild.name)
            self.claimed = True
        else:
            self.name = 'lost island'
            self.claimed = False
        self.size = random.randint(30, 800)
        self.claimed_at = datetime.now().isoformat()
        self.days_since_claimed = 0
        self.resources = []
        self.populate_resources()

    def get_resource(self, name):
        for resource in self.resources:
            if resource.name == name:
                return resource
        return None

    def populate_resources(self):
        for resource in range(5):
            self.resources.append(Resource.random(50, 500))
