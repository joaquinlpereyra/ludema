from game.screen import Screen
from game.board import Board
from game.utils import Position, Direction
from game.pieces import Character
from game_pieces import Door, Key

map_ = Board("Main", 20, 20)
bruma = Character("Y", "Bruma")
door = Door("Door1")
key = Key("Key1", door, letter="K")
map_.put_piece(bruma, Position(0,0))
map_.put_piece(door, Position(10,10))
map_.put_piece(key, Position(19,19))

def control_bruma():
    def go_up():
        up_tile = bruma.surroundings[Direction.UP]
        bruma.move(up_tile)

    def go_down():
        down_tile = bruma.surroundings[Direction.DOWN]
        bruma.move(down_tile)

    def go_right():
        right_tile = bruma.surroundings[Direction.RIGHT]
        bruma.move(right_tile)

    def go_left():
        left_tile = bruma.surroundings[Direction.LEFT]
        bruma.move(left_tile)

    def grab_item_from_right():
        right_tile = bruma.surroundings[Direction.RIGHT]
        bruma.grab_item(right_tile)

    def use_key():
        bruma.use_item(key)

    def show_map():
        print(map_)

    mappings = {"up": go_up,
                "down": go_down,
                "right": go_right,
                "left": go_left,
                "grab": grab_item_from_right,
                "use": use_key,
                "show map": show_map}

    action = input("What to do now? ")
    mappings[action]()

def bruma_information(): print("Name: {0} / Position: {1}".format(bruma.name, bruma.position))
def show_map(): print(str(map_))
screen = Screen(show_map, bruma_information, control_bruma)
while True:
    screen.show()


