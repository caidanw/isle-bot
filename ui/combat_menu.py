from concurrent import futures

from discord import Client, TextChannel, User

from ui.reaction import Reaction
from ui.reaction_message import ReactionMessage

MESSAGES = ['Choose an action...',
            'You chose to attack.',  # attack
            'You chose to defend.',  # defend
            'You chose to use an item.',  # use item
            'You chose to surrender.']  # surrender
REACTIONS = [Reaction.CROSSED_SWORDS.value, Reaction.SHIELD.value, Reaction.PACKAGE.value, Reaction.WHITE_FLAG.value]


class CombatMenu(ReactionMessage):
    def __init__(self, client: Client, channel: TextChannel):
        super().__init__(client, channel, MESSAGES.copy(), REACTIONS)

    async def reset(self):
        await self.message_literal.delete()
        await self.send()

    async def wait_for_user_reaction(self, target_user: User=None, timeout=10):
        if self.message_literal is None:
            raise ValueError('Message has not been sent yet, send a message before waiting for the response.')
        if target_user is None:
            raise ValueError('target_user must not be none for combat.')

        def check(reaction, user):
            if not user.bot:
                return str(reaction.emoji) in self.reactions and user == target_user
            return False

        try:
            response = await self.client.wait_for('reaction_add', check=check, timeout=timeout)
        except futures.TimeoutError:
            response = None

        if response:
            emoji_code = str(response[0])
            await self.message_literal.edit(content=self.reaction_messages.get(emoji_code))
            return Reaction(emoji_code)
        else:
            await self.message_literal.edit(content='You did not choose an action in time, passing turn.')
            return None
