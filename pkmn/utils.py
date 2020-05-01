from pkmn.constants import POKEDEX_TO_INDEX_MAP

def get_pokedex_no_by_index(value):
  for mapping in POKEDEX_TO_INDEX_MAP:
    if mapping[1] == value:
      return mapping[0]

def get_index_by_pokdex_no(value):
  for mapping in POKEDEX_TO_INDEX_MAP:
    if mapping[0] == value:
      return mapping[1]
