from ludema.screen import Screen
from ludema.board import Board
from ludema.pieces import Character, Player
from pieces_example import Door, Key, Enemy
import colorama
from colorama import Fore, Back, Style

bruma = Player(Fore.GREEN + "\u03A8", "Bruma")
door = Door("Door1", letter=Fore.CYAN + 'D')
key = Key("Key1", door, letter=Fore.YELLOW + "K")
enemy = Enemy(Fore.RED + "E", "Enemy")
enemy2 = Enemy(Fore.RED + "B", "Enemy2")
win_conditions = [lambda: door.is_open]
lose_conditions = [lambda: False]
map_ = Board("Main", 5, 7, win_conditions, lose_conditions, empty_repr=(Style.DIM + " . " + Style.RESET_ALL))

map_.put_piece(bruma, 0, 0)
map_.put_piece(door, 4, 6)
map_.put_piece(key, 1, 6)
map_.put_piece(enemy, 1, 1)
map_.put_piece(enemy2, 4, 4)

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

    mappings = {"up": lambda: bruma.move.up(),
                "down": lambda: bruma.move.down(),
                "right": lambda: bruma.move.right(),
                "left": lambda: bruma.move.left(),
                "grab": lambda: grab_item(),
                "use": lambda: use_key(),
                "show map": lambda: show_map(),
                "debug": lambda: debug()}

    action = input("What to do now? ")
    try:
        mappings[action]()
    except:
        print("ooops...")
        # raise

colorama.init()
def bruma_information():
    print("Name: {0}\nHealth: {1}\nPosition: {2}".format(bruma.name, bruma.health, bruma.position))

screen = Screen(lambda: print(map_), bruma_information, control_bruma)
while True:
    screen.show(clear_after=True)
    if map_.lost or map_.won:
        break
if map_.won:
    print("YOU OPENED THE DOOR. YOU WON!!!!")
if map_.lost:
    print("YOU DIED.")
