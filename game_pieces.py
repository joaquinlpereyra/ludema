from ludema.pieces import Piece, Character
from ludema.items import Item, ShortRangeItem
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
        range_tiles = self.range.values()
        surrounding_pieces = [tile.piece for tile in range_tiles if tile]
        for piece in surrounding_pieces:
            if piece is self.target_door:
                self.target_door.is_open = True
                print("DOOR OPEN")
                break
