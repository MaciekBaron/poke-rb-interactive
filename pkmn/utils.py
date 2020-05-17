from pkmn.constants import POKEDEX_TO_INDEX_MAP, BANNED_WORDS, MONSTER_NAMES
import re

def get_pokedex_no_by_index(value):
    for mapping in POKEDEX_TO_INDEX_MAP:
        if mapping[1] == value:
            return mapping[0]

def get_index_by_pokedex_no(value):
    for mapping in POKEDEX_TO_INDEX_MAP:
        if mapping[0] == value:
            return mapping[1]

def get_index_by_monster_name(value):
    try:
        return get_index_by_pokedex_no(MONSTER_NAMES.index(value) + 1)
    except:
        return False

def validate_text(vote):
    if re.fullmatch('[a-zA-Z0-9 ]+', vote):
        if any(word in vote.lower() for word in BANNED_WORDS):
            return False
        return vote
    else:
        return False

def validate_monster(vote):
    try:
        return MONSTER_NAMES[int(vote) - 1]
    except:
        try:
            return MONSTER_NAMES[list(map(lambda v: v.lower(), list(MONSTER_NAMES))).index(vote.lower())]
        except:
            return False
