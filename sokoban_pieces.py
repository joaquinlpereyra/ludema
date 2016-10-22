from ludema.pieces import Piece
from colorama import Fore, Back, Style

class Box(Piece):
    def __init__(self, possible_destinations):
        Piece.__init__(self, letter=(Fore.YELLOW + "\u25A1"))
        self.possible_destinations = possible_destinations

    @property
    def in_position(self):
        return self.position in [destination.position for destination in self.possible_destinations]

    def on_touch_do(self, touching_piece):
        touching_piece_last_movement = touching_piece.move.history[-1]
        return getattr(self.move, touching_piece_last_movement)()

class BoxDestination(Piece):
    def __init__(self):
        Piece.__init__(self, letter=(Fore.RED + "\u25CC"), walkable=True)
