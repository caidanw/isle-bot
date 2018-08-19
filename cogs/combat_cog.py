import asyncio

from discord.ext import commands

import settings
from game.game import Game
from ui.combat_menu import CombatMenu
from ui.confirm_message import ConfirmMessage
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
        if target_player is None:
            return await channel.send(f'The player "{target_player_name}" does not exist, are they using an alias?')

        if player.get_location.id != target_player.get_location.id:
            return await channel.send('You must be in the same area to fight this player.')

        target_author = self.bot.get_user(target_player.uuid)
        if target_author:
            # get the author's private channel, so we can let them know the request has been sent
            author_dm = author.dm_channel if author.dm_channel else await author.create_dm()

            request_status_msg = await author_dm.send(f'Request has been delivered to {target_player.username}')

            # get the target author's private channel, so we can send them a request
            target_dm = target_author.dm_channel if target_author.dm_channel else await target_author.create_dm()

            fight_request_msg = ConfirmMessage(self.bot, target_dm,
                                               [f'{player.username} has requested to fight you.',
                                                'You declined the request.',
                                                'You accepted the request, waiting to fight.'])

            await fight_request_msg.send()
            accepted_request = await fight_request_msg.wait_for_user_reaction(target_player)

            if not accepted_request:
                return await request_status_msg.edit(
                    content=f'{target_player.username} has declined the request to fight.',
                    delete_after=settings.DEFAULT_DELETE_DELAY
                )
            else:
                await target_dm.send(f'Waiting for {player.username} to finish their turn.')

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

        p1_user = self.bot.get_user(player_1.uuid)
        p2_user = self.bot.get_user(player_2.uuid)

        # get both player stats TODO: replace with player's real values
        p1_health, p1_dmg, p1_def = 3, 2, 1
        p2_health, p2_dmg, p2_def = 3, 2, 1
        player_1.health, player_1.damage, player_1.defense = p1_health, p1_dmg, p1_def
        player_2.health, player_2.damage, player_2.defense = p2_health, p2_dmg, p2_def

        first_round = True
        fighting = True
        while fighting:
            await asyncio.sleep(3)

            p1_action = None
            p2_action = None

            if first_round:
                # send the initial messages
                await p1_menu.send()
                p1_action = await p1_menu.wait_for_user_reaction(p1_user)

                await p2_menu.send()
                p2_action = await p2_menu.wait_for_user_reaction(p2_user)

                first_round = False
            else:
                # reset for a new round
                await p1_menu.reset()
                p1_action = await p1_menu.wait_for_user_reaction(p1_user)

                await p2_menu.reset()
                p2_action = await p2_menu.wait_for_user_reaction(p2_user)

            p1_msg, p2_msg = await self.handle_combat_actions(player_1, p1_action, player_2, p2_action)

            p1_msg += f'```\nHealth : {player_1.health} \nDamage : {player_1.damage} \nDefense: {player_1.defense}\n```'
            p2_msg += f'```\nHealth : {player_2.health} \nDamage : {player_2.damage} \nDefense: {player_2.defense}\n```'

            await p1_dm.send(p1_msg)
            await p2_dm.send(p2_msg)

            # todo: add support for surrendering
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

    @staticmethod
    async def handle_combat_actions(player_1, p1_action, player_2, p2_action):
        p1_action = 'passed' if p1_action is None else p1_action
        p2_action = 'passed' if p2_action is None else p2_action

        p1_desc = combat_helper.combat_descriptions.get(p1_action)
        p2_desc = combat_helper.combat_descriptions.get(p2_action)

        p1_msg = p1_desc.get(p2_action, 'No support for current action')
        p2_msg = p2_desc.get(p1_action, 'No support for current action')

        if p1_action == 'passed':
            if p2_action == 'passed':
                p1_msg = p1_msg.format(username=player_2.username)
                p2_msg = p2_msg.format(username=player_1.username)
            elif p2_action == Reaction.CROSSED_SWORDS:
                actual_damage = combat_helper.get_critical_damage(player_2.damage)
                player_1.health -= actual_damage

                p1_msg = p1_msg.format(username=player_2.username, received_dmg=actual_damage)
                p2_msg = p2_msg.format(username=player_1.username, dealt_dmg=actual_damage)
            elif p2_action == Reaction.SHIELD:
                actual_damage = combat_helper.get_damage_after_defense(player_1.damage, player_2.defense)
                player_2.health -= actual_damage

                p1_msg = p1_msg.format(username=player_2.username)
                p2_msg = p2_msg.format(username=player_1.username)
            elif p2_action == Reaction.PACKAGE:
                pass
            elif p2_action == Reaction.WHITE_FLAG:
                pass
        elif p1_action == Reaction.CROSSED_SWORDS:
            if p2_action == 'passed':
                actual_damage = combat_helper.get_critical_damage(player_1.damage)
                player_2.health -= actual_damage

                p1_msg = p1_msg.format(username=player_2.username, dealt_dmg=actual_damage)
                p2_msg = p2_msg.format(username=player_1.username, received_dmg=actual_damage)
            elif p2_action == Reaction.CROSSED_SWORDS:
                player_1.health -= player_2.damage
                player_2.health -= player_1.damage

                p1_msg = p1_msg.format(username=player_2.username, dealt_dmg=player_1.damage, received_dmg=player_2.damage)
                p2_msg = p2_msg.format(username=player_1.username, dealt_dmg=player_2.damage, received_dmg=player_1.damage)
            elif p2_action == Reaction.SHIELD:
                actual_damage = combat_helper.get_damage_after_defense(player_1.damage, player_2.defense)
                player_2.health -= actual_damage

                p1_msg = p1_msg.format(username=player_2.username, dealt_dmg=actual_damage)
                p2_msg = p2_msg.format(username=player_1.username, blocked_dmg=player_2.defense, received_dmg=actual_damage)
            elif p2_action == Reaction.PACKAGE:
                pass
            elif p2_action == Reaction.WHITE_FLAG:
                pass
        elif p1_action == Reaction.SHIELD:
            if p2_action == 'passed':
                p1_msg = p1_msg.format(username=player_2.username)
                p2_msg = p2_msg.format(username=player_1.username)
            elif p2_action == Reaction.CROSSED_SWORDS:
                actual_damage = combat_helper.get_damage_after_defense(player_2.damage, player_1.defense)
                player_1.health -= actual_damage

                p1_msg = p1_msg.format(username=player_2.username, blocked_dmg=player_1.defense, received_dmg=actual_damage)
                p2_msg = p2_msg.format(username=player_1.username, dealt_dmg=actual_damage)
            elif p2_action == Reaction.SHIELD:
                p1_msg = p1_msg.format(username=player_2.username)
                p2_msg = p2_msg.format(username=player_1.username)
            elif p2_action == Reaction.PACKAGE:
                pass
            elif p2_action == Reaction.WHITE_FLAG:
                pass
        elif p1_action == Reaction.PACKAGE:
            if p2_action == 'passed':
                pass
            elif p2_action == Reaction.CROSSED_SWORDS:
                pass
            elif p2_action == Reaction.SHIELD:
                pass
            elif p2_action == Reaction.PACKAGE:
                pass
            elif p2_action == Reaction.WHITE_FLAG:
                pass
        elif p1_action == Reaction.WHITE_FLAG:
            if p2_action == 'passed':
                pass
            elif p2_action == Reaction.CROSSED_SWORDS:
                pass
            elif p2_action == Reaction.SHIELD:
                pass
            elif p2_action == Reaction.PACKAGE:
                pass
            elif p2_action == Reaction.WHITE_FLAG:
                pass

        p1_msg = f'```\n{p1_msg}\n```'
        p2_msg = f'```\n{p2_msg}\n```'

        return p1_msg, p2_msg


def setup(bot):
    bot.add_cog(CombatCog(bot))
