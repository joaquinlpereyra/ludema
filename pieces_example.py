from ludema.pieces import Piece, Character, NPC, Item, ShortRangeItem
import ludema.exceptions

class Door(Piece):
    """A simple door."""
    def __init__(self, name, is_open=False, letter = "D"):
        Piece.__init__(self, letter, name)
        self.is_open = is_open
        self.__letter = letter

    @property
    def letter(self):
        return self.__letter if self.is_open else "{0}*".format(self.__letter)

    @letter.setter
    def letter(self, letter):
        self.__letter = letter

class Key(ShortRangeItem):
    def __init__(self, name, target_door, owner=None, letter="K"):
        ShortRangeItem.__init__(self, letter, name, owner)
        self.target_door = target_door

    def do_action(self):
        return self.open_door()

    def open_door(self):
        surrounding_pieces = [tile.piece for tile in self.range if tile]
        for piece in surrounding_pieces:
            if piece is self.target_door:
                self.target_door.is_open = True
                return True
        else:
            return False

class Enemy(NPC):
    def __init__(self, letter, name):
        NPC.__init__(self, letter, name)

    def do_passive_action(self):
        self.attack.random_and_valid()
        self.move.random_and_valid()
