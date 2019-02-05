from discord import User

from src.game.items.material import Material
from src.menus.level_up_menu import LevelUpMenu


class Living(Material):
    def __init__(self, name, harvest_time):
        super().__init__(name, harvest_time, consumable=True)


class Fairy(Living):
    def __init__(self):
        super().__init__('fairy', 10)

    async def consume(self, client, user: User):
        dm_channel = user.dm_channel
        if dm_channel is None:
            dm_channel = await user.create_dm()

        lum = LevelUpMenu(client, dm_channel, user, level_amt=2)
        await lum.send()
        succeeded = await lum.wait_for_user_reaction(user)
        await lum.clear()
        return succeeded

