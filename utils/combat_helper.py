from ui.reaction import Reaction

combat_descriptions = {
    Reaction.NO_ENTRY_SIGN: {
        Reaction.NO_ENTRY_SIGN: 'You stare, {opponent} stares. It\'s awkward.',
        Reaction.CROSSED_SWORDS: 'You stare, and {opponent} attacks. '
                                 'You took a critical hit worth {received_dmg} damage',
        Reaction.SHIELD: 'You stare, and {opponent} defends against your glare. Nothing happens.',
        Reaction.PACKAGE: 'You stare, while {opponent} uses an item.',
        Reaction.WHITE_FLAG: 'You stare, and {opponent} surrenders. Your stare was very effective.'
    },
    Reaction.CROSSED_SWORDS: {
        Reaction.NO_ENTRY_SIGN: 'You attack, and {opponent} does nothing.'
                                'You landed a critical attack worth {dealt_dmg} damage.',
        Reaction.CROSSED_SWORDS: 'You attack, and {opponent} attacks. '
                                 'You dealt {dealt_dmg} damage, and took {received_dmg} damage',
        Reaction.SHIELD: 'You attack, but {opponent} blocked your attack. You dealt {dealt_dmg} damage.',
        Reaction.PACKAGE: 'You attack, and {opponent} used an item. You dealt {dealt_dmg} damage.',
        Reaction.WHITE_FLAG: 'You attack, but {opponent} surrendered. You dealt {dealt_dmg} damage.'
    },
    Reaction.SHIELD: {
        Reaction.NO_ENTRY_SIGN: 'You defend, and {opponent} did nothing. {opponent} stares deeply into your soul.',
        Reaction.CROSSED_SWORDS: 'You defended, and {opponent} attacks. '
                                 'You blocked {blocked_dmg} damage, and took {received_dmg} damage',
        Reaction.SHIELD: 'You defended, and {opponent} defend. Nothing happens.',
        Reaction.PACKAGE: 'You defended, and {opponent} used an item.',
        Reaction.WHITE_FLAG: 'You defended, and {opponent} surrendered.'
    },
    Reaction.PACKAGE: {
        Reaction.NO_ENTRY_SIGN: 'You use an item, while {opponent} stares at you.',
        Reaction.CROSSED_SWORDS: 'You use an item, while {opponent} attacks. You took {received_dmg} damage.',
        Reaction.SHIELD: 'You use an item, and {opponent} defends. Nothing happens.',
        Reaction.PACKAGE: 'You use an item, and {opponent} uses an item.',
        Reaction.WHITE_FLAG: 'You use an item, while {opponent} surrenders.'
    },
    Reaction.WHITE_FLAG: {
        Reaction.NO_ENTRY_SIGN: 'You surrender, while {opponent} stares at you.',
        Reaction.CROSSED_SWORDS: 'You surrender, and {opponent} attacks. You take {received_dmg} damage.',
        Reaction.SHIELD: 'You surrender, and {opponent} defends.',
        Reaction.PACKAGE: 'You surrender, while {opponent} uses an item.',
        Reaction.WHITE_FLAG: 'You surrender, and {opponent} surrenders.'
    }
}


def get_critical_damage(damage):
    return damage * 2


def get_damage_after_defense(damage, defense):
    actual_damage = damage - defense
    if actual_damage < 0:
        return 0
    return actual_damage


