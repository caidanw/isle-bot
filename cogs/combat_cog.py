import asyncio

from discord.ext import commands

import settings
from game.game import Game
from ui.combat_menu import CombatMenu
from ui.confirm_menu import ConfirmMenu
from ui.reaction import Reaction
from utils import combat_helper


class CombatCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['kill'])
    async def fight(self, context, *target_player_name):
        """ Fight another player to the death, or until one of you wusses out. """
        channel = context.message.channel
        author = context.message.author
        player = Game.get_player(author)

        target_player_name = ' '.join(target_player_name)
        if target_player_name == '':
            return await channel.send('You must enter the player you wish to fight. Try "?help fight"')

        target_player = Game.get_player_by_name(target_player_name)
        target_author = self.bot.get_user(target_player.uuid)
        if target_player is None or target_author is None:
            return await channel.send(f'The player "{target_player_name}" does not exist, are they using an alias?')

        if player.get_location.id != target_player.get_location.id:
            return await channel.send('You must be in the same area to fight this player.')

        # get the author's private channel, so we can let them know the request has been sent
        author_dm = author.dm_channel if author.dm_channel else await author.create_dm()

        request_status_msg = await author_dm.send(f'Request has been delivered to {target_player.username}')

        # get the target author's private channel, so we can send them a request
        target_dm = target_author.dm_channel if target_author.dm_channel else await target_author.create_dm()

        fight_request_msg = ConfirmMenu(self.bot, target_dm,
                                        [f'{player.username} has requested to fight you.',
                                            'You declined the request.',
                                            'You accepted the request, waiting to fight.'])

        await fight_request_msg.send()
        accepted_request = await fight_request_msg.wait_for_user_reaction(target_player)

        if not accepted_request:
            await request_status_msg.edit(
                content=f'{target_player.username} has declined the request to fight.',
                delete_after=settings.DEFAULT_DELETE_DELAY
            )
            await asyncio.sleep(3)
            return await fight_request_msg.message_literal.delete()
        else:
            await author_dm.send(f'You and {target_player.username} find an open field, away from others.')
            await target_dm.send(f'You and {player.username} find an open field, away from others.')

        # if all went well and the fight was accepted, then we can start a fight between the two players
        p1_dm = author.dm_channel
        if not p1_dm:
            p1_dm = await author.create_dm()

        p2_dm = target_author.dm_channel
        if not p2_dm:
            p2_dm = await target_author.create_dm()

        await self.conduct_fight(player, p1_dm, target_player, p2_dm)

    async def conduct_fight(self, player_1, p1_dm, player_2, p2_dm):
        # create combat menus for both players
        p1_menu = CombatMenu(self.bot, p1_dm)
        p2_menu = CombatMenu(self.bot, p2_dm)

        # find the discord users associated with the players
        p1_user = self.bot.get_user(player_1.uuid)
        p2_user = self.bot.get_user(player_2.uuid)

        # get both player stats TODO: replace with player's real values
        p1_health, p1_dmg, p1_def = 5, 2, 1
        p2_health, p2_dmg, p2_def = 5, 2, 1
        player_1.health, player_1.damage, player_1.defense = p1_health, p1_dmg, p1_def
        player_2.health, player_2.damage, player_2.defense = p2_health, p2_dmg, p2_def

        fighting = True
        while fighting:
            
            """ Send the combat menus to each player, one at a time. """

            # send a message to the second player to let them know they are waiting
            courtesy_message = await p2_dm.send(f'Waiting for {player_1.username} to choose an action.')

            # present the first player with combat menu
            await p1_menu.send()
            p1_action = await p1_menu.wait_for_user_reaction(p1_user)

            await courtesy_message.delete()  # delete unwanted message

            # send a message to p1 to let them know they are waiting
            courtesy_message = await p1_dm.send(f'Waiting for {player_2.username} to choose an action.')

            # present the second player with combat menu
            await p2_menu.send()
            p2_action = await p2_menu.wait_for_user_reaction(p2_user)

            await courtesy_message.delete()

            """ Handle combat input determined from the players, and send them the descriptions of their actions. """

            p1_msg, p2_msg = await combat_helper.handle_combat_actions(player_1, p1_action, player_2, p2_action)

            p1_msg += f'```\nHealth : {player_1.health} \nDamage : {player_1.damage} \nDefense: {player_1.defense}\n```'
            p2_msg += f'```\nHealth : {player_2.health} \nDamage : {player_2.damage} \nDefense: {player_2.defense}\n```'

            await p1_dm.send(p1_msg)
            await p2_dm.send(p2_msg)

            """ Check if either play has died or surrendered. """

            if player_1.health <= 0 or player_2.health <= 0:
                await p1_menu.message_literal.delete()
                await p2_menu.message_literal.delete()

                fight_end_msg = 'The fight has ended, {username} has won!'

                if player_1.health > 0:
                    fight_end_msg = fight_end_msg.format(username=player_1.username)
                elif player_2.health > 0:
                    fight_end_msg = fight_end_msg.format(username=player_2.username)
                else:
                    fight_end_msg = 'No one won, you both died. Great job.'

                await p1_dm.send(fight_end_msg)
                await p2_dm.send(fight_end_msg)

                fighting = False
            elif p1_action == Reaction.WHITE_FLAG or p2_action == Reaction.WHITE_FLAG:
                await p1_menu.message_literal.delete()
                await p2_menu.message_literal.delete()

                fight_end_msg = 'The fight has ended, {loser} has surrendered, {winner} has won!'

                p1_surrendered = p1_action == Reaction.WHITE_FLAG
                p2_surrendered = p2_action == Reaction.WHITE_FLAG

                if p1_surrendered and p2_surrendered:
                    fight_end_msg = 'The fight has ended, you both surrendered, bunch of cowards.'
                elif p1_surrendered:
                    fight_end_msg = fight_end_msg.format(loser=player_1.username, winner=player_2.username)
                elif p2_surrendered:
                    fight_end_msg = fight_end_msg.format(loser=player_2.username, winner=player_1.username)

                await p1_dm.send(fight_end_msg)
                await p2_dm.send(fight_end_msg)

                fighting = False


def setup(bot):
    bot.add_cog(CombatCog(bot))
