from pkmn.utils import validate_text, validate_monster, get_index_by_monster_name

class Action():
    def __init__(self, cost, execute):
        self.cost = cost
        self.execute = execute

# Each functions needs to accept 'game' and 'arguments' parameters
def _make_dark(game, arguments):
    game.set_palette_to_darkness()

def _heal_monster(game, arguments):
    if game.is_battle_happening():
        game.heal_active_player_monster()
    else:
        game.heal_player_monster(1)

def _rename_player(game, name):
    if validate_text(name):
        game.set_player_name(name)

def _poison_monster(game, arguments):
    if game.is_battle_happening():
        game.set_active_player_monster_poisoned()
    else:
        game.set_player_monster_poisoned(1)

def _trigger_wild_encounter(game, arguments):
    game.set_wild_encounter_rate(0xff)

def _summon_monster(game, arguments):
    monster = validate_monster(arguments)
    index = get_index_by_monster_name(monster)
    if index:
        game.set_wild_encounter_rate(0xff)
        game.set_memory_value(0xD889, index)
        game.set_memory_value(0xD88B, index)
        game.set_memory_value(0xD88D, index)
        game.set_memory_value(0xD88F, index)

ACTIONS = {
    'dark': Action(5, _make_dark),
    'heal': Action(5, _heal_monster),
    'poison': Action(10, _poison_monster),
    'wild': Action(10, _trigger_wild_encounter),
    'summon': Action(20, _summon_monster),
    'playername': Action(50, _rename_player),
}
