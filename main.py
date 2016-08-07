from game.board import Board
from game.utils import Position, Direction
from game.pieces import Character
from game_pieces import Door, Key

map_ = Board("Main", 2, 2)
bruma = Character("Y", "Bruma")
door = Door("Door1")
key = Key("Key1", door, letter="K")
map_.put_piece(bruma, Position(0,0))
map_.put_piece(door, Position(1,1))
map_.put_piece(key, Position(1,0))

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

while True:
    print(map_)
    order = input("What to do?")
    mappings[order]()
