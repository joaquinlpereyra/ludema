from ludema.screen import Screen
from ludema.board import Board
from ludema.utils import Position, Direction
from ludema.pieces import Character
from game_pieces import Door, Key

map_ = Board("Main", 5, 5)
bruma = Character("\u03A8", "Bruma")
door = Door("Door1")
key = Key("Key1", door, letter="K")
map_.put_piece(bruma, Position(0,0))
map_.put_piece(door, Position(2, 2))
map_.put_piece(key, Position(3, 3))

def control_bruma():
    def grab_item():
        bruma.grab_item_from_surroundings()

    def use_key():
        bruma.use_item(key)

    def show_map():
        print(map_)

    mappings = {"up": bruma.move.up,
                "down": bruma.move.down,
                "right": bruma.move.right,
                "left": bruma.move.left,
                "grab": grab_item,
                "use": use_key,
                "show map": show_map}

    action = input("What to do now? ")
    try:
        mappings[action]()
    except:
        print("ooops...")
        raise

def bruma_information(): print("Name: {0} / Position: {1}".format(bruma.name, bruma.position))
def show_map(): print(str(map_))

screen = Screen(show_map, bruma_information, control_bruma)
while True:
    screen.show()
