from ui.reaction import Reaction

combat_descriptions = {
    'passed': {
        'passed': 'You stare, {username} stares. It\'s awkward.',
        Reaction.CROSSED_SWORDS: 'You stare, and {username} attacks. '
                                 'You took a critical hit worth {received_dmg} damage',
        Reaction.SHIELD: 'You stare, and {username} defends against your glare. Nothing happens.',
        Reaction.PACKAGE: 'You stare, while {username} uses an item.',
        Reaction.WHITE_FLAG: 'You stare, and {username} surrenders. Your stare was very effective.'
    },
    Reaction.CROSSED_SWORDS: {
        'passed': 'You attack, and {username} does nothing. You landed a critical attack worth {dealt_dmg} damage.',
        Reaction.CROSSED_SWORDS: 'You attack, and {username} attacks. '
                                 'You dealt {dealt_dmg} damage, and took {received_dmg} damage',
        Reaction.SHIELD: 'You attack, but {username} blocked your attack. You dealt {dealt_dmg} damage.',
        Reaction.PACKAGE: 'You attack, and {username} used an item. You dealt {dealt_dmg} damage.',
        Reaction.WHITE_FLAG: 'You attack, but {username} surrendered. You dealt {dealt_dmg} damage.'
    },
    Reaction.SHIELD: {
        'passed': 'You defend, and {username} did nothing. {username} stares deeply into your soul.',
        Reaction.CROSSED_SWORDS: 'You defended, and {username} attacks. '
                                 'You blocked {blocked_dmg} damage, and took {received_dmg} damage',
        Reaction.SHIELD: 'You defended, and {username} defend. Nothing happens.',
        Reaction.PACKAGE: 'You defended, and {username} used an item.',
        Reaction.WHITE_FLAG: 'You defended, and {username} surrendered.'
    },
    Reaction.PACKAGE: {
        'passed': 'TBD',
        Reaction.CROSSED_SWORDS: 'TBD',
        Reaction.SHIELD: 'TBD',
        Reaction.PACKAGE: 'TBD',
        Reaction.WHITE_FLAG: 'TBD'
    },
    Reaction.WHITE_FLAG: {
        'passed': 'TBD',
        Reaction.CROSSED_SWORDS: 'TBD',
        Reaction.SHIELD: 'TBD',
        Reaction.PACKAGE: 'TBD',
        Reaction.WHITE_FLAG: 'TBD'
    }
}


def get_critical_damage(damage):
    return damage * 2


def get_damage_after_defense(damage, defense):
    actual_damage = damage - defense
    if actual_damage < 0:
        return 0
    return actual_damage
