import asyncio

from discord import Client, TextChannel

from src import settings


class ReactionMenu:

    def __init__(self, client: Client, channel: TextChannel, messages: list, reactions: list):
        self.client = client
        self.channel = channel
        self.message_literal = None
        self.initial_message = messages.pop(0)
        self.reactions = reactions

        if len(reactions) == len(messages):
            # for the remaining messages, assign them to the reactions
            # the order of the messages and reactions is how they will be assigned to each other
            self.reaction_messages = dict(zip(reactions, messages))
        else:
            raise ValueError('The length of messages must be the same length as reactions. '
                             'Minus the first index in messages, as that is used as the initial message.')

    async def send(self):
        self.message_literal = await self.channel.send(self.initial_message)
        for emoji in self.reactions:
            await self.message_literal.add_reaction(emoji)

    async def clear(self):
        if self.message_literal is not None:
            await self.message_literal.delete()
            self.message_literal = None

    async def wait_for_user_reaction(self, target_user):
        if self.message_literal is None:
            raise ValueError('Message has not been sent yet, send a message before waiting for the response.')

        def check(reaction, user):
            if not user.bot:
                if target_user is not None:
                    return str(reaction.emoji) in self.reactions and user == target_user
                else:
                    return str(reaction.emoji) in self.reactions
            return False

        try:
            response = await self.client.wait_for('reaction_add', check=check, timeout=settings.DEFAULT_TIMEOUT)
        except asyncio.TimeoutError:
            return await self.clear()

        emoji_code = str(response[0])
        await self.message_literal.edit(content=self.reaction_messages.get(emoji_code))
