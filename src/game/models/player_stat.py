from peewee import IntegerField

from src.game import BaseModel


class PlayerStat(BaseModel):
    vigor = IntegerField(default=5)      # increases the base amount of max health
    strength = IntegerField(default=1)   # increases the base amount of damage dealt
    dexterity = IntegerField(default=1)  # increases the base chance to successfully land an attack
    fortitude = IntegerField(default=1)  # increases the base amount of damage blocked

    def set_vigor(self, amount):
        self.vigor = amount
        self.save()

    def increase_vigor(self, amount):
        self.set_vigor(self.vigor + amount)

    def set_strength(self, amount):
        self.strength = amount
        self.save()

    def increase_strength(self, amount):
        self.set_strength(self.strength + amount)

    def set_dexterity(self, amount):
        self.dexterity = amount
        self.save()

    def increase_dexterity(self, amount):
        self.set_dexterity(self.dexterity + amount)

    def set_fortitude(self, amount):
        self.fortitude = amount
        self.save()

    def increase_fortitude(self, amount):
        self.set_fortitude(self.fortitude + amount)
