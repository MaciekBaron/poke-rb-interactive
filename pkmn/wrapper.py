from pyboy import PyBoy
import pkmn.constants as constants

class InteractivePkmn(PyBoy):
  def set_text(self, text, address):
    """Sets text at address.

    Will always add a string terminator (80) at the end.
    """
    i = 0
    for character in text:
      try:
        self.set_memory_value(address + i, ord(character) + constants.ASCII_DELTA)
        i += 1
      except:
        pass
    self.set_memory_value(address + i, constants.STRING_TERMINATOR)

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

  def teach_sleep(self):
    self.set_player_monster_move(0, 0, constants.MOVE_SLEEP_POWDER)

  def set_player_monster(self, index, monster):
    """
    Sets player monster at a given index.

    Args:
      index (int): Which monster to change (0-5).
      monster (int): Which type of monster to set.
    """
    self.set_memory_value(0xD16B + index, monster)
    self.set_memory_value(0xD164 + (index * 0x2C), monster)

  def set_player_monster_nickname(self, index, text):
    """
    Sets player monster's nickname at a given index.

    Args:
      index (int): Which monster to change (0-5).
      text (string): Nickname to set (will be trimmed at 10 characters).
    """
    self.set_text(text[:10], 0xD2B5 + (index * 0xB))

  def get_player_monster_nickname(self, index):
    return self.get_text(0xD2B5 + (index * 0xB))

  def set_player_monster_move(self, index, move_index, move):
    """
    Sets player monster's move at a given index.

    Args:
      index (int): Which monster to change (0-5).
      move_index (int): Which move to change (0-3).
      move (int): Which type of move to set.
    """
    self.set_memory_value(0xD01C + (index * 0xB) + move_index, move)
