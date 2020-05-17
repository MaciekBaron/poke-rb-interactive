from pyboy import PyBoy
import pkmn.constants as constants

PKMN_SIZE = 0x2C
BYTE_ORDER = 'big'

def get_character_index(character):
    if character == ' ':
        return 0x7F
    if character == '?':
        return 0xE6
    if character == '!':
        return 0xE7
    if character == 'é':
        return 0xBA

    index = ord(character)
    if index > 47 and index < 58:
        # number
        return index + 197
    return index + constants.ASCII_DELTA

class InteractivePkmn(PyBoy):
    def get_int_at_address(self, address, size=2):
        """Returns an integer from a given address of a spcified size."""
        bytes = []
        for i in range(size):
            bytes.append(self.get_memory_value(address + i))
        return int.from_bytes(bytes, byteorder=BYTE_ORDER)

    def set_int_at_address(self, address, value, size=2):
        """Sets an integer at a given address of a specified size."""
        bytes = value.to_bytes(2, byteorder=BYTE_ORDER)
        i = 0
        for byte in bytes:
            self.set_memory_value(address + i, byte)
            i += 1

    def set_text(self, text, address):
        """Sets text at address.

        Will always add a string terminator (80) at the end.
        """
        i = 0
        for character in text:
            try:
                self.set_memory_value(address + i, get_character_index(character))
                i += 1
            except:
                pass
        self.set_memory_value(address + i, constants.STRING_TERMINATOR)

    def set_rom_text(self, text, bank, address):
        i = 0
        for character in text:
            try:
                self.override_memory_value(bank, address + i, get_character_index(character))
                i += 1
            except:
                pass

    def set_player_name(self, name):
        """
        Sets the player name.

        Args:
            name (string): Name to be set (will be trimmed at 8 characters).
        """
        self.set_text(name[:8], 0xD158)

    def get_player_name(self):
        """
        Returns player name.
        """
        return self.get_text(0xD158)

    def set_rival_name(self, name):
        """
        Sets the rival name.

        Args:
            name (string): Name to be set (will be trimmed at 8 characters).
        """
        self.set_text(name[:8], 0xD34A)

    def get_rival_name(self):
        """
        Returns rival name.
        """
        return self.get_text(0xD34A)

    def get_text(self, address, cap = 16):
        """
        Retrieves a string from a given address.

        Args:
            address (int): Address from where to retrieve text from.
            cap (int): Maximum expected length of string (default: 16).
        """
        i = 0
        text = ''
        while i < cap:
            value = self.get_memory_value(address + i)
            try:
                text += chr(value - constants.ASCII_DELTA)
            except:
                pass
            if value == constants.STRING_TERMINATOR:
                break
            i += 1
        return text

    def set_palette_to_darkness(self):
        self.set_memory_value(0xD35D, 6)

    def set_player_monster(self, index, monster):
        """
        Sets player monster at a given index.

        Args:
            index (int): Which monster to change (0-5).
            monster (int): Which type of monster to set.
        """
        self.set_memory_value(0xD16B + index, monster)
        self.set_memory_value(0xD164 + (index * PKMN_SIZE), monster)

    def get_player_monster(self, index):
        """
        Returns player monster at a given index.

        Args:
            index (int): Which monster to change (0-5).
        """
        return self.get_memory_value(0xD16B + index)

    def set_player_monster_nickname(self, index, text):
        """
        Sets player monster's nickname at a given index.

        Args:
            index (int): Which monster to change (0-5).
            text (string): Nickname to set (will be trimmed at 10 characters).
        """
        self.set_text(text[:10], 0xD2B5 + (index * PKMN_SIZE))

    def get_player_monster_nickname(self, index):
        """
        Returns player monster's nickname at a given index.

        Args:
            index (int): Which monster (0-5).
        """
        return self.get_text(0xD2B5 + (index * PKMN_SIZE))

    def set_player_monster_move(self, index, move_index, move):
        """
        Sets player monster's move at a given index.

        Args:
            index (int): Which monster to change (0-5).
            move_index (int): Which move to change (0-3).
            move (int): Which type of move to set.
        """
        self.set_memory_value(0xD01C + (index * PKMN_SIZE) + move_index, move)

    def get_player_monster_move(self, index, move_index):
        """
        Returns player monster's move at a given index.

        Args:
            index (int): Which monster (0-5).
            move_index (int): Which move to change (0-3).
        """
        return self.get_memory_value(0xD01C + (index * PKMN_SIZE) + move_index)

    def get_player_monster_current_hp(self, index):
        """
        Returns player monster's current HP at a given index.

        Args:
            index (int): Which monster (0-5).
        """
        return self.get_int_at_address(0xD16C + (index * PKMN_SIZE))

    def get_active_player_monster_current_hp(self):
        return self.get_int_at_address(0xD015)

    def set_player_monster_current_hp(self, index, hp):
        """
        Sets the current HP of a given player monster.

        Args:
            index (int): Which monster to change (0-5).
            hp (int): Health points.
        """
        self.set_int_at_address(0xD16C + (index * PKMN_SIZE), hp)

    def set_active_player_monster_current_hp(self, hp):
        self.set_int_at_address(0xD015, hp)

    def get_player_monster_max_hp(self, index):
        """
        Returns player monster's max HP at a given index.

        Args:
            index (int): Which monster (0-5).
        """
        return self.get_int_at_address(0xD18D + (index * PKMN_SIZE))

    def get_active_player_monster_max_hp(self):
        return self.get_int_at_address(0xD023)

    def set_player_monster_max_hp(self, index, hp):
        """
        Sets the max HP of a given player monster.

        Args:
            index (int): Which monster to change (0-5).
            hp (int): Health points.
        """
        self.set_int_at_address(0xD18D + (index * PKMN_SIZE), hp)

    def set_active_player_monster_max_hp(self, hp):
        return self.set_int_at_address(0xD023, hp)

    def set_player_monster_status(self, index, status):
        """
        Sets the ailment status of a given player monster.

        Args:
            index (int): Which monster to change (0-5).
            status (int): Status to be set.
        """
        assert status >= 0 and status < 0xFF
        assert index < 6
        self.set_memory_value(0xD16F + (index * PKMN_SIZE), status)

    def set_player_monster_asleep(self, index):
        self.set_player_monster_status(index, constants.STATUS_ASLEEP)

    def set_player_monster_poisoned(self, index):
        self.set_player_monster_status(index, constants.STATUS_POISONED)

    def set_player_monster_burned(self, index):
        self.set_player_monster_status(index, constants.STATUS_BURNED)

    def set_player_monster_frozen(self, index):
        self.set_player_monster_status(index, constants.STATUS_FROZEN)

    def set_player_monster_paralyzed(self, index):
        self.set_player_monster_status(index, constants.STATUS_PARALYZED)

    def set_player_monster_no_ailment(self, index):
        self.set_player_monster_status(index, 0)

    def get_player_money(self):
        return self.get_int_at_address(0xD347, size=3)

    def set_active_player_monster_status(self, status):
        self.set_memory_value(0xD018, status)

    def set_active_player_monster_asleep(self):
        self.set_active_player_monster_status(constants.STATUS_ASLEEP)

    def set_active_player_monster_poisoned(self):
        self.set_active_player_monster_status(constants.STATUS_POISONED)

    def set_active_player_monster_burned(self):
        self.set_active_player_monster_status(constants.STATUS_BURNED)

    def set_active_player_monster_frozen(self):
        self.set_active_player_monster_status(constants.STATUS_FROZEN)

    def set_active_player_monster_paralyzed(self):
        self.set_active_player_monster_status(constants.STATUS_PARALYZED)

    def set_active_player_monster_no_ailment(self):
        self.set_active_player_monster_status(0)

    def set_active_player_monster_move(self, index, move):
        self.set_memory_value(0xD01C + index, move)

    def set_active_opponent_monster_move(self, index, move):
        self.set_memory_value(0xCFED + index, move)

    def set_active_player_monster_nickname(self, nickname):
        self.set_text(nickname[:10], 0xD009)

    def set_active_opponent_monster_nickname(self, nickname):
        self.set_text(nickname[:10], 0xCFDA)

    def set_active_opponent_monster_status(self, status):
        self.set_memory_value(0xCFE9, status)

    def set_active_opponent_monster_asleep(self):
        self.set_active_opponent_monster_status(constants.STATUS_ASLEEP)

    def set_active_opponent_monster_poisoned(self):
        self.set_active_opponent_monster_status(constants.STATUS_POISONED)

    def set_active_opponent_monster_burned(self):
        self.set_active_opponent_monster_status(constants.STATUS_BURNED)

    def set_active_opponent_monster_frozen(self):
        self.set_active_opponent_monster_status(constants.STATUS_FROZEN)

    def set_active_opponent_monster_paralyzed(self):
        self.set_active_opponent_monster_status(constants.STATUS_PARALYZED)

    def set_active_opponent_monster_no_ailment(self):
        self.set_active_opponent_monster_status(0)

    def heal_player_monster(self, index):
        """
        Fully heals a player monster.

        Args:
            index (int): Which monster to change (0-5).
        """
        self.set_player_monster_no_ailment(index)
        max_hp = self.get_player_monster_max_hp(index)
        self.set_player_monster_current_hp(index, max_hp)

    def heal_active_player_monster(self):
        self.set_active_player_monster_no_ailment()
        max_hp = self.get_active_player_monster_max_hp()
        self.set_active_player_monster_current_hp(max_hp)

    def is_battle_happening(self):
        return self.get_memory_value(0xD057) != 0

    def get_current_map(self):
        return self.get_memory_value(0xD35E)

    def get_current_map_name(self):
        return constants.MAP_NAMES[self.get_current_map()]

    def set_wild_encounter_rate(self, value):
        self.set_memory_value(0xD887, value)
