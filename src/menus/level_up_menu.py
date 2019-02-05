import asyncio

from src import settings
from src.game.game import Game
from src.game.enums.reaction import Reaction
from src.ui.reaction_menu import ReactionMenu

MESSAGES = ['Choose a stat to level up.',
            'You chose to level up vigor.',
            'You chose to level up strength.',
            'You chose to level up dexterity.',
            'You chose to level up fortitude.']

REACTIONS = [Reaction.HEART.value,   # vigor
             Reaction.MUSCLE.value,  # strength
             Reaction.RUNNER.value,  # dexterity
             Reaction.SHIELD.value]  # fortitude


class LevelUpMenu(ReactionMenu):
    def __init__(self, client, channel, user, level_amt):
        self.player = Game.get_player(user)
        self.level_amount = level_amt

        super().__init__(client, channel, MESSAGES.copy(), REACTIONS)

    async def wait_for_user_reaction(self, target_user):
        if self.message_literal is None:
            raise ValueError('Message has not been sent yet, send a message before waiting for the response.')

        def check(reaction, user):
            if not user.bot:
                return str(reaction.emoji) in self.reactions and user == target_user
            return False

        try:
            response = await self.client.wait_for('reaction_add', check=check, timeout=settings.DEFAULT_TIMEOUT)
        except asyncio.TimeoutError:
            await self.channel.send('You waited to long, try again.')
            return False

        emoji_code = str(response[0])
        await self.message_literal.edit(content=self.reaction_messages.get(emoji_code))

        reaction = Reaction(emoji_code)
        stats = self.player.stats

        if reaction == Reaction.HEART:
            stats.increase_vigor(self.level_amount)
            stat = 'vigor'
        elif reaction == Reaction.MUSCLE:
            stats.increase_strength(self.level_amount)
            stat = 'strength'
        elif reaction == Reaction.RUNNER:
            stats.increase_dexterity(self.level_amount)
            stat = 'dexterity'
        elif reaction == Reaction.SHIELD:
            stats.increase_fortitude(self.level_amount)
            stat = 'fortitude'

        await self.channel.send(f'You have leveled up your {stat}.')
        return True
