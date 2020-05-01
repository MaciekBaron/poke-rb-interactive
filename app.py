from pkmn.wrapper import InteractivePkmn
from pkmn.state_updater import StateUpdater
from pkmn.names import get_name_by_monster_index, get_name_by_pokedex_no
from pkmn.voting import VoteManager, good_or_bad_poll
import pkmn.constants as constants
import threading
from os import path

pkmn = InteractivePkmn('pokered.gb')

save_exists = path.exists("autosave.state") and path.getsize("autosave.state") > 0
autosave = open("autosave.state", "rb")
if save_exists:
  pkmn.load_state(autosave)
  print("Loaded state")
autosave.close()

state_updater = StateUpdater(pkmn)

vote_manager = VoteManager()

vote_manager.set_current_poll(good_or_bad_poll)
vote_manager.activate_poll()

def ask_for_command():
  f = ''
  while f != 'exit':
    f = input("Enter command:")
    if f == 'name':
      name = input("  Enter name:")
      pkmn.set_player_name(name)
    elif f == 'save':
      save_file = open("autosave.state", "wb")
      pkmn.save_state(save_file)
      save_file.close()
      print("Saved state")
    elif f == 'dark':
      pkmn.set_palette_to_darkness()
    elif f == 'sleep':
      pkmn.teach_sleep()
    elif f == 'mew':
      pkmn.set_player_monster(0, constants.MONSTER_MEW)
      pkmn.set_player_monster_nickname(0, 'MEWSKI')
    elif f == 'dex':
      no = int(input("Enter pokedex no: "))
      print(get_name_by_pokedex_no(no))
    elif f == 'index':
      index = int(input("Enter index: "))
      print(get_name_by_monster_index(index))
    elif f == 'vote':
      print(vote_manager.get_current_question())
      vote = input("Enter vote: ")
      vote_manager.cast_vote("me", vote)
      print(vote_manager.get_results())
    print(pkmn.get_text(0xD158))
    print(pkmn.get_text(0xD34A))
    print(pkmn.get_memory_value(0xCCD5))

x = threading.Thread(target=ask_for_command)

x.start()

state_updater.start()

while not pkmn.tick():
  pass
