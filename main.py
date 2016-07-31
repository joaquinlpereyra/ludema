from game.board import Board
from game.utils import Position, Direction
from game.pieces import Door, _Character
from game.items import Key

map_ = Board("Main", 2, 2)
bruma = _Character("Bruma")
door = Door("A")
map_.put_piece(bruma, Position(0,0))
map_.put_piece(door, Position(1,1))

print(map_)

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

def show_map():
    print(map_)

mappings = {"up" : go_up,
            "down" : go_down,
            "right" : go_right,
            "left" : go_left,
            "show map" : show_map}

while True:
    order = input("What to do?")
    mappings[order]()
    print(map_)
