import colorama
import sys
from colorama import Fore, Back, Style
from ludema.screen import Screen
from ludema.board import Board
from ludema.pieces import Wall, Player, Piece
from ludema.user_input import user_input

# We create a player. It will be green, named "Guy" and represented on the board
# by the Ψ character (Ψ = 03A8 in unicode)
# the player (and actually all the pieces) have a Move and Attack interface unless
# specified otherwise.
# in this level we're gonna only use the move interface, see control_guy function
guy = Player(Fore.GREEN + "\u03A8", "Guy")

# we define a function to control our guy and wait for user input
# thanks to ludema.user_input module, we don't wait for the user to press
# return: user_input will process the information as soon as a character
# is inputed by the user.
def control_guy():
    mappings = {"w": guy.move.up,
                "s": guy.move.down,
                "d": guy.move.right,
                "a": guy.move.left,
                "q": sys.exit}

    action = user_input()
    try:
        mappings[action]()
    except KeyError:
        print("That's not an action. Try again")

# besides the player, we're gonna need boxes and their destination, right?
# the Ludema.Pieces.Piece class is intended to be subclassed, and allows us
# to easily define our own pieces
class Box(Piece):
    def __init__(self, possible_destinations):
        Piece.__init__(self, letter=(Fore.YELLOW + "\u25A1"))
        self.possible_destinations = possible_destinations

    @property
    def in_position(self):
        return self.position in [destination.position for destination in self.possible_destinations]

    # the following is probably the most complicated piece of code on this game
    # for someone new to python or coding to understand
    # on_touch_do is a Piece function which is called every time another piece
    # (the touching_piece) collisions with this one.
    # for Sokoban, we want to do this: when guy pushes to any direction,
    # make the box move in that direction too.
    # so we access the touching_piece last movement,
    # and then we use getattr to call that same movement on the box.
    # we need to call getattr because move.history is just a list of strings
    # like ['up', 'up', 'right', 'left', 'down']. Python allows us
    # to access attributes via strings with getattr.
    def on_touch_do(self, touching_piece):
        touching_piece_last_movement = touching_piece.move.history[-1]
        return getattr(self.move, touching_piece_last_movement)()

# the destinations are easier. they just need to be marked, and we need
# to specify that they are 'walkable', that is: the player (or any other piece)
# can be placed above them.
class BoxDestination(Piece):
    def __init__(self):
        Piece.__init__(self, letter=(Fore.RED + "\u25CC"), walkable=True)

# we will now create a board for our sokoban example
# the boards are intended to represent levels in a game
# our sokoban example will only have one level
# before creating a board, we need to specify winning and losing conditions
# winning and losing conditions are lists of nullary functions
win_conditions = [lambda: all([box.in_position for box in boxes])]
lose_conditions = [lambda: False]  # never lose :)

# create the actual board named First of 8x8 tiles with the specified conditions
# board = Board("First", 8, 8, win_conditions, lose_conditions)

# lets create 4 boxes and boxes destinations
boxes_dest = [BoxDestination() for _ in range(4)]
boxes = [Box(boxes_dest) for _ in range(4)]

# we create as silly function that returns wall with a style we like
# the Wall class is already provided by ludema :)
def wall(): return Wall(letter = Style.DIM + ".")

# lets create our first level
# this is the blueprint for level 1
level1 = """
. . . . . . . .
. . * * * . . .
. . * O * * * *
. . * X . X O *
* * * . @ . . *
* O X . X . * *
* * * * O * * .
. . . * * * . .
"""

# and this the leyend
leyend = {'*': wall,
           '@': guy,
           'X': boxes,
           'O': boxes_dest
           }

#ludema takes care of everything else
board = Board.new_from_blueprint("First", level1, leyend, win_conditions, lose_conditions)

# this is just a continous loop to play the level
# it will probably be abstracted away in future versions of ludema
colorama.init(autoreset=True)
screen = Screen(lambda: print(board), control_guy)
while True:
    screen.show(clear_after=True)
    if board.lost or board.won:
        screen.show(clear_after=True)
        break
if board.won:
    print("ALL BOXES IN PLACE. YOU WON!!!!")
