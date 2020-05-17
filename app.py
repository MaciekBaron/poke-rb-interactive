from pkmn.wrapper import InteractivePkmn
from pkmn.state_updater import StateUpdater
from pkmn.names import get_name_by_monster_index, get_name_by_pokedex_no
from pkmn.voting import VoteManager
from pkmn.polls import BATTLE_POLLS, OVERWORLD_POLLS, good_or_bad_poll, starter_poll, parcel_poll
from pkmn.web import start_web_interface
from pkmn.websockets import start_web_sockets, add_message
from pkmn.bot import start_bot
import pkmn.constants as constants
import threading
from os import path
from pkmn.config import ROM
import json
import time
import random

pkmn = InteractivePkmn(ROM['FileName'])

save_exists = path.exists("autosave.state") and path.getsize("autosave.state") > 0
if save_exists:
    autosave = open("autosave.state", "rb")
    pkmn.load_state(autosave)
    print("Loaded state")
    autosave.close()

state_updater = StateUpdater(pkmn)

vote_manager = VoteManager.Instance()
vote_manager.set_game_instance(pkmn)
vote_manager.set_current_poll(good_or_bad_poll)
vote_manager.activate_poll()

start_web_interface()
start_web_sockets()

def init_bot():
    start_bot(vote_manager)

def wait():
    time.sleep(.1)

def wait_for_battle_to_finish_or_timeout(timeout):
    wait_until = time.time() + timeout
    while pkmn.is_battle_happening():
        if time.time() > wait_until:
            return True
        wait()
    return False

def start_poll_loop():
    # Main poll flags
    last_poll_time = time.time()
    starter_poll_done = False
    parcel_poll_done = False

    # Main poll loop
    while True:
        # Try to start an overworld poll
        poll = None

        # Are we in Red's room? (Oak intro)
        if not starter_poll_done and pkmn.get_current_map() == constants.MAP_REDS_HOUSE_2F:
            starter_poll_done = True
            poll = starter_poll
        elif not parcel_poll_done and pkmn.get_current_map() == constants.MAP_VIRIDIAN_CITY:
            parcel_poll_done = True
            poll = parcel_poll

        # @TODO Add additional polls

        elif starter_poll_done and time.time() - last_poll_time > 120:
            poll = random.choice(OVERWORLD_POLLS)

        if poll is not None:
            last_poll_time = time.time()
            # We have a poll to run
            vote_manager.set_current_poll(poll, 60)
            # Wait for the poll to finish
            while vote_manager.is_poll_available():
                wait()
            vote_manager.resolve_poll(pkmn)
            # Poll is over but let's deactivate it too
            vote_manager.deactivate_poll()

        if pkmn.is_battle_happening():
            # Entered battle
            vote_manager.set_current_poll(random.choice(BATTLE_POLLS))
            # Wait for battle to finish
            while pkmn.is_battle_happening():
                wait()
                if not vote_manager.is_poll_available():
                    # Poll has finished
                    vote_manager.resolve_poll(pkmn)
                    # Wait until battle finishes or 20s have passed
                    # If the battle hasn't finished within 20s, loop starts new poll
                    wait_for_battle_to_finish_or_timeout(20)
                    break
            # Battle has finished at this stage
            vote_manager.deactivate_poll()
            last_poll_time = time.time()
        wait()

def ask_for_command():
    # Debug commands
    c = ''
    while c != 'exit':
        c = input("\nEnter command:")
        if c == 'name':
            name = input("  Enter name:")
            pkmn.set_player_name(name)
        elif c == 'save':
            save_file = open("autosave.state", "wb")
            pkmn.save_state(save_file)
            save_file.close()
            print("Saved state")
        elif c == 'vote':
            print(vote_manager.get_current_question())
            vote = input("Enter vote: ")
            vote_manager.cast_vote("me", vote)
            print(vote_manager.get_results())


# @TODO Implement "clean exit" for all threads and loops
b = threading.Thread(target=start_poll_loop)
b.start()

bt = threading.Thread(target=init_bot)
bt.start()

state_updater.start()

x = threading.Thread(target=ask_for_command)
x.start()

while not pkmn.tick():
    pass
