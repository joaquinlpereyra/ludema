from game.board import Map, Door, Character

map_ = Map(10, 10)
bruma = Character(0, 0, "Bruma")
door = Door(5, 5)
map_.put_object(bruma)
map_.put_object(door)
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
