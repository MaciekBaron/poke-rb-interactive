from pkmn.constants import MONSTER_NAMES, POKEDEX_TO_INDEX_MAP
from pkmn.utils import get_pokedex_no_by_index

def get_name_by_pokedex_no(value):
  try:
    return MONSTER_NAMES[value - 1]
  except:
    return "MISSINGNO"

def get_name_by_monster_index(value):
  return get_name_by_pokedex_no(get_pokedex_no_by_index(value))
