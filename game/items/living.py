from discord import User

from game.items.items import Item
from ui.level_up_menu import LevelUpMenu


class Fairy(Item):
    def __init__(self):
        super().__init__('fairy', 10, consumable=True)

    async def consume(self, client, user: User):
        dm_channel = user.dm_channel
        if dm_channel is None:
            dm_channel = await user.create_dm()

        lum = LevelUpMenu(client, dm_channel, user, level_amt=2)
        await lum.send()
        succeeded = await lum.wait_for_user_reaction(user)
        await lum.clear()
        return succeeded

