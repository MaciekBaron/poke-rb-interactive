from pkmn.voting import OpenPoll, OptionPoll
from pkmn.constants import SPRITE_ROCKET, SPRITE_BIRD, MONSTER_NAMES, BANNED_WORDS, MOVE_SPLASH, MOVE_FLY, MOVE_SELFDESTRUCT, MOVE_HYPER_BEAM, MOVE_LOVELY_KISS, MOVE_METRONOME, MOVE_TRANSFORM, MOVE_SING
from pkmn.utils import validate_text, validate_monster, get_index_by_monster_name
import re

def do_nothing(pkmn, option, votes):
    pass

def _heal_or_sleep(pkmn, option, votes):
    if option == 'help':
        # Help the player
        pkmn.heal_active_player_monster()
    else:
        # Hinder the player
        pkmn.set_active_player_monster_asleep()

def _poison_enemy_or_reduce_hp(pkmn, option, votes):
    if option == 'help':
        pkmn.set_active_opponent_monster_poisoned()
    else:
        pkmn.set_active_player_monster_hp(1)

def _paralyze_enemy_or_reduce_hp(pkmn, option, votes):
    if option == 'help':
        pkmn.set_active_opponent_monster_paralyzed()
    else:
        pkmn.set_active_player_monster_hp(1)

def _sleep_enemy_or_player(pkmn, option, votes):
    if option == 'help':
        pkmn.set_active_opponent_monster_asleep()
    else:
        pkmn.set_active_player_monster_asleep()

def _splash_enemy_or_paralyzed(pkmn, option, votes):
    if option == 'help':
        pkmn.set_active_opponent_monster_move(0, MOVE_SPLASH)
        pkmn.set_active_opponent_monster_move(1, MOVE_SPLASH)
        pkmn.set_active_opponent_monster_move(2, MOVE_SPLASH)
        pkmn.set_active_opponent_monster_move(3, MOVE_SPLASH)
    else:
        pkmn.set_active_opponent_monster_paralyzed()

def _change_enemy_name(pkmn, option, votes):
    if option is not None:
        pkmn.set_active_opponent_monster_nickname(option)

def _change_player_name(pkmn, option, votes):
    if option is not None:
        pkmn.set_active_player_monster_nickname(option)

def _set_first_move(pkmn, option, votes):
    move = MOVE_HYPER_BEAM

    if option == "selfdestruct":
        move = MOVE_SELFDESTRUCT
    elif option == "fly":
        move = MOVE_FLY
    elif option == "splash":
        move = MOVE_SPLASH
    elif option == "kiss":
        move = MOVE_LOVELY_KISS
    elif option == "metronome":
        move = MOVE_METRONOME
    elif option == "transform":
        move = MOVE_TRANSFORM
    elif option == "sing":
        move = MOVE_SING

    pkmn.set_active_player_monster_move(0, move)

def _override_sprites(pkmn, option, votes):
    sprite = 0x07
    if option == 'fatguy':
        sprite = 0x05
    elif option == 'oak':
        sprite = 0x09
    elif option == 'ball':
        sprite = 0x0B
    for i in range(15):
        if pkmn.get_memory_value(0xC20E + (i * 0x10)) != 0x01:
            pkmn.set_memory_value(0xC20E + (i * 0x10), sprite)

def _set_starters(pkmn, option, votes):
    # Get top three votes
    top_three = list(
        map(lambda a: a[1], sorted([(v, k) for k, v in votes.items()], reverse=True)[:3]))
    offset = 0
    starter_locations = (0x110E, 0x111F, 0x1130)
    for starter in top_three:
        index = get_index_by_monster_name(starter)
        pkmn.override_memory_value(7, starter_locations[offset], index)
        offset += 1
    pass

def _rename_pokeball(pkmn, option, votes):
    if option:
        new_name = option + '         '
        new_name = new_name[:9]
        pkmn.set_rom_text(new_name, 1, 0x074D)

def _rename_potion(pkmn, option, votes):
    if option:
        new_name = option + '      '
        new_name = new_name[:6]
        pkmn.set_rom_text(new_name, 1, 0x07F1)

def _rename_antidote(pkmn, option, votes):
    if option:
        new_name = option + '        '
        new_name = new_name[:8]
        pkmn.set_rom_text(new_name, 1, 0x078D)

def _rename_pokedex(pkmn, option, votes):
    if option:
        new_name = option + '       '
        new_name = new_name[:7]
        pkmn.set_rom_text(new_name, 1, 0x31AF)

def _rename_parcel(pkmn, option, votes):
    if option:
        new_name = option + '           '
        new_name = new_name[:11]
        pkmn.set_rom_text(new_name, 1, 0x09E1)

good_or_bad_poll = OptionPoll(
    "Do a good or bad thing to the player?",
    do_nothing,
    ["good", "bad"],
    ["", ""],
)

poll_heal_or_sleep = OptionPoll(
    "Fight! Help or hinder?",
    _heal_or_sleep,
    ["help", "hinder"],
    ["Heal active Pokemon", "Make active Pokemon fall asleep"],
)

