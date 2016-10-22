import colorama
import sys
from colorama import Fore, Back, Style
from ludema.screen import Screen
from ludema.board import Board
from ludema.pieces import Wall, Player
from ludema.user_input import user_input
from sokoban_pieces import Box, BoxDestination

def control_guy():
    mappings = {"w": lambda: guy.move.up(),
                "s": lambda: guy.move.down(),
                "d": lambda: guy.move.right(),
                "a": lambda: guy.move.left(),
                "q": lambda: sys.exit(0),
                }

    print(Style.DIM + "What to do now? ")
    action = user_input()
    try:
        mappings[action]()
    except KeyError:
        print("That's not an action. Try again")

guy = Player(Fore.GREEN + "\u03A8", "Bruma")
boxes_dest = [BoxDestination() for _ in range(4)]
boxes = [Box(boxes_dest) for _ in range(4)]
win_conditions = [lambda: all([box.in_position for box in boxes])]
lose_conditions = [lambda: False]
board = Board("First", 8, 8, win_conditions, lose_conditions)

def wall(): return Wall(letter = Style.DIM + ".")
def horizontal_wall(x_b, x_e, y): [board.put_piece(wall(), x, y) for x in range(x_b, x_e+1)]
def vertical_wall(x, y_b, y_e): [board.put_piece(wall(), x, y) for y in range(y_b, y_e+1)]
horizontal_wall(3, 5, 0)
vertical_wall(5, 1, 3)
board.put_piece(wall(), 6, 3)
vertical_wall(7, 3, 5)
board.put_piece(wall(), 6, 5)
board.put_piece(wall(), 5, 5)
vertical_wall(4, 5, 7)
horizontal_wall(2, 3, 7)
vertical_wall(2, 4, 6)
board.put_piece(wall(), 1, 4)
vertical_wall(0, 2, 4)
horizontal_wall(1, 3, 2)
board.put_piece(wall(), 3, 1)
board.put_piece(guy, 4, 3)
board.put_piece(boxes[0], 4, 2)
board.put_piece(boxes_dest[0], 4, 1)
board.put_piece(boxes[1], 3, 3)
board.put_piece(boxes_dest[1], 1, 3)
board.put_piece(boxes[2], 3, 4)
board.put_piece(boxes_dest[2], 3, 5)
board.put_piece(boxes[3], 5, 4)
board.put_piece(boxes_dest[3], 6, 4)

colorama.init(autoreset=True)
screen = Screen(lambda: print(board), control_guy)
while True:
    screen.show(clear_after=True)
    if board.lost or board.won:
        screen.show(clear_after=True)
        break
if board.won:
    print("ALL BOXES IN PLACE. YOU WON!!!!")
