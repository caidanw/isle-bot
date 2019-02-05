import asyncio

from discord import Client, User, TextChannel

from src import settings
from src.game.enums.reaction import Reaction
from src.ui.reaction_menu import ReactionMenu

REACTIONS = [Reaction.DISMISS.value, Reaction.CONFIRM.value]


class ConfirmMenu(ReactionMenu):
    def __init__(self, client: Client, channel: TextChannel, messages: list):
        super().__init__(client, channel, messages, REACTIONS)

    async def wait_for_user_reaction(self, target_user: User=None):
        if self.message_literal is None:
            raise ValueError('Message has not been sent yet, send a message before waiting for the response.')

        def check(reaction, user):
            if not user.bot:
                if target_user and user == self.message_literal.author:
                    return str(reaction.emoji) in self.reactions and user == target_user
                else:
                    return str(reaction.emoji) in self.reactions
            return False

        try:
            response = await self.client.wait_for('reaction_add', check=check, timeout=settings.DEFAULT_TIMEOUT)
        except asyncio.TimeoutError:
            await self.clear()
            return None

        if response:
            emoji_code = str(response[0])
            await self.message_literal.edit(content=self.reaction_messages.get(emoji_code))
            return emoji_code == Reaction.CONFIRM.value  # if the confirm button was clicked, then return true
        else:
            await self.clear()
            return None
