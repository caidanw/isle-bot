from discord import Client, Channel, User


class ReactionMessage:
    TIMEOUT = 20

    def __init__(self, client: Client, channel: Channel, messages: list, reactions: list):
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
        self.message_literal = await self.client.send_message(self.channel, self.initial_message)
        for emoji in self.reactions:
            await self.client.add_reaction(self.message_literal, emoji)

    async def wait_for_user_reaction(self, target_user: User=None):
        if self.message_literal is None:
            return

        def check(reaction, user):
            if user:
                return str(reaction.emoji) in self.reactions and user == target_user
            return str(reaction.emoji) in self.reactions

        response = await self.client.wait_for_reaction(message=self.message_literal, check=check, timeout=self.TIMEOUT)
        await self.client.edit_message(self.message_literal, self.reaction_messages.get(str(response.reaction.emoji)))
