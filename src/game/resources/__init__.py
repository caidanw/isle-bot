def all_resources():
    from src.game.resources.field import Field
    from src.game.resources.forest import Forest
    from src.game.resources.mine import Mine
    from src.game.resources.swamp import Swamp

    return [
        Field(),
        Forest(),
        Mine(),
        Swamp()
    ]
