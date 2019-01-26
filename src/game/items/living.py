from discord import User

from src.game.items.items import Living
from src.ui.level_up_menu import LevelUpMenu


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