async def handle_combat_actions(player_1, p1_action, player_2, p2_action):
    p1_desc = combat_descriptions.get(p1_action)
    p2_desc = combat_descriptions.get(p2_action)

    p1_desc_values = {'opponent': player_2.username}
    p2_desc_values = {'opponent': player_1.username}

    if p1_action == Reaction.NO_ENTRY_SIGN:
        if p2_action == Reaction.NO_ENTRY_SIGN:
            pass  # don't need to do anything here, as we already have the opponent value
        elif p2_action == Reaction.CROSSED_SWORDS:
            actual_damage = get_critical_damage(player_2.damage)
            player_1.health -= actual_damage

            p1_desc_values['received_dmg'] = actual_damage
            p2_desc_values['dealt_dmg'] = actual_damage
        elif p2_action == Reaction.SHIELD:
            pass
        elif p2_action == Reaction.PACKAGE:
            pass
        elif p2_action == Reaction.WHITE_FLAG:
            pass
    elif p1_action == Reaction.CROSSED_SWORDS:
        if p2_action == Reaction.NO_ENTRY_SIGN:
            actual_damage = get_critical_damage(player_1.damage)
            player_2.health -= actual_damage

            p1_desc_values['dealt_dmg'] = actual_damage
            p2_desc_values['received_dmg'] = actual_damage
        elif p2_action == Reaction.CROSSED_SWORDS:
            player_1.health -= player_2.damage
            player_2.health -= player_1.damage

            p1_desc_values['dealt_dmg'] = player_1.damage
            p1_desc_values['received_dmg'] = player_2.damage
            p2_desc_values['dealt_dmg'] = player_2.damage
            p2_desc_values['received_dmg'] = player_1.damage
        elif p2_action == Reaction.SHIELD:
            actual_damage = get_damage_after_defense(player_1.damage, player_2.defense)
            player_2.health -= actual_damage

            p1_desc_values['dealt_dmg'] = actual_damage
            p2_desc_values['blocked_dmg'] = player_2.defense
            p2_desc_values['received_dmg'] = actual_damage
        elif p2_action == Reaction.PACKAGE:
            player_2.health -= player_1.damage

            p1_desc_values['dealt_dmg'] = player_1.damage
            p2_desc_values['received_dmg'] = player_1.damage
        elif p2_action == Reaction.WHITE_FLAG:
            player_2.health -= player_1.damage

            p1_desc_values['dealt_dmg'] = player_1.damage
            p2_desc_values['received_dmg'] = player_1.damage
    elif p1_action == Reaction.SHIELD:
        if p2_action == Reaction.NO_ENTRY_SIGN:
            pass
        elif p2_action == Reaction.CROSSED_SWORDS:
            actual_damage = get_damage_after_defense(player_2.damage, player_1.defense)
            player_1.health -= actual_damage

            p1_desc_values['blocked_dmg'] = player_1.defense
            p1_desc_values['received_dmg'] = actual_damage
            p2_desc_values['dealt_dmg'] = actual_damage
        elif p2_action == Reaction.SHIELD:
            pass
        elif p2_action == Reaction.PACKAGE:
            pass
        elif p2_action == Reaction.WHITE_FLAG:
            pass
    elif p1_action == Reaction.PACKAGE:
        if p2_action == Reaction.NO_ENTRY_SIGN:
            pass
        elif p2_action == Reaction.CROSSED_SWORDS:
            player_1.health -= player_2.damage

            p1_desc_values['received_dmg'] = player_2.damage
            p2_desc_values['dealt_dmg'] = player_1.damage
        elif p2_action == Reaction.SHIELD:
            pass
        elif p2_action == Reaction.PACKAGE:
            pass
        elif p2_action == Reaction.WHITE_FLAG:
            pass
    elif p1_action == Reaction.WHITE_FLAG:
        if p2_action == Reaction.NO_ENTRY_SIGN:
            pass
        elif p2_action == Reaction.CROSSED_SWORDS:
            player_1.health -= player_2.damage

            p1_desc_values['received_dmg'] = player_2.damage
            p2_desc_values['dealt_dmg'] = player_1.damage
        elif p2_action == Reaction.SHIELD:
            pass
        elif p2_action == Reaction.PACKAGE:
            pass
        elif p2_action == Reaction.WHITE_FLAG:
            pass

    p1_msg = p1_desc.get(p2_action).format(**p1_desc_values)
    p2_msg = p2_desc.get(p1_action).format(**p2_desc_values)

    p1_msg = f'```\n{p1_msg}\n```'
    p2_msg = f'```\n{p2_msg}\n```'

    return p1_msg, p2_msg
