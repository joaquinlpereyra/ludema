from game.board import Board
from game.pieces import Door, _Character
from game.items import Key

map_ = Board(10, 10)
bruma = _Character("Bruma")
door = Door()
map_.put_piece(bruma, 2, 2)
map_.put_piece(door, 5, 5)

print(map_)

def go_up():
    bruma.move("up")

def go_down():
    bruma.move("down")

def go_right():
    bruma.move("right")

def go_left():
    bruma.move("left")

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
