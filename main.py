from ludema.screen import Screen
from ludema.board import Board
from ludema.utils import Position, Direction
from ludema.pieces import Character, Player
from game_pieces import Door, Key, Enemy
import colorama
from colorama import Fore, Back, Style

map_ = Board("Main", 5, 7, empty_repr=(Style.DIM + " . " + Style.RESET_ALL))
bruma = Player(Fore.GREEN + "\u03A8", "Bruma")
door = Door("Door1", letter=Fore.CYAN + 'D')
key = Key("Key1", door, letter=Fore.YELLOW + "K")
enemy = Enemy(Fore.RED + "E", "Enemy")
enemy2 = Enemy(Fore.RED + "B", "Enemy2")
map_.put_piece(bruma, Position(0, 0))
map_.put_piece(door, Position(4, 6))
map_.put_piece(key, Position(1, 6))
map_.put_piece(enemy, Position(1,1))
map_.put_piece(enemy2, Position(4,4))

def control_bruma():
    def grab_item():
        bruma.grab_item_from_surroundings()

    def use_key():
        key_success = bruma.use_item(key)
        if key_success:
            global won
            won = True

    def show_map():
        print(map_)

    def debug():
        import ipdb; ipdb.set_trace()

    mappings = {"up": bruma.move.up,
                "down": bruma.move.down,
                "right": bruma.move.right,
                "left": bruma.move.left,
                "grab": grab_item,
                "use": use_key,
                "show map": show_map,
                "debug": debug}

    action = input("What to do now? ")
    try:
        mappings[action]()
    except:
        print("ooops...")
        raise

colorama.init()
def bruma_information(): print("Name: {0} / Position: {1}".format(bruma.name, bruma.position))
def show_map(): print(str(map_))

screen = Screen(show_map, bruma_information, control_bruma)
won = False
while not won:
    screen.show(clear_after=True)

print("YOU OPENED THE DOOR. YOU WON!!!!")
