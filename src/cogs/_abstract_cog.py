class AbstractCog:
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    # Need to add a setup function or discord.py will complain
    # This cog will not show up in the help command menu
    pass
