from pkmn.wrapper import InteractivePkmn
from threading import Timer
from pkmn.config import STATE

INTERVAL = float(STATE['UpdateInterval'])
STATE_DIR = "state/"

def write_state(name, value):
    """Writes a value to the state text file provided"""
    state_file = open(STATE_DIR + "%s.txt" % name, "w")
    try:
        state_file.write(value)
    except:
        print("Could not write state %s" % name)
    state_file.close()

class StateUpdater():
    def __init__(self, game: InteractivePkmn):
        self.game = game

    def update(self):
        """Updates text files with current values"""
        write_state("playername", self.game.get_player_name())
        write_state("rivalname", self.game.get_rival_name())

        for i in range(4):
            write_state(f"monster_nickname{i + 1}", self.game.get_player_monster_nickname(i)[:-1])

        write_state("map", self.game.get_current_map_name())

        self.start()

    def start(self):
        """Initiates the regular update process"""
        self.timer = Timer(INTERVAL, self.update)
        self.timer.start()

    def stop(self):
        """Stops the update process until restarted again"""
        self.timer.cancel()