poll_poison_or_hp = OptionPoll(
    "Battle time! Help or hinder?",
    _poison_enemy_or_reduce_hp,
    ["help", "hinder"],
    ["Poison enemy", "Reduce player's HP to 1"],
)

poll_splash_or_paralyzed = OptionPoll(
    "Battle time! Help or hinder?",
    _splash_enemy_or_paralyzed,
    ["help", "hinder"],
    ["Enemy just uses Splash", "Paralyze player"],
)

poll_splash_or_reduce_hp = OptionPoll(
    "Battle time! Help or hinder?",
    _paralyze_enemy_or_reduce_hp,
    ["help", "hinder"],
    ["Enemy is paralyzed", "Reduce player's HP to 1"],
)

poll_sleep_both = OptionPoll(
    "Sleepy time! Help or hinder?",
    _sleep_enemy_or_player,
    ["help", "hinder"],
    ["Enemy falls asleep", "Player falls asleep"],
)

poll_move_change = OptionPoll(
    "Let's change the player's first move to:",
    _set_first_move,
    ["hyperbeam", "selfdestruct", "fly", "splash"],
    ["Powerful blast", "Self explanotary", "Takes to the skies", "Hmmm...."]
)
poll_move_change_two = OptionPoll(
    "Let's change the player's first move to:",
    _set_first_move,
    ["kiss", "metronome", "transform", "sing"],
    ["Lovely kiss", "Random move", "Turns into the enemy", "Lovely song"]
)

poll_sprite = OptionPoll(
    "Let's change the look of all the characters on this map to:",
    _override_sprites,
    ["fatguy", "oldguy", "oak", "ball"],
    ["Big belly bro", "Old wise man", "Professor Oak", "Literally just a Pokeball"]
)

rename_enemy_monster = OpenPoll(
    "What should we rename the enemy Pokemon to?",
    _change_enemy_name,
    validate_text,
    "open"
)

rename_player_monster = OpenPoll(
    "Let's temporarily change the player's Pokemon's nickname! Ideas?",
    _change_player_name,
    validate_text,
    "open"
)

rename_pokeball_poll = OpenPoll(
    "Screw it. Let's find a new name for the POKEBALL. Max 9 characters. Ideas?",
    _rename_pokeball,
    validate_text,
    "open"
)

rename_potion_poll = OpenPoll(
    "Let's be confusing and rename POTION. Max 6 characters. Go!",
    _rename_potion,
    validate_text,
    "open"
)

rename_potion_poll = OpenPoll(
    "Let's be confusing and rename ANTIDOTE. Max 8 characters. Suggestions?",
    _rename_antidote,
    validate_text,
    "open"
)

rename_pokedex_poll = OpenPoll(
    "The Pokedex needs a new name. Max 7 characters. Ideas?",
    _rename_pokedex,
    validate_text,
    "open"
)

starter_poll = OpenPoll(
    "What should the available starters be?",
    _set_starters,
    validate_monster,
    "monster"
)

underrated_poll = OpenPoll(
    "Which is the most underrated 1st generation Pokemon?",
    do_nothing,
    validate_monster,
    "monster"
)

overrated_poll = OpenPoll(
    "Which is the most overrated 1st generation Pokemon?",
    do_nothing,
    validate_monster,
    "monster"
)

annoying_poll = OpenPoll(
    "Which is the most ANNOYING 1st generation Pokemon?",
    do_nothing,
    validate_monster,
    "monster"
)

cutest_poll = OpenPoll(
    "Which is the CUTEST 1st generation Pokemon?",
    do_nothing,
    validate_monster,
    "monster"
)

ugliest_poll = OpenPoll(
    "Which is the UGLIEST 1st generation Pokemon?",
    do_nothing,
    validate_monster,
    "monster"
)

normal_looking_poll = OpenPoll(
    "Which 1st generation Pokemon is the most 'normal' looking?",
    do_nothing,
    validate_monster,
    "monster"
)

generation_poll = OptionPoll(
    "Which generation is the best?",
    do_nothing,
    ["1", "2", "3", "latest"],
    ["Red, Blue, Yellow", "Gold, Silver, Crystal", "Ruby, Sapphire, Emerald", "Sword, Shield"]
)

parcel_poll = OpenPoll(
    "What should we call the item Oak's will be getting (Oak's Parcel)? Max 11 characters.",
    _rename_parcel,
    validate_text,
    "open"
)

OVERWORLD_POLLS = [
    poll_sprite,
    rename_pokeball_poll,
    rename_potion_poll,
    rename_pokedex_poll,
    underrated_poll,
    overrated_poll,
    annoying_poll,
    cutest_poll,
    ugliest_poll,
    normal_looking_poll,
    generation_poll
]

BATTLE_POLLS = [
    poll_heal_or_sleep,
    poll_poison_or_hp,
    rename_enemy_monster,
    rename_player_monster,
    poll_splash_or_paralyzed,
    poll_move_change,
    poll_move_change_two,
    poll_splash_or_reduce_hp,
    poll_sleep_both
]
